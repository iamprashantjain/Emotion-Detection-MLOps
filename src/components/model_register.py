import yaml
import os
import sys
import json
import mlflow
import logging
import os
import dagshub


from src.logger.logging import logging
from src.exception.exception import customexception

mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")
dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)


def load_model_info(file_path: str) -> dict:
    """Load the model info from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            model_info = json.load(file)
        logging.info('Model info loaded from %s', file_path)
        return model_info
    
    except Exception as e:
        logging.info('Unexpected error occurred while loading the model info: %s', e)
        raise customexception(e, sys)

def register_model(model_name: str, model_info: dict):
    """Register the model to the MLflow Model Registry."""
    try:
        model_uri = f"runs:/{model_info['run_id']}/{model_info['artifact_path']}"
        
        # Register the model
        model_version = mlflow.register_model(model_uri, model_name)
        
        # Transition the model to "Staging" stage from none
        client = mlflow.tracking.MlflowClient()
        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )
        
        logging.info(f'Model {model_name} version {model_version.version} registered and transitioned to Staging.')
    except Exception as e:
        logging.info('Error during model registration: %s', e)
        raise customexception(e, sys)



def load_params(params_path):
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.info("Parameters loaded successfully.")
        return params
    except Exception as e:
        raise customexception(e, sys)




def main():
    try:
        params = load_params("params.yaml")
        registration_params = params['model_registration']

        model_info_path = registration_params['model_info_path']
        model_name = registration_params['model_name']

        model_info = load_model_info(model_info_path)
        register_model(model_name, model_info)

    except Exception as e:
        logging.info('Failed to complete the model registration process: %s', e)
        raise customexception(e, sys)


if __name__ == '__main__':
    main()