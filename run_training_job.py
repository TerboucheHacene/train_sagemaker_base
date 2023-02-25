import sagemaker
from sagemaker.estimator import Estimator


if __name__ == "__main__":
    # define input data
    data_dir = "s3://sagemaker-us-east-1-123456789012/tf-custom-container-test/data"
    # define output data
    output_dir = "s3://sagemaker-us-east-1-123456789012/tf-custom-container-test/output"

    # define input channels
    data_channels = {
        "train": data_dir,
    }

    # define hyperparameters
    hyperparameters = {
        "img_size": 150,
        "batch_size": 32,
        "validation_split": 0.2,
    }

    estimator = Estimator(
        image_uri=byoc_image_uri,
        role=get_execution_role(),
        base_job_name="tf-custom-container-test-job",
        instance_count=1,
        instance_type="ml.p2.xlarge",
    )
    # start training

    estimator.fit()
