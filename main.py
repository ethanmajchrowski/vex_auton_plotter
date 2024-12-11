import sys
import PyQt6.QtWidgets as qwidget

from mainwindow import Ui_MainWindow

sequence = ["hello!", "i am a robot"]

class MainWindow(qwidget.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.listWidget.addItems(sequence)

        # on selection change, run sequence select
        self.listWidget.itemSelectionChanged.connect(self.sequence_select)
    
    def sequence_select(self):
        # Get the currently selected item's text
        print(self.listWidget.selectedItems()[0].text())

app = qwidget.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
