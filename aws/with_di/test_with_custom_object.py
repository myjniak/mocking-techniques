import pytest
from mypy_boto3_s3 import S3Client

from src.ls import ls


class MockedS3Client(S3Client):
    def __init__(self):
        pass

    def get_paginator(self, *args):
        return self

    @staticmethod
    def paginate(*args, **kwargs):
        return [
            {
                "Contents": [
                    {"Key": "folder/file2.txt"},
                    {"Key": "folder/file3.txt"}
                ]
            }
        ]


@pytest.fixture
def mocked_s3() -> MockedS3Client:
    return MockedS3Client()


def test_ls(mocked_s3):
    result = ls("data", "folder", client=mocked_s3)
    assert result == ["folder/file2.txt", "folder/file3.txt"]
