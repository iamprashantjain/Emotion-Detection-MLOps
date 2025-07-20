import dagshub
import mlflow

mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")
dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)

with mlflow.start_run():
  mlflow.log_param('parameter name', 'value')
  mlflow.log_metric('metric name', 1)
