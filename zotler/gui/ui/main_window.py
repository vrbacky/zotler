#!/usr/bin/env python3

import os
from pathlib import Path
import tempfile

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import QLabel, QMainWindow, QPushButton, QWidget,\
    QHBoxLayout, QVBoxLayout, QStackedWidget

from zotler import __author__, __name__, __version__, zotler
from zotler.gui.ui.custom_widgets import LabeledComboBox
from zotler.gui.ui.variable_areas import DeleteOrphans, FindOrphans
from zotler.gui.ui.dialogs import AboutDialog, ShowStdinDialog
from zotler.exceptions import InvalidModeError

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent, flags=Qt.WindowFlags())

        script_dir = os.path.dirname(os.path.realpath(__file__))
        self.path_to_icon = os.path.sep.join((script_dir,
                                              '..',
                                              'icons',
                                              'zotler.ico'))
        self.icon = QPixmap(self.path_to_icon)
        self.title = f'{__name__.title()} v{__version__}'

        path_to_license = os.path.join(os.path.dirname(__file__),
                                       '..', '..', '..', 'LICENSE.md')
        with open(path_to_license) as license_file:
            license_text = '\n'.join(license_file.readlines())

        self.about_dialog = AboutDialog(self,
                                        icon=self.icon,
                                        title=self.title,
                                        name=self.title,
                                        copyright_text=f'(c)2018 by {__author__}',
                                        license_text=license_text
                                        )

        self.main_widget = MainWidget(parent=self)

        self.init_ui()

    def init_ui(self):
        self.setWindowIcon(QIcon(self.path_to_icon))
        self.setWindowTitle(self.title)
        self.setCentralWidget(self.main_widget)

        self.show()


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent, flags=Qt.WindowFlags())
        self.parent = parent
        self.icon = parent.icon

        self.main_layout = QVBoxLayout()

        self.header_layout = QHBoxLayout()
        self.header_left_layout = QVBoxLayout()
        self.icon_layout = QVBoxLayout()
        self.icon_label = QLabel()
        self.header_right_layout = QVBoxLayout()
        self.app_name = QLabel(__name__.title())
        self.app_version = QLabel(__version__)
        self.author_name = QLabel(f'(c)2018 by {__author__}')

        self.choose_mode = LabeledComboBox(values=('Find and delete orphan files',
                                                   'Delete orphan files'),
                                           label='Choose mode:',
                                           vertical=True)
        self.load_defaults_button = QPushButton('Fill in default values')

        self.specific_layout = QVBoxLayout()
        self.specific_area_stack = QStackedWidget(self)
        self.find_orphans = FindOrphans()
        self.delete_orphans = DeleteOrphans()
        self.variable_area_widgets = (
            self.find_orphans,
            self.delete_orphans,
        )

        self.buttons_layout = QHBoxLayout()
        self.about_button = QPushButton('About...')
        self.cancel_button = QPushButton('Cancel')
        self.ok_button = QPushButton('OK')

        self.init_ui()

    def init_ui(self):
        self.choose_mode.input_widget.currentIndexChanged.connect(self.action_changed)
        self.load_defaults_button.clicked.connect(self.fill_in_default_values)
        self.about_button.clicked.connect(self.open_about)
        self.cancel_button.clicked.connect(self.quit_action)
        self.ok_button.clicked.connect(self.run_action)

        self.main_layout.setContentsMargins(15, 10, 15, 10)
        self.main_layout.addLayout(self.header_layout, 0)
        self.main_layout.addLayout(self.specific_layout, 0)
        self.main_layout.addLayout(self.buttons_layout, 0)
        self.main_layout.addStretch(2)

        self.header_layout.setSpacing(10)
        self.header_layout.addLayout(self.header_left_layout, 2)
        self.header_layout.addLayout(self.icon_layout, 0)
        self.header_layout.addLayout(self.header_right_layout, 0)

        self.header_left_layout.addWidget(self.choose_mode, 0, Qt.AlignBottom)
        self.header_left_layout.addWidget(self.load_defaults_button, 0, Qt.AlignBottom)

        self.icon_layout.setContentsMargins(0, 15, 0, 0)
        self.icon_layout.addWidget(self.icon_label, 0, Qt.AlignBottom)
        self.icon_label.setPixmap(self.icon)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setFixedWidth(100)
        self.icon_label.setFixedHeight(85)
        self.icon_label.setContentsMargins(75, 75, 75, 150)

        self.header_right_layout.addWidget(self.app_name, 0, Qt.AlignBottom)
        self.header_right_layout.addWidget(self.app_version, 0, Qt.AlignBottom)
        self.header_right_layout.addWidget(self.author_name, 0, Qt.AlignBottom)
        self.app_name.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.app_name.setFont(font)
        self.app_version.setAlignment(Qt.AlignCenter)
        self.author_name.setAlignment(Qt.AlignCenter)

        self.load_defaults_button.setMinimumWidth(250)
        self.load_defaults_button.setMinimumHeight(40)
        self.load_defaults_button.setStyleSheet("background-color: darkseagreen")

        self.specific_layout.setContentsMargins(0, 0, 0, 0)
        self.specific_layout.setSpacing(0)
        self.specific_layout.addWidget(self.specific_area_stack, Qt.AlignBottom)

        for widget in self.variable_area_widgets:
            self.specific_area_stack.addWidget(widget)

        self.buttons_layout.setContentsMargins(0, 10, 0, 0)
        self.buttons_layout.addStretch(2)
        self.buttons_layout.addWidget(self.about_button, 0, Qt.AlignBottom)
        self.buttons_layout.addWidget(self.cancel_button, 0, Qt.AlignBottom)
        self.buttons_layout.addWidget(self.ok_button, 0, Qt.AlignBottom)

        self.setLayout(self.main_layout)

    def action_changed(self, index):
        self.specific_area_stack.setCurrentIndex(index)
        self.change_defaults_button_status(index)

    def change_defaults_button_status(self, index):
        if index == 1:
            self.load_defaults_button.setEnabled(False)
        else:
            self.load_defaults_button.setEnabled(True)

    def fill_in_default_values(self):
        path_to_prefs_file = zotler.get_prefs_file(silent=True)
        self.find_orphans.path_to_prefs_file.text = path_to_prefs_file

        zotero_home_dir = os.path.join(str(Path.home()), 'Zotero')
        self.find_orphans.path_to_database_file.text = os.path.join(zotero_home_dir,
                                                                    'zotero.sqlite')

    def open_about(self):
        self.parent.about_dialog.show()

    def run_action(self):
        if self.choose_mode.text == 'Find and delete orphan files':
            self.find_orphans_action()
        elif self.choose_mode.text == 'Delete orphan files':
            self.delete_orphans_action(
                self.delete_orphans.path_to_list_of_orphans.text.strip()
            )
        else:
            raise InvalidModeError('Invalid mode\'s been chosen.')

        self.quit_action()

    def find_orphans_action(self):
        zotero_prefs = self.find_orphans.path_to_prefs_file.text
        zotero_dbase = self.find_orphans.path_to_database_file.text
        orphan_files = zotler.create_set_of_orphans(zotero_dbase, zotero_prefs)

        path_to_output_file = self.find_orphans.path_to_output_file.text.strip()
        if path_to_output_file == '':
            _, path_to_output_file = tempfile.mkstemp(prefix='zotler_gui-')

        with open(path_to_output_file, 'w') as output_file:
            print('\n'.join(orphan_files), file=output_file)

        self.delete_orphans_action(path_to_output_file)

    def delete_orphans_action(self, path_to_orphans_file):
        text_dialog = ShowStdinDialog(self, file_path=path_to_orphans_file)
        is_accepted = text_dialog.exec()
        if is_accepted:
            with open(path_to_orphans_file, 'r') as file:
                zotler.remove_files(file.readlines())

    @staticmethod
    def quit_action():
        QCoreApplication.instance().quit()
