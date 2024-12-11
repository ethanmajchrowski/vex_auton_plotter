import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QDial


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        button = QPushButton("Press Me!")
        # button.setCheckable(True)
        button.clicked.connect(self.the_button_was_clicked)

        self.dial = QDial()
        self.dial.valueChanged.connect(self.dial_change)

        # Set the central widget of the Window.
        self.setCentralWidget(self.dial)

    def the_button_was_clicked(self):
        print("Clicked!")
    
    def dial_change(self):
        v = self.dial.value()
        print((v/100)*255)
        self.dial.setStyleSheet(f"background-color: rgb({(v/100)*255}, {(v/100)*255}, {(v/100)*255});")

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()