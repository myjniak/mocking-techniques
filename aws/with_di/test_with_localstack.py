from src.ls import ls


def test_ls(local_s3):
    result = ls("data", "folder", client=local_s3)
    assert result == ["folder/file2.txt", "folder/file3.txt"]
