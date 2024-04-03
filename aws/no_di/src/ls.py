import boto3


def ls(bucket: str, path: str) -> list[str]:
    client = boto3.Session().client("s3")
    paginator = client.get_paginator("list_objects_v2")
    pages: list[dict] = paginator.paginate(Bucket=bucket, Prefix=path)
    bucket_objects = []
    for page in pages:
        for contents in page.get("Contents", []):
            bucket_objects.append(contents["Key"])
    return bucket_objects
