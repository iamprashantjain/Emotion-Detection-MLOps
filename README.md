# Emotion Detection MLOps Pipeline

This project shows a complete MLOps workflow for Emotion Detection using DVC, MLflow, DagsHub, and AWS (ECR/ECS).

---

## Project Setup

1. **Create a GitHub Repository**

   Start by creating a GitHub repository using a machine learning project template.

2. **Clone the Repository Locally**

   Clone that repository to your local system.

3. **Set Up a Virtual Environment**

   Create and activate a virtual environment to manage project dependencies.

4. **Configure MLflow Tracking on DagsHub**

   Connect MLflow tracking to DagsHub using the following code:

   ```python
   import dagshub, mlflow

   dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)
   mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")

   with mlflow.start_run():
       mlflow.log_param('parameter', 'value')
       mlflow.log_metric('metric', 1)
   ```

   You can access the MLflow dashboard on DagsHub here:
   [DagsHub MLflow Dashboard](https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow)

---

## Experimentation

5. **Verify MLflow Integration**

   Test MLflow is properly connected and tracks experiments.

6. **Run Experiments**

   * First, run a baseline model.
   * Next, compare Bag-of-Words and TF-IDF vectorization.
   * Then, tune hyperparameters to find the best combination.
   * All experiments will be tracked through MLflow on DagsHub.

---

## DVC Pipeline

7. **Initialize DVC**

   Use the command `dvc init` to start version controlling your data.

8. **Add DVC Remote**

   Set up a local remote, or connect to AWS S3 as a remote storage.

9. **Create a DVC Pipeline**

   Define your pipeline using `dvc.yaml` and `params.yaml`.

10. **Register the Best Model**

    Save best performing model in the MLflow model registry.

11. **Set Up AWS S3 Bucket**

    Use S3 as a DVC remote to store data and artifacts.

---

## Model Serving

12. **Build a Flask API**

    Create a simple Flask application that fetches the latest production model from the registry and serves predictions.

---

## CI/CD Automation

13. **Set Up Continuous Integration with GitHub Actions**

    * Run the entire DVC pipeline on every code push.
    * Register the latest model in the staging phase.
    * Run automated tests to check:

      * Model input and output formats
      * Model performance
      * Flask API functionality
    * If all tests pass, promote the model to production.

14. **Dockerize the Flask App**

    Build a Docker image of your Flask application and push it to AWS ECR.

15. **Set Up Continuous Deployment**

    Deploy the production-ready model and Flask API using AWS EC2 or ECS.

---

## Summary

This project shows a complete cycle of working with version-controlled data and code, running machine learning experiments, registering models, building a prediction API, and setting up automated CI/CD with deployment to the cloud.
