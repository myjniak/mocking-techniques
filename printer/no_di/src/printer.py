from PyQt6.QtGui import QTextDocument, QTextCursor
from PyQt6.QtPrintSupport import QPrinter
from PyQt6.QtWidgets import QApplication
from markdown import markdown


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
    cursor.insertText("\n\nPrinted by:\nJohn Awesome")
    return document


def print_markdown_file(filepath: str):
    text = read_file(filepath)
    with QApplication([]):
        document = prepare_document(text)
        printer = QPrinter()
        printer.setFullPage(True)
        document.print(printer)
        return document


if __name__ == "__main__":
    print_markdown_file("data/sample.md")
