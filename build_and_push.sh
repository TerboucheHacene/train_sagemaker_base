#!/usr/bin/env bash

# Build docker image, push to ECR for use with SageMaker

# exit when any command fails
set -e

# image name
image="train_sagemaker"


# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text --profile hacene)
echo "account $account"

if [ $? -ne 0 ]
then
    exit 255
fi

# Get the region defined in the current configuration (default to us-east-1 if none defined)
region=$(aws configure get region)
region=${region:-us-east-1}
echo "region $region"


fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

# Get the login command from ECR and execute it directly
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin $account.dkr.ecr.$region.amazonaws.com

# Get the login command from ECR in order to pull down the SageMaker PyTorch image
aws ecr get-login-password --region $region | docker login --username AWS --password-stdin 763104351884.dkr.ecr.$region.amazonaws.com



# Build the docker image locally with the image name and then push it to ECR
# with the full name.
docker buildx build --platform linux/amd64 --push -t haceneterbouche/${image} .
docker tag haceneterbouche/${image} ${fullname}

docker push ${fullname}

echo "BUILD AND PUSH COMPLETE!"