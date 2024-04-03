from unittest.mock import patch, MagicMock

import pytest

from src.ls import ls


@pytest.fixture
def mocked_s3() -> MagicMock:
    """This monkeypatching will only assure that the tested function is
    calling expected methods from expected attributes and parses output correctly.
    As opposed to moto it is ignoring the tested function input arguments.
    """
    with patch('src.ls.boto3.Session') as mocked_boto3_session:
        client = mocked_boto3_session.return_value.client.return_value
        paginate = client.get_paginator.return_value.paginate
        paginate.return_value = [
            {
                "Contents": [
                    {"Key": "folder/file2.txt"},
                    {"Key": "folder/file3.txt"}
                ]
            }
        ]
        yield client


def test_ls(mocked_s3):
    result = ls("data", "folder")
    assert result == ["folder/file2.txt", "folder/file3.txt"]
