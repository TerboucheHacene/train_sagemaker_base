FROM 763104351884.dkr.ecr.us-east-1.amazonaws.com/tensorflow-training:2.11.0-gpu-py39-cu112-ubuntu20.04-sagemaker


# code and data files
ENV CODE_PATH=/opt/ml/code
ENV MODEL_PATH=/opt/ml/model
ENV INPUT_PATH=/opt/ml/input
ENV PATH="/opt/ml/code:${PATH}"


COPY sagemaker-code /opt/ml/code
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt 

# Set up the program in the image
ENV SAGEMAKER_SUBMIT_DIRECTORY /opt/ml/code
ENV SAGEMAKER_PROGRAM train.py