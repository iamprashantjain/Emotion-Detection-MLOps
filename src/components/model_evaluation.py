import os
import sys
import pandas as pd
import yaml
import joblib
from sklearn.metrics import accuracy_score, classification_report
from src.logger.logging import logging
from src.exception.exception import customexception
import dagshub
import mlflow

# Set DagsHub + MLflow Tracking URI
mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")
dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)


def load_params(params_path):
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logging.info("Parameters loaded.")
        return params
    except Exception as e:
        logging.info("Error loading params.yaml")
        raise customexception(e, sys)


def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        X = df.drop(columns=["sentiment"]).values
        y = df["sentiment"].values
        logging.info("Test data loaded.")
        return X, y
    except Exception as e:
        logging.info("Error loading test data")
        raise customexception(e, sys)


def evaluate(model, X_test, y_test):
    try:
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        logging.info(f"Accuracy: {acc}")
        return acc, report
    except Exception as e:
        logging.info("Error during evaluation")
        raise customexception(e, sys)


def save_metrics(acc, report, metrics_path):
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
        logging.info(f"Metrics saved at {metrics_path}")
    except Exception as e:
        logging.info("Error saving metrics")
        raise customexception(e, sys)


def main():
    try:
        params = load_params("params.yaml")
        eval_params = params['model_evaluation']

        model_path = eval_params['model_path']
        input_test = eval_params['input_test']
        metrics_path = eval_params['metrics_path']

        model = joblib.load(model_path)
        X_test, y_test = load_data(input_test)

        acc, report = evaluate(model, X_test, y_test)

        save_metrics(acc, report, metrics_path)

        # MLflow Logging
        mlflow.set_experiment("dvc_pipeline")
        with mlflow.start_run(run_name="model_evaluation"):
            # Log Params
            mlflow.log_params(params['model_trainer']['model_params'])
            # Log Metrics
            mlflow.log_metric("accuracy", acc)
            mlflow.log_metric("precision_class_0", report["0"]["precision"])
            mlflow.log_metric("precision_class_1", report["1"]["precision"])
            mlflow.log_metric("recall_class_0", report["0"]["recall"])
            mlflow.log_metric("recall_class_1", report["1"]["recall"])
            
            #log model
            mlflow.sklearn.log_model(model, artifact_path="model")

        logging.info("Model evaluation pipeline completed with MLflow logging.")

    except Exception as e:
        logging.info("Exception in model_evaluation main function.")
        raise customexception(e, sys)


if __name__ == "__main__":
    main()
