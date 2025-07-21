# 📝 Project Workflow: Emotion Detection MLOps

## 🚀 Project Setup

1. **Create GitHub Repository**

   * Use MLOps project template and initialize a clean repository.

2. **Clone Repository Locally**

3. **Create Virtual Environment**

4. **Configure MLflow & DagsHub Tracking**

   ```python
   import dagshub
   dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)

   import mlflow
   with mlflow.start_run():
       mlflow.log_param('param', 'value')
       mlflow.log_metric('metric', 1)
   ```

   * MLflow Dashboard: [DagsHub MLflow UI](https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow)

---

## 🧪 Experimentation

5. **Test MLflow Connection**

6. **Run Experiments**

   * **Baseline:** Test different models.
   * **Vectorizer Comparison:** BOW vs TF-IDF.
   * **Hyperparameter Tuning:** Identify best algorithm + vectorizer combo.
   * **Track Experiments:** All runs logged on DagsHub MLflow UI.

---

## ⚙️ DVC Pipeline

7. `dvc init` – Initialize DVC.

8. **Configure DVC Remote:**

   * Local (e.g., `%TEMP%`) or S3 remote.

9. **Create DVC Pipeline:**

   * Define stages via `dvc.yaml` and parameters in `params.yaml`.

10. **Model Registry:** Push best model to MLflow Model Registry.

11. **S3 Setup:**

    * Create S3 bucket and add as DVC remote.

---

## 🖥️ Model Serving

12. **Model Inference API:**

    * Fetch model from registry, build a Flask API for real-time predictions.

---

## ⚙️ CI/CD Deployment

13. **CI Pipeline:**

    * Setup GitHub Actions for automated testing and builds.

14. **Dockerization:**

    * Build Docker image and push to AWS ECR.

15. **CD Pipeline:**

    * Setup continuous deployment pipeline.

16. **Production Deployment:**

    * Deploy on AWS EC2 or ECS.

---

✅ End-to-end Emotion Detection pipeline with Experiment Tracking (MLflow), Versioning (DVC), Model Registry, and Production Deployment (AWS).