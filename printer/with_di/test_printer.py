from unittest.mock import Mock

import pytest

from src.printer import print_markdown_file


@pytest.mark.parametrize("md_filepath, expected", [
    ("data/sample.md", "I\nlove\npancakes\n\n\nPrinted by:\nMe")
])
def test_with_di(md_filepath: str, expected: str):
    nothing = Mock()
    printed_document = print_markdown_file(md_filepath, print_func=nothing)
    assert printed_document.toPlainText() == expected
    nothing.assert_called_once_with(printed_document)
