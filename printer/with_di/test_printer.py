import pytest
from PyQt6.QtGui import QTextDocument

from src.printer import print_markdown_file


@pytest.mark.parametrize("md_filepath, expected", [
    ("data/sample.md", "I\nlove\npancakes\n\n\nPrinted by:\nJohn Awesome")
])
def test_with_di(md_filepath: str, expected: str):
    printed_document = print_markdown_file(md_filepath, print_method=QTextDocument.toPlainText)
    assert printed_document.toPlainText() == expected
