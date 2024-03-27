import pytest

from src.printer import print_markdown_file, QTextDocument
from mock import patch


@pytest.mark.parametrize("md_filepath, expected", [
    ("data/sample.md", "I\nlove\npancakes\n\n\nPrinted by:\nMe")
])
def test_with_patching(mocker, md_filepath: str, expected: str):
    spy = mocker.spy(QTextDocument, "toPlainText")
    with patch.object(QTextDocument, "print", lambda self, _: spy(self)):
        print_markdown_file(md_filepath)
    assert spy.spy_return == expected
