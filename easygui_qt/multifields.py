import sys
from collections import OrderedDict
from PyQt4 import QtGui, QtCore

if sys.version_info >= (3,):
    unicode = str

class MultipleFieldsDialog(QtGui.QDialog):
    """Dialog with multiple fields stored in a dict, with the label
       being the key and the entry being the corresponding value"""
    def __init__(self, labels=None, title="Demo", masks=None, parent=None,
                 verification=None):
        super(MultipleFieldsDialog, self).__init__(None,
                         QtCore.Qt.WindowSystemMenuHint |
                         QtCore.Qt.WindowTitleHint)

        if parent is None:
            raise Exception("Parent must be a valid object")

        if verification == "demo":
            self.verification = self.demo_verification
        else:
            self.verification = verification

        self.parent = parent
        self.parent.o_dict = OrderedDict()
        self.setWindowTitle(title)

        # set up a special case for quick demo
        if labels is None:
            labels = ["Regular field", "Masked field"]
            masks = [False, True]
            self.setWindowTitle("MultipleFieldsDialog demo")

        if masks is not None:
            assert len(masks) == len(labels)

        layout = QtGui.QGridLayout()
        layout.setColumnStretch(1, 1)
        layout.setColumnMinimumWidth(1, 250)

        self._labels_ = []
        self.fields = []
        for index, choice in enumerate(labels):
            self._labels_.append(QtGui.QLabel())
            self._labels_[index].setText(choice)
            self.fields.append(QtGui.QLineEdit())
            self.fields[index].setText('')
            self.parent.o_dict[choice] = ''
            if masks is not None and masks[index]:
                self.fields[index].setEchoMode(QtGui.QLineEdit.Password)
            layout.addWidget(self._labels_[index], index, 0)
            layout.addWidget(self.fields[index], index, 1)

        button_box = QtGui.QDialogButtonBox()
        confirm_button = button_box.addButton(QtGui.QDialogButtonBox.Ok)
        layout.addWidget(button_box, index+1, 1)
        confirm_button.clicked.connect(self.confirm)
        self.setLayout(layout)
        self.setWindowTitle(title)
        self.show()
        self.raise_()

    def confirm(self):
        """Selection completed, set the value and close"""
        o_dict = self.parent.o_dict
        for index, item in enumerate(self._labels_):
            o_dict[item.text()] = unicode(self.fields[index].text())
        if self.verification is None:   # no verification
            self.close()
        elif self.verification(self) is None:    # no error raised
            self.close()
        else:
            for index, item in enumerate(self._labels_):
                o_dict[item.text()] = ''
            self.close()

    def demo_verification(self, dummy=None):
        """Silly demo of a verification function.  It requires that the
           original password be "password" and that the two new passwords
           be identical.
        """
        if dummy is not None:
            dummy = self
        message = None
        o_dict = self.parent.o_dict
        if o_dict[self._labels_[0].text()] != "password":
            message = ("Original password does not match expected value " +
                       "[Hint: it's 'password']")
            self.show_warning(message)
        elif o_dict[self._labels_[1].text()] != o_dict[self._labels_[2].text()]:
            message = "New password values must be identical."
            self.show_warning(message)
        return message

    def show_warning(self, message):
        QtGui.QMessageBox.critical(None, ' ', message)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    class Parent:
        pass
    parent = Parent()
    dialog = MultipleFieldsDialog(parent=parent)
    dialog.exec_()
    print(parent.o_dict)