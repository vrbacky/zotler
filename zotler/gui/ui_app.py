#!/usr/bin/env python3

import sys
from PyQt5.QtWidgets import QApplication

from zotler.gui.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    exit(main())