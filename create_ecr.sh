#!/usr/bin/env bash

# Build docker image, push to ECR for use with SageMaker

# exit when any command fails
set -e

# ECR repository name
repository_name="train_sagemaker"

account=$(aws sts get-caller-identity --query Account --output text --profile=hacene)
echo "account $account"

if [ $? -ne 0 ]
then
    exit 255
fi

region=$(aws configure get region)
region=${region:-us-east-1}
echo "region $region"

# Get the login command from ECR and execute it directly
aws ecr get-login-password --region $region| docker login --username AWS --password-stdin $account.dkr.ecr.$region.amazonaws.com

# Create ECR repository if it does not exist
aws ecr create-repository --repository-name $repository_name --region $region

