# train_sagemaker_base
A repo to train a Custom Deep Learning Model with Amazon SageMaker


aws s3 mb s3://sagemaker-train-data-hacene
aws s3 mb s3://sagemaker-output-data-hacene

kaggle datasets download -d alxmamaev/flowers-recognition
unzip flowers-recognition.zip
aws s3 sync flowers s3://sagemaker-train-data-hacene

account=$(aws sts get-caller-identity --query Account --output text)
echo "account $account"

# Get the region defined in the current configuration (default to us-east-1 if none defined)
region=$(aws configure get region)
region=${region:-us-east-1}
echo "region $region"

aws ecr get-login-password --region $region| docker login --username AWS --password-stdin $account.dkr.ecr.$region.amazonaws.com

aws ecr create-repository --repository-name sagemaker-images

340195785701.dkr.ecr.us-east-1.amazonaws.com/sagemaker-images

image="train_sagemaker"
fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

