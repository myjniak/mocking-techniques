from typing import Optional

import boto3
from mypy_boto3_s3 import S3Client
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef


def ls(bucket: str, path: str, client: Optional[S3Client] = None) -> list[str]:
    if client is None:
        client: S3Client = boto3.Session().client("s3")
    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=path)
    bucket_objects = []
    for page in pages:
        page: ListObjectsV2OutputTypeDef
        for contents in page.get("Contents", []):
            bucket_objects.append(contents["Key"])
    return bucket_objects
