#!/usr/bin/env python3

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QCheckBox, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout,\
    QWidget, QComboBox, QFileDialog, QPushButton


class LabeledWidget(QWidget):
    def __init__(self, widget, parent=None, label='Font size:',
                 width=40, name='', tooltip='', vertical=False, is_widget_first=False):
        super().__init__(parent=parent, flags=Qt.WindowFlags())

        self.label = QLabel(label)
        self.input_widget = widget
        if tooltip != '':
            self.input_widget.setToolTip(tooltip)
        self.input_widget.setObjectName(name)
        self.input_widget.setMinimumWidth(width)

        if vertical:
            self.layout = QVBoxLayout()
        else:
            self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        if is_widget_first:
            self.layout.addWidget(self.input_widget, 0, Qt.AlignVCenter)
            self.layout.addWidget(self.label, 0, Qt.AlignVCenter)
            self.layout.addStretch()
        else:
            self.layout.addWidget(self.label, 0, Qt.AlignVCenter)
            self.layout.addWidget(self.input_widget, 1, Qt.AlignVCenter)

        self.setLayout(self.layout)


class LabeledText(LabeledWidget):
    def __init__(self, parent=None, label='Font size:', text='',
                 width=40, name='', tooltip='', vertical=False):
        super().__init__(QLineEdit(),
                         parent=parent,
                         label=label,
                         width=width,
                         name=name,
                         tooltip=tooltip,
                         vertical=vertical)
        self.input_widget.setText(text)

    @property
    def text(self):
        return self.input_widget.text()

    @text.setter
    def text(self, text):
        self.input_widget.setText(text)


class LabeledComboBox(LabeledWidget):
    def __init__(self, parent=None, label='Font size:', values=(),
                 width=40, name='', tooltip='', vertical=False,
                 editable=False):
        super().__init__(QComboBox(),
                         parent=parent,
                         label=label,
                         width=width,
                         name=name,
                         tooltip=tooltip,
                         vertical=vertical)

        self.input_widget.setEditable(editable)
        self.input_widget.setDuplicatesEnabled(False)
        self._values = values
        self.input_widget.addItems(values)

    @property
    def text(self):
        return self.input_widget.currentText()

    @text.setter
    def text(self, text):
        if text not in self._values:
            self._values.append(text)
            self.input_widget.addItem(text)
        self.input_widget.setCurrentText(text)


class LabeledPath(QWidget):
    def __init__(self, parent=None, label='Font size:', text='',
                 width=40, name='', tooltip='', vertical=False,
                 open_dir=False):
        super().__init__(parent, flags=Qt.WindowFlags())
        self._open_dir = open_dir
        self.labeled_text = LabeledText(parent, label, text, width, name,
                                        tooltip, vertical)
        self.parent = parent
        self.button = QPushButton('Browse...')
        self.button.clicked.connect(self.open_dialog)
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.labeled_text, 0, Qt.AlignBottom)
        self.layout.addWidget(self.button, 0, Qt.AlignBottom)
        self.setLayout(self.layout)

    @property
    def text(self):
        return self.labeled_text.text

    @text.setter
    def text(self, text):
        self.labeled_text.text = text

    def open_dialog(self):
        if self._open_dir:
            path = QFileDialog.getExistingDirectory(self.parent,
                                                    caption='Open Directory',
                                                    options=QFileDialog.ShowDirsOnly)
            self.labeled_text.text = path
        else:
            path = QFileDialog.getOpenFileName(self.parent,
                                               caption='Open Directory',
                                               options=QFileDialog.Options())
            self.labeled_text.text = path[0]


class LabeledCheckBox(LabeledWidget):
    def __init__(self, parent=None, label='Font size:', name='', tooltip=''):
        super().__init__(QCheckBox(),
                         parent=parent,
                         label=label,
                         name=name,
                         tooltip=tooltip,
                         width=0,
                         is_widget_first=True)

    @property
    def is_checked(self):
        return self.input_widget.isChecked()
