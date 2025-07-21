# 🚀 Emotion Detection MLOps Pipeline

This project demonstrates a complete Machine Learning Operations (MLOps) workflow for Emotion Detection using **DVC**, **MLflow**, **DagsHub**, and **AWS (ECR/ECS)**.

---

## ✅ Project Setup

1. **Create GitHub Repository**

   * Use ML project template and initialize a clean repository.

2. **Clone Repository Locally**

3. **Setup Virtual Environment**

4. **Configure MLflow Tracking on DagsHub**

   ```python
   import dagshub, mlflow

   dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)
   mlflow.set_tracking_uri("https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow")

   with mlflow.start_run():
       mlflow.log_param('parameter', 'value')
       mlflow.log_metric('metric', 1)
   ```

   * MLflow UI: [DagsHub MLflow Dashboard](https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow)

---

## 🧪 Experimentation

5. **Verify MLflow Integration**

6. **Run Experiments**

   * **Experiment 1:** Baseline model
   * **Experiment 2:** Bag-of-Words (BoW) vs TF-IDF Vectorization
   * **Experiment 3:** Hyperparameter tuning for best model-vectorizer combo
   * Track all experiments via **MLflow** on **DagsHub**.

---

## ⚙️ DVC Pipeline

7. **Initialize DVC:** `dvc init`

8. **Add DVC Remote:**

   * Local remote: `%TEMP%`
   * Optional: Configure AWS S3 remote.

9. **Create DVC Pipeline:**

   * Define pipeline via `dvc.yaml` and `params.yaml`.

10. **Register Best Model** in **MLflow Model Registry**.

11. **Setup AWS S3 Bucket** and configure as **DVC Remote**.

---

## 🖥️ Model Serving

12. **Build Flask API:**

    * Fetch the latest production model from Model Registry and serve real-time predictions via Flask app.

---

## 🔄 CI/CD Automation

13. **Continuous Integration (CI) with GitHub Actions:**

* Run the complete **DVC pipeline** on every push.
* Register the latest model in **Staging**.
* Automated tests:

  * Model signature validation
  * Performance metrics validation
  * Flask API endpoint testing
* On successful validation, promote model to **Production**.

14. **Dockerize Flask App**

    * Build Docker image and push to **AWS ECR**.

15. **Continuous Deployment (CD):**

    * Deploy the production-ready model and Flask app on **AWS EC2** or **ECS**.

---

### 📌 End-to-End Workflow:

Version-controlled data & code → ML Experiments Tracking → Model Registry → Model Serving API → Automated CI/CD → Cloud Deployment.