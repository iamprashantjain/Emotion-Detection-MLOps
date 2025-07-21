import os
import mlflow
from src.logger.logging import logging
from src.exception.exception import customexception


def get_latest_model_version(model_name, stage="Production"):
    """
    Get the latest version number of a model in a given stage (default is Production).

    Args:
        model_name (str): Name of the registered MLflow model.
        stage (str): MLflow stage (e.g., "Production", "Staging").

    Returns:
        str: Latest version number as string or None if not found.
    """
    client = mlflow.MlflowClient()
    latest_versions = client.get_latest_versions(model_name, stages=[stage])
    return latest_versions[0].version if latest_versions else None


def promote_model():
    """
    Promote the latest model from 'Staging' to 'Production' in MLflow model registry.
    It also archives any previous models in 'Production' stage.
    """
    #Authenticate to DagsHub using Personal Access Token (PAT)
    dagshub_token = os.getenv("DAGSHUB_PAT")
    if not dagshub_token:
        raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

    #Setup MLflow credentials for DagsHub
    os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
    os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

    #Configure MLflow tracking URI (DagsHub repo)
    dagshub_url = "https://dagshub.com"
    repo_owner = "iamprashantjain"
    repo_name = "Emotion-Detection-MLOps"
    mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')

    #Initialize MLflow client
    client = mlflow.MlflowClient()
    model_name = "emotion_predictor_model"

    #Get latest model in Staging
    staging_version = get_latest_model_version(model_name, stage="Staging")
    if not staging_version:
        raise ValueError(f"No model version found in 'Staging' stage for {model_name}")

    #Archive any currently active Production models
    prod_versions = client.get_latest_versions(model_name, stages=["Production"])
    if prod_versions:
        for version in prod_versions:
            logging.info(f"Archiving current Production version {version.version}")
            client.transition_model_version_stage(
                name=model_name,
                version=version.version,
                stage="Archived"
            )

    #Promote latest Staging version to Production
    client.transition_model_version_stage(
        name=model_name,
        version=staging_version,
        stage="Production"
    )
    logging.info(f"Model version {staging_version} promoted to Production successfully.")


if __name__ == "__main__":
    promote_model()