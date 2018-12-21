#!/usr/bin/env python3


from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from zotler.gui.ui.custom_widgets import LabeledPath, LabeledCheckBox


class DeleteOrphans(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, flags=Qt.WindowFlags())

        self.main_layout = QVBoxLayout()
        self.path_to_list_of_orphans = LabeledPath(
            parent=self,
            label='Path to the file:',
            name='path_to_list_of_orphans',
            tooltip='Path to the file containing path to orphan files',
            vertical=True,
        )

        self.init_ui()

    def init_ui(self):
        self.main_layout.setContentsMargins(0, 10, 0, 0)
        self.main_layout.setSpacing(10)

        self.main_layout.addWidget(self.path_to_list_of_orphans, 0, Qt.AlignBottom)
        self.main_layout.addStretch(2)

        self.setLayout(self.main_layout)


class FindOrphans(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, flags=Qt.WindowFlags())

        self.main_layout = QVBoxLayout()

        self.path_to_prefs_file = LabeledPath(
            parent=self,
            label='Path to the Zotero settings file prefs.js:',
            name='path_to_list_of_orphans',
            tooltip='Path to the file containing Zotero preferences (prefs.js).',
            vertical=True,
        )

        self.path_to_database_file = LabeledPath(
            parent=self,
            label='Path to the Zotero database file zotero.sqlite:',
            name='path_to_database_file',
            tooltip='Path to the file containing Zotero database file (zotero.sqlite).',
            vertical=True,
        )

        self.path_to_output_file = LabeledPath(
            parent=self,
            label='Path to the output file with paths to orphan files '
                  '(A temporary file will be used if empty):',
            name='path_to_output_file',
            tooltip='Path to the output file with paths to orphan files.',
            vertical=True,
        )

        self.init_ui()

    def init_ui(self):

        self.main_layout.setContentsMargins(0, 10, 0, 0)
        self.main_layout.setSpacing(10)

        self.main_layout.addWidget(self.path_to_prefs_file, 0, Qt.AlignBottom)
        self.main_layout.addWidget(self.path_to_database_file, 0, Qt.AlignBottom)
        self.main_layout.addWidget(self.path_to_output_file, 0, Qt.AlignBottom)
        self.main_layout.addStretch(2)

        self.setLayout(self.main_layout)

    def print_stat(self):
        pass
