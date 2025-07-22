-- project setup --

1. create github repo from ml template

2. clone on local pc (clean based on current project)

3. create venv

4. host mlflow on dagshub

    --------------------------------------------------------------------------------------------
    https://dagshub.com/iamprashantjain/Emotion-Detection-MLOps.mlflow

    import dagshub
    dagshub.init(repo_owner='iamprashantjain', repo_name='Emotion-Detection-MLOps', mlflow=True)

    import mlflow
    with mlflow.start_run():
    mlflow.log_param('parameter name', 'value')
    mlflow.log_metric('metric name', 1)

    --------------------------------------------------------------------------------------------

-- Experiments --

5. test mlflow if connected

6. run 3 experiments
    - baseline, bow vs tfidf -- this will give best model & best vectorizer
    - from there find best parameters of that algo & vectorizer combincation
    - track all experiments on mlflow hosted on dagshub

-- DVC Pipeline --

7. dvc init
8. add dvc remote (local or s3) - echo %TEMP%
9. crate dvc pipeline (dvc.yaml + params.yaml)
10. send best model to model_registry
11. create s3 bucket
12. add s3 dvc remote

-- model serving --

13. write a code to fetch model from model_registry, create flask app and make predictions


-- Continous Integration --

14. apply CI
    - generate requirements_dev.txt
    - create .github/workflows/ci.yaml
    - run dvc pipeline on github actions means latest model will be registered in staging stage
        - error: "Authorization Required: dagshub auth required to access mlflow hosted on dagshub" -- create github secret variable of dagshub token
        - error: src not found - use PYTHONPATH
    - test model: load model, model signature to avoid shape mismatch
        - model test: check if model loading correctly (1_model_loading.py)
    - model performance
    - once testing completed then promote model to production
    - flask app test
    - model in produciton will be used by flask app to make predictions


15. create Docker image
    - add ci/cd step to dockerize just flask_app and its dependecies like vectorizer etc -- no need to dockerize whole project
    - create seperate requirements_prod.txt -- use pipreqs / pipreqs . --force
    - add host="0.0.0.0" in flask app to make it accessible from outside of docker
    - add production server : gunicorn
        + add gunicorn in requirements
        + add "CMD['gunicorn','-b','0.0.0.0:5000','app.py']" in dockerfile
    - create docker image using buildkit for faster execution:
        + set DOCKER_BUILDKIT=1
        + docker build -t emotion-detector:latest .
        + solve DAGSHUB_PAT environment variable -- docker run -p 5000:5000 -e DAGSHUB_PAT=your_actual_token emotion-detector:latest
        + docker run -p 5000:5000 -e DAGSHUB_PAT=bd4136ab964348874ebb74d06e9d10f5bf763d52 emotion-detector:latest
        + docker build -t emotion-detector:latest . && docker run -p 5000:5000 -e DAGSHUB_PAT=your_actual_token emotion-detector:latest
        

16. apply docker image creation in CI
    - build docker image via ci.yaml


17. Deployment
    1. ECR to EC2 
    2. ECR to ECS (Scalable)

    - **Why ECR instead of Dockerhub**
        1. Tightly integrated with other AWS services
        2. IAM based access control
        3. High availability & Automatic scaling for n number of push-pulls
        4. Security: all repos are private by default
        5. ECR repos are automatically encrypted
        6. VPC endpoints (not available on public internet)
        7. Highly cost effective
        8. No rate limits unlike dockerhub
        9. All repos will be scanned for Vulnerability check
        10. Global coverage of servers
        11. Image lifecycle management: we can set policies or rules to manage image lifecycle when to archive or delete etc
        12. Fully managed services - No need to worry about infra
        13. ECR integrates easily with CI/CD
        14. Support multi architecture images like windows, linux or max os
        

    - **How to reduce docker image size**
    - 

    - Create ECR repo
         - Create ECR: "prashant-mlops-ecr" normally without changing any settings
    
    - Push docker image to ECR via ci.yaml
      - "View push commands" to know how to push docker image to ECR
         1. aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 739275446561.dkr.ecr.ap-south-1.amazonaws.com
         2. docker build -t prashant-mlops-ecr .

    - In EC2, we will pull image from ECR and run via cicd pipeline
         1. create EC2
         2. run below commands to setup EC2

         ![alt text](image-1.png)

         3. after setup done, update cicd pipeline
         4. updated AWS security groups

         ![alt text](image-2.png)

    - 

      
      ![alt text](image.png)

    - 





