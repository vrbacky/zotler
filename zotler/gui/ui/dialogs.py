#!/usr/bin/env python3

from PyQt5.QtWidgets import QMessageBox, QTextEdit, QHBoxLayout, QVBoxLayout, QDialog, QLabel, QPushButton
from PyQt5.QtCore import Qt


class AboutDialog(QMessageBox):
    def __init__(self, parent, icon=QMessageBox.Information, title='',
                 name='', copyright_text='', license_text=''):
        super().__init__(parent)

        if isinstance(icon, QMessageBox.Icon):
            self.setIcon(icon)
        else:
            self.setIconPixmap(icon)
        self.setWindowTitle(title)
        self.setText(name)
        self.setInformativeText(copyright_text)
        self.setDetailedText(license_text)
        self.setStandardButtons(QMessageBox.Ok)


class ShowStdinDialog(QDialog):
    def __init__(self, parent, file_path):
        super().__init__(parent)

        self._file_path = file_path
        self.layout = QVBoxLayout()

        self.label = QLabel('Delete these files?')
        self.text_box = QTextEdit()

        self.buttons_layout = QHBoxLayout()
        self.ok_button = QPushButton('Save and delete')
        self.cancel_button = QPushButton('Save and don\'t delete')

        self. show_ui()

    def show_ui(self):
        self.cancel_button.clicked.connect(self.cancel_pushed)
        self.ok_button.clicked.connect(self.ok_pushed)

        self.setModal(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.text_box)

        self.buttons_layout.addStretch(2)
        self.buttons_layout.addWidget(self.cancel_button, 0, Qt.AlignBottom)
        self.buttons_layout.addWidget(self.ok_button, 0, Qt.AlignBottom)
        self.layout.addLayout(self.buttons_layout)

        self.setLayout(self.layout)

        with open(self._file_path) as file:
            self.text_box.setText(file.read())

    def cancel_pushed(self):
        self.save_file()
        self.reject()

    def ok_pushed(self):
        self.save_file()
        self.accept()

    def save_file(self):
        with open(self._file_path, 'w') as file:
            file.write(self.text_box.toPlainText())
