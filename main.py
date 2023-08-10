import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtWidgets
from sidebar_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.full_menu_widget.hide()

        self.ui.stackedWidget.setCurrentIndex(0)


        ## Connect stackedWidget's currentChanged signal to on_stackedWidget_currentChanged slot
        self.ui.stackedWidget.currentChanged.connect(self.on_stackedWidget_currentChanged)

        ## Connect QPushButton toggled signals to respective slots


    ## Function for searching

    ## Change QPushButton Checkable status when stackedWidget index changed

    def on_stackedWidget_currentChanged(self, index):
        btn_list = self.ui.icon_only_widget.findChildren(QPushButton) + self.ui.full_menu_widget.findChildren(QPushButton)

        for btn in btn_list:
            if index in [7, 8]:
                btn.setAutoExclusive(False)
                btn.setChecked(False)
            else:
                btn.setAutoExclusive(True)

    ## functions for changing menu page


    def on_option1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(4)
        self.ui.returnButton.clicked.connect(self.ui.on_returnButton_v1)

    def on_home_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.returnButton.clicked.connect(self.ui.on_returnButton_v1)


    def on_home_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(0)
        self.ui.returnButton.clicked.connect(self.ui.on_returnButton_v1)


    def on_folder_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def on_folder_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(1)


    def on_picture_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)


    def on_picture_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(2)


    def on_data_btn_1_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)

    def on_data_btn_2_toggled(self):
        self.ui.stackedWidget.setCurrentIndex(3)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
