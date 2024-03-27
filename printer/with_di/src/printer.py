from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QApplication
from markdown import markdown
from typing import Callable, Any


def print_on_paper(document: QTextDocument):
    printer = QPrinter()
    printer.setFullPage(True)
    document.print(printer)


def read_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read()


def prepare_document(text: str) -> QTextDocument:
    html_doc = markdown(text)
    document = QTextDocument()
    document.setHtml(html_doc)
    cursor = QTextCursor(document)
    cursor.movePosition(QTextCursor.MoveOperation.End)
    cursor.insertBlock()
    cursor.movePosition(QTextCursor.MoveOperation.End)
    cursor.insertText("\n\nPrinted by:\nMe")
    return document


def print_markdown_file(
        filepath: str,
        print_func: Callable[[QTextDocument], Any] = print_on_paper
):
    content = read_file(filepath)
    with QApplication([]):
        doc = prepare_document(content)
        print_func(doc)
        return doc


if __name__ == "__main__":
    print_markdown_file("data/sample.md")
