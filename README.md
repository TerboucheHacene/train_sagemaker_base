# Train a Deep Learning Model on SageMaker
A repo to train a Custom Deep Learning Model with Amazon SageMaker


## 1. How to create buckets for input and output
    aws s3 mb s3://sagemaker-train-data-hacene
    aws s3 mb s3://sagemaker-output-data-hacene

## 2. How to download and uplaod the dataset to S3
    kaggle datasets download -d alxmamaev/flowers-recognition
    unzip flowers-recognition.zip
    aws s3 sync flowers s3://sagemaker-train-data-hacene/flowers


## 3. Create an ECR Repository

    account=$(aws sts get-caller-identity --query Account --output text --profile=hacene)

    region=$(aws configure get region)
    
    aws ecr get-login-password --region $region| docker login --username AWS --password-stdin $account.dkr.ecr.$region.amazonaws.com

    aws ecr create-repository --repository-name train_sagemaker

## 4. Build and push the Image

    ./build_and_push.sh


## 5. Launch the Training Job

     aws sagemaker create-training-job --cli-input-json file://training-config.json