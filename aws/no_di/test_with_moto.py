import boto3
import pytest
from mypy_boto3_s3.client import S3Client
from moto import mock_aws
from src.ls import ls


@pytest.fixture
def mocked_s3() -> S3Client:
    """
    Creates a virtual AWS S3 bucket called "data" with a following structure:
    data
    │   file1.txt
    │
    └───folder
            file2.txt
            file3.txt
    All tests using this fixture will run moto instead of boto3.
    """
    with mock_aws():
        client: S3Client = boto3.Session().client("s3")
        client.create_bucket(Bucket="data")
        client.put_object(Bucket="data", Key="file1.txt", Body="Hello")
        client.put_object(Bucket="data", Key="folder/file2.txt", Body="Hello")
        client.put_object(Bucket="data", Key="folder/file3.txt", Body="Hello")
        yield client


def test_ls(mocked_s3: S3Client):
    result = ls("data", "folder")
    assert result == ["folder/file2.txt", "folder/file3.txt"]
