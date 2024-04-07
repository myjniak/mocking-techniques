import subprocess
from pathlib import Path

import boto3
import pytest
from mypy_boto3_s3 import S3Client


def pytest_addoption(parser):
    parser.addoption("--docker-compose-path", action="store", default="")


@pytest.fixture
def localstack_s3_container(request):
    """On test setup: runs boto3 S3 simulation service on localhost.
    Remember to pass --docker-compose-path arg.
    On test teardown: container is stopped.
    """
    cwd = request.config.getoption("--docker-compose-path")
    if not (Path(cwd) / "docker-compose.yaml").exists():
        raise FileNotFoundError("Path to localstack S3 repo has to be provided with --docker-compose-path arg.\n"
                                "Example: python -m pytest --docker-compose-path=C:/Path/To/LocalStack-boto3")
    start_command = "docker-compose -f docker-compose.yaml up --build"
    stop_command = "docker-compose -f docker-compose.yaml down"
    process = subprocess.Popen(start_command, cwd=cwd, shell=True)
    yield
    process.terminate()
    process.wait()
    subprocess.Popen(stop_command, cwd=cwd, shell=True)
    print("Localstack S3 terminated successfully.")


@pytest.fixture
def local_s3(localstack_s3_container):
    """Using service on localhost, create a bucket and some files to prepare test assets"""
    s3: S3Client = boto3.client(
        service_name='s3',
        aws_access_key_id='test',
        aws_secret_access_key='test',
        endpoint_url='http://localhost:4566',
    )

    s3.create_bucket(Bucket="data")
    s3.put_object(Bucket="data", Key="file2.txt", Body="Hello")
    s3.put_object(Bucket="data", Key="folder/file2.txt", Body="Hello")
    s3.put_object(Bucket="data", Key="folder/file3.txt", Body="Hello")
    return s3
