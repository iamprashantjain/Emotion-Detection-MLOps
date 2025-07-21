import os
import sys
import json
import pandas as pd
import yaml
import joblib
from sklearn.metrics import accuracy_score, classification_report
from src.logger.logging import logging
from src.exception.exception import customexception
import dagshub
import mlflow

# Initialize DagsHub + MLflow Tracking URI
# mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")
# dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)


# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("DAGSHUB_PAT")
if not dagshub_token:
    raise EnvironmentError("DAGSHUB_PAT environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "iamprashantjain"
repo_name = "Emotion-Detection-MLOps"

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')


def load_params(params_path: str):
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.info("Parameters loaded successfully.")
        return params
    except Exception as e:
        logging.info("Error loading params.yaml")
        raise customexception(e, sys)


def load_data(file_path: str):
    try:
        df = pd.read_csv(file_path)
        X = df.drop(columns=["sentiment"]).values
        y = df["sentiment"].values
        logging.info(f"Test data loaded from {file_path}")
        return X, y
    except Exception as e:
        logging.info("Error loading test data")
        raise customexception(e, sys)


def evaluate_model(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        logging.info(f"Model evaluated with Accuracy: {acc}")
        return acc, report
    except Exception as e:
        logging.info("Error during model evaluation")
        raise customexception(e, sys)


def save_metrics(acc, report, metrics_path: str):
    try:
        os.makedirs(os.path.dirname(metrics_path), exist_ok=True)
        metrics = {
            "accuracy": float(acc),
            "precision_class_0": float(report["0"]["precision"]),
            "precision_class_1": float(report["1"]["precision"]),
            "recall_class_0": float(report["0"]["recall"]),
            "recall_class_1": float(report["1"]["recall"])
        }
        with open(metrics_path, "w") as f:
            yaml.dump(metrics, f)
        logging.info(f"Metrics saved to {metrics_path}")
    except Exception as e:
        logging.info("Error saving metrics")
        raise customexception(e, sys)


def save_model_info(run_id: str, artifact_path: str, output_file: str):
    try:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        model_info = {
            "run_id": run_id,
            "artifact_path": artifact_path
        }
        with open(output_file, "w") as f:
            json.dump(model_info, f, indent=4)
        logging.info(f"Model info saved at {output_file}")
    except Exception as e:
        logging.info("Error saving model information JSON file")
        raise customexception(e, sys)


def main():
    try:
        params = load_params("params.yaml")
        eval_params = params["model_evaluation"]
        trainer_params = params["model_trainer"]

        model_path = eval_params["model_path"]
        input_test = eval_params["input_test"]
        metrics_path = eval_params["metrics_path"]
        experiment_name = eval_params["experiment_name"]
        run_name = eval_params["run_name"]
        experiment_info_path = eval_params["experiment_info_path"]

        logging.info(f"Loading model from {model_path}")
        model = joblib.load(model_path)

        X_test, y_test = load_data(input_test)

        acc, report = evaluate_model(model, X_test, y_test)

        save_metrics(acc, report, metrics_path)

        mlflow.set_experiment(experiment_name)

        with mlflow.start_run(run_name=run_name) as run:
            mlflow.log_params(trainer_params["model_params"])
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision_class_0", report["0"]["precision"])
            mlflow.log_metric("precision_class_1", report["1"]["precision"])
            mlflow.log_metric("recall_class_0", report["0"]["recall"])
            mlflow.log_metric("recall_class_1", report["1"]["recall"])

            mlflow.sklearn.log_model(model, artifact_path="model")
            save_model_info(run.info.run_id, "model", experiment_info_path)

        logging.info("Model evaluation pipeline completed successfully with MLflow tracking.")

    except Exception as e:
        logging.info("Exception in model_evaluation main function.")
        raise customexception(e, sys)


if __name__ == "__main__":
    main()
