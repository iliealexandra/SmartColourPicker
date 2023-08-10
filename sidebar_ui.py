import os
import csv
import subprocess
import sys
from random import randint
from PyQt5 import QtCore, QtGui, QtWidgets
from extract_colour import process_picture
import results_pictures
import colour_search
import traceback


from PIL import ImageQt



class ColourPaletteSelect(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.palette = [QtGui.QColor() for _ in range(5)]
        self.init_ui()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()
        name_layout = QtWidgets.QHBoxLayout()
        palette_layout = QtWidgets.QHBoxLayout()
        btn_layout = QtWidgets.QHBoxLayout()
        option_layout = QtWidgets.QHBoxLayout()

        self.setLayout(layout)

        layout.addLayout(palette_layout)
        layout.addLayout(name_layout)
        layout.addLayout(btn_layout)
        layout.addLayout(option_layout)

        name_label = QtWidgets.QLabel('Enter Palette name:')
        self.error_msg = QtWidgets.QLabel()
        self.name_enter = QtWidgets.QLineEdit()
        regex_pattern = '[A-Za-z0-9]+'
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(regex_pattern))
        self.name_enter.setValidator(validator)

        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_enter)
        name_layout.addWidget(self.error_msg)

        self.colour_palette = []
        for i in range(5):
            label = QtWidgets.QLabel()
            self.colour_palette.append(label)
            palette_layout.addWidget(label)

        for i in range(5):
            button = QtWidgets.QPushButton(f"Select Color {i+1}")
            button.clicked.connect(lambda checked, i=i: self.open_color_dialog(i))
            btn_layout.addWidget(button)

        self.generate_button = QtWidgets.QPushButton('Generate Palette')
        self.generate_button.clicked.connect(self.generate)
        option_layout.addWidget(self.generate_button)

        self.csv_button = QtWidgets.QPushButton('Save')
        self.csv_button.clicked.connect(self.save_colours)
        option_layout.addWidget(self.csv_button)

        self.result_button = QtWidgets.QPushButton('View Results')
        option_layout.addWidget(self.result_button)

    def generate(self):
        for i in range(5):
            r = randint(0, 255)
            g = randint(0, 255)
            b = randint(0, 255)
            colour = QtGui.QColor(r, g, b)
            self.palette[i] = colour
        self.update_palette()

    def open_color_dialog(self,index):
        colour = QtWidgets.QColorDialog.getColor()
        if colour.isValid():
            self.palette[index] = colour
            self.update_palette()

    def update_palette(self):
        for i, colour_label in enumerate(self.colour_palette):
            colour = self.palette[i]
            colour_label.setText(f"Color {i+1}: {colour.name()}")
            colour_label.setStyleSheet(f"background-color: {colour.name()}; color: {colour.name()}")

    def save_colours(self):


        palette_name = self.name_enter.text()
        colour_code = []

        for i, colour in enumerate(self.palette):
            colour_code.append(colour.name())  # Append the color name to colour_code list

        if palette_name:
            self.result_button.setVisible(True)
            self.csv_button.setVisible(False)
            self.generate_button.setVisible(False)
            with open('Data/search_data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([palette_name] + colour_code)

        if not palette_name:
            self.error_msg.setText('!Enter the colour palette name!')
        else:
            self.error_msg.clear()


class ImageLabel(QtWidgets.QLabel):
    clicked = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setText('\n\n Drop Picture Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')
        self.setAcceptDrops(True)


    def setPixmap(self, image):
        super().setPixmap(image)

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        event.ignore()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.LeftButton:
            self.emitClickEvent()

    def emitClickEvent(self):
        self.clicked.emit()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage or event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()

            self.set_image(file_path)

            event.accept()

        elif event.mimeData().hasUrls():
            url = event.mimeData().urls()[0]
            if url.isLocalFile():
                file_path = url.toLocalFile()

                self.set_image(file_path)

                event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        pixmap = QtGui.QPixmap(file_path)
        pixmap = pixmap.scaled(self.size() , QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(pixmap)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setFixedSize(800 , 600)
        window_icon = QtGui.QIcon()
        window_icon.addFile("Gui_elements/SCP_ICON.png", QtCore.QSize(), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(window_icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.logo = QtWidgets.QLabel(MainWindow)
        self.logo.setObjectName(u"label")
        self.logo.setGeometry(QtCore.QRect(300, 0, 350, 61))
        font = QtGui.QFont()
        font.setFamily(u"Modern")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.logo.setFont(font)

        self.icon_only_widget = QtWidgets.QWidget(self.centralwidget)

        self.icon_only_widget.setStyleSheet("background-color: #92A08A;")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.icon_only_widget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.home_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.home_btn_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Gui_elements/icons/house-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon.addPixmap(QtGui.QPixmap("Gui_elements/icons/house-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.home_btn_1.setIcon(icon)
        self.home_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.home_btn_1.setCheckable(True)
        self.home_btn_1.setAutoExclusive(False)
        self.home_btn_1.setObjectName("home_btn_1")
        self.verticalLayout.addWidget(self.home_btn_1)
        self.folder_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.folder_btn_1.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Gui_elements/icons/folder-3-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap("Gui_elements/icons/folder-3-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.folder_btn_1.setIcon(icon1)
        self.folder_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.folder_btn_1.setCheckable(True)
        self.folder_btn_1.setAutoExclusive(True)
        self.verticalLayout.addWidget(self.folder_btn_1)
        self.picture_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.picture_btn_1.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Gui_elements/icons/picture-2-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon2.addPixmap(QtGui.QPixmap("Gui_elements/icons/picture-2-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.picture_btn_1.setIcon(icon2)
        self.picture_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.picture_btn_1.setCheckable(True)
        self.picture_btn_1.setAutoExclusive(True)
        self.picture_btn_1.setObjectName("picture_btn_1")
        self.verticalLayout.addWidget(self.picture_btn_1)
        self.data_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.data_btn_1.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Gui_elements/icons/text-file-3-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap("Gui_elements/icons/text-file-3-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.data_btn_1.setIcon(icon3)
        self.data_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.data_btn_1.setCheckable(True)
        self.data_btn_1.setAutoExclusive(True)
        self.data_btn_1.setObjectName("data_btn_1")
        self.verticalLayout.addWidget(self.data_btn_1)


        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 375, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.exit_btn_1 = QtWidgets.QPushButton(self.icon_only_widget)
        self.exit_btn_1.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Gui_elements/icons/close-window-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_btn_1.setIcon(icon5)
        self.exit_btn_1.setIconSize(QtCore.QSize(20, 20))
        self.exit_btn_1.setObjectName("exit_btn_1")
        self.verticalLayout_3.addWidget(self.exit_btn_1)
        self.gridLayout.addWidget(self.icon_only_widget, 0, 0, 1, 1)
        self.full_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.full_menu_widget.setObjectName("full_menu_widget")
        self.full_menu_widget.setStyleSheet("background-color: #92A08A;")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.full_menu_widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.logo_label_2 = QtWidgets.QLabel(self.full_menu_widget)
        self.logo_label_2.setMinimumSize(QtCore.QSize(40, 40))
        self.logo_label_2.setMaximumSize(QtCore.QSize(40, 40))
        self.logo_label_2.setText("")
        self.logo_label_2.setPixmap(QtGui.QPixmap("Gui_elements/icons/house-24.png"))
        self.logo_label_2.setScaledContents(True)
        self.logo_label_2.setObjectName("logo_label_2")
        self.horizontalLayout_2.addWidget(self.logo_label_2)
        self.logo_label_3 = QtWidgets.QLabel(self.full_menu_widget)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.logo_label_3.setFont(font)
        self.logo_label_3.setObjectName("logo_label_3")
        self.horizontalLayout_2.addWidget(self.logo_label_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.home_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.home_btn_2.setIcon(icon)
        self.home_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.home_btn_2.setCheckable(True)
        self.home_btn_2.setAutoExclusive(True)
        self.home_btn_2.setObjectName("home_btn_2")
        self.verticalLayout_2.addWidget(self.home_btn_2)
        self.folder_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.folder_btn_2.setIcon(icon1)
        self.folder_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.folder_btn_2.setCheckable(True)
        self.folder_btn_2.setAutoExclusive(True)
        self.folder_btn_2.setObjectName("folder_btn_2")
        self.verticalLayout_2.addWidget(self.folder_btn_2)
        self.picture_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.picture_btn_2.setIcon(icon2)
        self.picture_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.picture_btn_2.setCheckable(True)
        self.picture_btn_2.setAutoExclusive(True)
        self.picture_btn_2.setObjectName("picture_btn_2")
        self.verticalLayout_2.addWidget(self.picture_btn_2)
        self.data_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.data_btn_2.setIcon(icon3)
        self.data_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.data_btn_2.setCheckable(True)
        self.data_btn_2.setAutoExclusive(True)
        self.data_btn_2.setObjectName("data_btn_2")
        self.verticalLayout_2.addWidget(self.data_btn_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 373, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem1)



        self.exit_btn_2 = QtWidgets.QPushButton(self.full_menu_widget)
        self.exit_btn_2.setIcon(icon5)
        self.exit_btn_2.setIconSize(QtCore.QSize(14, 14))
        self.exit_btn_2.setObjectName("exit_btn_2")
        self.verticalLayout_4.addWidget(self.exit_btn_2)

        self.gridLayout.addWidget(self.full_menu_widget, 0, 1, 1, 1)
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.widget = QtWidgets.QWidget(self.widget_3)
        self.widget.setMinimumSize(QtCore.QSize(0, 40))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 9, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.change_btn = QtWidgets.QPushButton(self.widget)
        self.change_btn.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("Gui_elements/icons/menu-4-24.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.change_btn.setIcon(icon6)
        self.change_btn.setIconSize(QtCore.QSize(14, 14))
        self.change_btn.setCheckable(True)
        self.change_btn.setObjectName("change_btn")
        self.horizontalLayout_4.addWidget(self.change_btn)

        spacerItem2 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.horizontalLayout_4.addLayout(self.horizontalLayout)
        spacerItem3 = QtWidgets.QSpacerItem(236, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)

        self.verticalLayout_5.addWidget(self.widget)
        self.stackedWidget = QtWidgets.QStackedWidget(self.widget_3)
        self.stackedWidget.setObjectName("stackedWidget")
        #pagina initiala a aplicatiei/the home page
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")

        self.home_page_layout = QtWidgets.QHBoxLayout()
        self.page.setLayout(self.home_page_layout)
        self.opt1_layout = QtWidgets.QVBoxLayout()
        self.opt2_layout = QtWidgets.QVBoxLayout()
        self.home_page_layout.addLayout(self.opt1_layout)
        self.home_page_layout.addLayout(self.opt2_layout)
        self.label_1 = QtWidgets.QLabel("Find the closest picture colour palette-wise.\nAnalyse pictures by their colour palettes.\nThe colour palettes contain the five primary dominant distinct colours.\nThe user can choose the colour tolerance of the colour palettes \nfor a better visual output colour data representation.")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setStyleSheet('''
            QLabel{
                border: 4px  groove  grey
            }
        ''')
        self.opt1_layout.addWidget(self.label_1)
        self.option1 = QtWidgets.QPushButton()
        self.opt1_layout.addWidget(self.option1)
        self.option1.setObjectName("option1")
        self.option1.setGeometry(QtCore.QRect(30, 80, 111, 51))
        self.option1.setCheckable(True)
        self.option1.setAutoExclusive(True)
        self.option2 = QtWidgets.QPushButton()

        self.label_2 = QtWidgets.QLabel(
            "Create or generate a colour palette.\n Use the created/generated palette to get the \n closest picture colour palette match.")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setStyleSheet('''
                   QLabel{
                       border: 4px  groove  grey
                   }
               ''')
        self.opt2_layout.addWidget(self.label_2)
        self.opt2_layout.addWidget(self.option2)
        self.option2.setObjectName("option2")
        self.option2.setCheckable(True)
        self.option2.setAutoExclusive(False)
        self.option2.setGeometry(QtCore.QRect(30, 140, 110, 51))
        self.stackedWidget.addWidget(self.page)
        #cand apasam in side bar pe butonul cu iconita cu un folder ,deschide folderele proiectului

        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.layout_3 = QtWidgets.QVBoxLayout(self.page_2)
        self.layout_3.setObjectName("layout_3")
        folder_view=QtWidgets.QFileSystemModel()
        project_dir="C:/Users/alexa/PycharmProjects/GUI_SCP"
        folder_view.setRootPath(project_dir)
        folder_tree_view=QtWidgets.QTreeView()
        folder_tree_view.setModel(folder_view)
        folder_tree_view.setRootIndex(folder_view.index(project_dir))
        folder_tree_view.setHeaderHidden(True)
        folder_tree_view.setSortingEnabled(True)
        folder_tree_view.sortByColumn(0, QtCore.Qt.AscendingOrder)
        self.layout_3.addWidget(folder_tree_view)
        self.page_2.setLayout(self.layout_3)
        self.stackedWidget.addWidget(self.page_2)
        # pagina pentru vederea imaginilor disponibile in proiect
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.layout_4 = QtWidgets.QGridLayout(self.page_3)
        self.layout_4.setObjectName("layout_4")
        self.pics_tab = QtWidgets.QTabWidget()
        self.pic_folders = ['test_pictures', 'images']
        for folder in self.pic_folders:
            self.pics_tree_view = QtWidgets.QTreeView()  # Create a new QTreeView instance for each folder
            self.pic_tab_model = QtWidgets.QFileSystemModel()
            self.pic_tab_model.setRootPath(folder)
            self.pics_tree_view.setModel(self.pic_tab_model)
            self.pics_tree_view.setRootIndex(self.pic_tab_model.index(folder))
            self.pics_tree_view.doubleClicked.connect(self.open_image_file)
            self.pics_tab.addTab(self.pics_tree_view, folder)

        self.layout_4.addWidget(self.pics_tab)
        self.stackedWidget.addWidget(self.page_3)

        #pentru vederea datelor din fisierele csv
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.layout_5 = QtWidgets.QGridLayout(self.page_4)
        tables_tabs = QtWidgets.QTabWidget()
        csv_files = ['Data/colour_data.csv', 'Data/search_data.csv', 'Data/search_results.csv']
        for csv_file in csv_files:
            tableView = QtWidgets.QTableView()
            with open(csv_file, 'r') as file:
                table_data = csv.reader(file)
                table_model = QtGui.QStandardItemModel()

                for row_table_data in table_data:
                    items = [QtGui.QStandardItem(field) for field in row_table_data]
                    table_model.appendRow(items)

            tableView.setModel(table_model)
            tableView.resizeColumnsToContents()
            tableView.setEditTriggers(QtWidgets.QTableView.NoEditTriggers)
            tab = QtWidgets.QWidget()
            tab_layout = QtWidgets.QVBoxLayout(tab)
            tab_layout.addWidget(tableView)
            tab.setLayout(tab_layout)

            tables_tabs.addTab(tab, csv_file)

        self.layout_5.addWidget(tables_tabs)  # Add tables_tabs to the layout
        self.page_4.setLayout(self.layout_5)  # Set the layout for page_4
        self.stackedWidget.addWidget(self.page_4)

        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.page_5.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.boxlayout = QtWidgets.QVBoxLayout(self.page_5)
        self.photoViewer = ImageLabel()
        self.pic_name=QtWidgets.QLineEdit()
        regex_pattern = '[A-Za-z0-9]+'
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(regex_pattern))
        self.pic_name.setValidator(validator)
        self.tol=QtWidgets.QLineEdit()
        number_regex = r'^[1-9]\d*$'
        nr_validator = QtGui.QRegExpValidator(QtCore.QRegExp(number_regex))
        self.tol.setValidator(nr_validator)
        self.label_11 = QtWidgets.QLabel('Enter picture name:')
        self.label_12 = QtWidgets.QLabel(' Colour Tolerance:')
        self.saveButton = QtWidgets.QPushButton('Save Image')
        self.tol.setVisible(False)
        self.label_12.setVisible(False)
        self.saveButton.clicked.connect(self.save_picture)

        self.boxlayout.addWidget(self.photoViewer)

        self.returnButton = QtWidgets.QPushButton('Return')
        self.returnButton.setObjectName('returnButton')
        self.analyzeButton = QtWidgets.QPushButton('Analyse')
        self.analyzeButton.setVisible(False)
        self.searchButton = QtWidgets.QPushButton('Search')
        self.searchButton.setObjectName('searchButton')
        self.searchButton.setVisible(False)
        self.data_layout = QtWidgets.QHBoxLayout()
        self.pictype = QtWidgets.QComboBox()
        self.pictype.addItems([".png", ".jpg", ".jpeg"])
        self.error = QtWidgets.QLabel()
        self.error.setFixedSize(250,30)
        self.error_layout=QtWidgets.QHBoxLayout()


        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.addWidget(self.returnButton)
        self.btn_layout.addWidget(self.saveButton)
        self.btn_layout.addWidget(self.analyzeButton)
        self.btn_layout.addWidget(self.searchButton)

        self.data_layout.addWidget(self.label_11)
        self.data_layout.addWidget(self.pic_name)
        self.data_layout.addWidget(self.pictype)
        self.data_layout.addWidget(self.label_12)
        self.data_layout.addWidget(self.tol)

        self.error_layout.addWidget(self.error)

        self.boxlayout.addLayout(self.data_layout)
        self.boxlayout.addLayout(self.error_layout)
        self.boxlayout.addLayout(self.btn_layout)

        self.stackedWidget.addWidget(self.page_5)
        self.verticalLayout_5.addWidget(self.stackedWidget)
        self.gridLayout.addWidget(self.widget_3, 0, 2, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(8)
        self.photoViewer.clicked.connect(self.onLabelClicked)
        self.analyzeButton.clicked.connect(self.analyze)
        self.returnButton.clicked.connect(self.on_returnButton_v1)
        self.searchButton.clicked.connect(self.on_searchButton_toggled)
        self.option2.clicked.connect(self.on_option2_toggled)

        self.change_btn.toggled['bool'].connect(self.icon_only_widget.setHidden)  # type: ignore
        self.change_btn.toggled['bool'].connect(self.full_menu_widget.setVisible)  # type: ignore
        self.home_btn_1.toggled['bool'].connect(self.home_btn_2.setChecked)  # type: ignore
        self.folder_btn_1.toggled['bool'].connect(self.folder_btn_2.setChecked)  # type: ignore
        self.picture_btn_1.toggled['bool'].connect(self.picture_btn_2.setChecked)  # type: ignore
        self.data_btn_1.toggled['bool'].connect(self.data_btn_2.setChecked)  # type: ignore

        self.home_btn_2.toggled['bool'].connect(self.home_btn_1.setChecked)  # type: ignore
        self.folder_btn_2.toggled['bool'].connect(self.folder_btn_1.setChecked)  # type: ignore
        self.picture_btn_2.toggled['bool'].connect(self.picture_btn_1.setChecked)  # type: ignore
        self.data_btn_2.toggled['bool'].connect(self.data_btn_1.setChecked)  # type: ignore
        self.exit_btn_2.clicked.connect(MainWindow.close)  # type: ignore
        self.exit_btn_1.clicked.connect(MainWindow.close)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def open_image_file(self, index):
        file_path = self.pic_tab_model.fileInfo(index).absoluteFilePath()
        if os.path.isfile(file_path):  # Check if the selected item is a file
            if file_path.endswith((".jpg", ".jpeg", ".png", ".gif")):  # Check if the file is an image
                QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(file_path))

    def save_picture(self):

        picture = ImageQt.fromqpixmap(self.photoViewer.pixmap())

        picture_name = self.pic_name.text()
        picture_type = self.pictype.currentText()
        picture_dir = 'test_pictures'
        save_path = os.path.join(picture_dir, picture_name + picture_type)

        if picture is not None:
            if picture_name:
                picture.save(save_path)
                self.analyzeButton.setVisible(True)
                self.saveButton.setVisible(False)
                self.tol.setVisible(True)
                self.label_12.setVisible(True)
                self.error.clear()  # Clear the error message
            else:
                self.error.setText('!Enter the image name!')
        else:
            self.error.clear()  # Clear the error message

    def analyze(self):
        text_tolerance = self.tol.text()
        if text_tolerance:
            colour_tolerance = int(text_tolerance)
            picture_name = self.pic_name.text()
            picture_type = self.pictype.currentText()
            picture_dir = 'test_pictures'
            save_path = os.path.join(picture_dir, picture_name + picture_type)
            process_picture(save_path,colour_tolerance)
            with open('Data/search_data.csv', newline='') as file:
                reader = csv.reader(file)
                colour_data = list(reader)
            row = colour_data[-1]
            colours = row[1:]
            colours_count = len(colours)
            if colours_count == 5 :
                self.colour_widget = QtWidgets.QWidget()
                self.colour_widget.setFixedSize(800, 50)
                self.palette_layout = QtWidgets.QHBoxLayout()



                for colour in colours:
                    colour_label = QtWidgets.QLabel()
                    colour_label.setStyleSheet(f"background-color:{colour};")
                    colour_label.setFixedSize(130, 30)
                    self.palette_layout.addWidget(colour_label)

                self.colour_widget.setLayout(self.palette_layout)

                self.boxlayout.addWidget(self.colour_widget)
                self.returnButton.clicked.connect(self.on_returnButton_v2)
                self.analyzeButton.setVisible(False)
                self.returnButton.setVisible(False)
                self.searchButton.setVisible(True)
                self.error.clear()
            else:
                self.error.setText("Decrease the value of the colour tolerance!")
        else:
            self.error.setText("Enter the tolerance number!")

    def on_returnButton_v1(self):

        self.stackedWidget.setCurrentIndex(0)
        self.pic_name.clear()
        self.tol.clear()
        self.tol.setVisible(False)
        self.label_12.setVisible(False)
        self.photoViewer.setText('\n\n Drop Picture Here \n\n')
        self.searchButton.setVisible(False)
        self.analyzeButton.setVisible(False)
        self.saveButton.setVisible(True)
        self.colour_widget = None


    def on_returnButton_v2(self):

        self.stackedWidget.setCurrentIndex(0)
        self.pic_name.clear()
        self.tol.clear()
        self.tol.setVisible(False)
        self.label_12.setVisible(False)
        self.photoViewer.setText('\n\n Drop Picture Here \n\n')
        self.searchButton.setVisible(False)
        self.analyzeButton.setVisible(False)
        self.saveButton.setVisible(True)
        if self.colour_widget:
            self.colour_widget.deleteLater()
            self.colour_widget = None  # Set the widget reference to Non

    def on_searchButton_toggled(self):
        self.colour_widget.deleteLater()
        self.returnButton.setVisible(True)
        self.returnButton.clicked.connect(self.on_returnButton_v1)
        self.page_6 = QtWidgets.QWidget(self.stackedWidget)
        self.page_layout = QtWidgets.QHBoxLayout(self.page_6)
        self.search_layout = QtWidgets.QVBoxLayout()
        self.palette_layout = QtWidgets.QHBoxLayout()
        self.results_layout = QtWidgets.QGridLayout()
        self.viewbtn = QtWidgets.QPushButton('View Results')
        self.returnbtn = QtWidgets.QPushButton('Return')
        self.returnbtn.clicked.connect(self.on_returnButton_v1)
        self.viewbtn.clicked.connect(self.search_results)
        self.search_layout.addWidget(self.viewbtn)
        self.search_layout.addWidget(self.returnbtn)
        self.searched_image = QtWidgets.QLabel()
        src_pixmap = self.photoViewer.pixmap()
        src_pixmap = src_pixmap.scaled(150, 200)
        self.searched_image.setPixmap(src_pixmap)
        self.search_layout.addWidget(self.searched_image)
        with open('Data\search_data.csv', newline='') as file:
            reader = csv.reader(file)
            colour_data = list(reader)
        row = colour_data[-1]
        colours = row[1:]
        for colour in colours:
            colour_label = QtWidgets.QLabel()
            colour_label.setStyleSheet(f"background-color:{colour};")
            colour_label.setFixedSize(30, 30)
            self.palette_layout.addWidget(colour_label)

        self.search_layout.addLayout(self.palette_layout)
        self.page_layout.addLayout(self.search_layout)
        self.page_layout.addLayout(self.results_layout)
        self.stackedWidget.addWidget(self.page_6)
        self.stackedWidget.setCurrentWidget(self.page_6)

    def search_results(self):
        self.viewbtn.setVisible(False)

        colour_search.colour_search_results()
        paths = results_pictures.create_path('Data\search_results.csv')
        self.res_layout = QtWidgets.QGridLayout()

        row_count = 0
        col_count = 0
        with open('Data/search_results.csv', 'r') as file:
            reader = csv.DictReader(file)
            colour_data = list(reader)  # Read all rows of color data into a list

        for path, row in zip(paths, colour_data):  # Iterate over paths and corresponding rows
            image_label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(path)
            pixmap = pixmap.scaled(170, 220)  # Adjust the size of the displayed image as needed
            image_label.setPixmap(pixmap)
            self.res_layout.addWidget(image_label, row_count, col_count)
            colours = [row[f'Colour #{i}'] for i in range(1, 6)]  # Get color values from the current row
            palette_layout = QtWidgets.QHBoxLayout()
            for colour in colours:
                colour_label = QtWidgets.QLabel()
                colour_label.setStyleSheet(f"background-color:{colour};")
                colour_label.setFixedSize(20, 20)
                palette_layout.addWidget(colour_label)
            self.res_layout.addLayout(palette_layout, row_count + 1, col_count)
            col_count += 1
            if col_count == 4:
                col_count = 0
                row_count += 2
        self.results_layout.addLayout(self.res_layout, row_count, col_count)

    def on_option2_toggled(self):
        self.palette_maker_widget = ColourPaletteSelect()
        self.pmw_layout = QtWidgets.QVBoxLayout()
        self.return_home = QtWidgets.QPushButton('Return')
        self.palette_maker_widget.result_button.clicked.connect(self.analyze_palette)
        self.palette_maker_widget.generate_button.setVisible(True)
        self.palette_maker_widget.result_button.setVisible(False)
        spacer_1 = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_2 = QtWidgets.QSpacerItem(50, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.pmw_layout.addWidget(self.palette_maker_widget)

        self.second_layout = QtWidgets.QHBoxLayout()
        self.second_layout.addItem(spacer_1)
        self.second_layout.addWidget(self.return_home)

        self.second_layout.addItem(spacer_2)

        self.return_home.clicked.connect(self.on_returnButton_v3)
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setLayout(self.pmw_layout)
        self.pmw_layout.addLayout(self.second_layout)

        self.stackedWidget.addWidget(self.page_7)
        self.stackedWidget.setCurrentWidget(self.page_7)

    def on_returnButton_v3(self):
        self.stackedWidget.setCurrentIndex(0)


    def analyze_palette(self):
       try:
            self.page_8 = QtWidgets.QWidget()
            self.stackedWidget.addWidget(self.page_8)
            self.stackedWidget.setCurrentWidget(self.page_8)
            plt_res_layout = QtWidgets.QVBoxLayout()
            self.page_8.setLayout(plt_res_layout)
            colour_search.colour_search_results()
            paths = results_pictures.create_path('Data\search_results.csv')
            search_palette=QtWidgets.QHBoxLayout()
            with open('Data\search_data.csv', newline='') as file:
                reader = csv.reader(file)
                colour_data = list(reader)
            row = colour_data[-1]
            colours = row[1:]
            for colour in colours:
                colour_label = QtWidgets.QLabel()
                colour_label.setStyleSheet(f"background-color:{colour};")
                colour_label.setFixedSize(150, 30)
                search_palette.addWidget(colour_label)

            row_count = 0
            col_count = 0
            result_layout=QtWidgets.QGridLayout()
            with open('Data/search_results.csv', 'r') as file:
                reader = csv.DictReader(file)
                colour_data = list(reader)
            for path, row in zip(paths, colour_data):  # Iterate over paths and corresponding rows
                image_label = QtWidgets.QLabel()
                pixmap = QtGui.QPixmap(path)
                pixmap = pixmap.scaled(150, 200)  # Adjust the size of the displayed image as needed
                image_label.setPixmap(pixmap)
                result_layout.addWidget(image_label, row_count, col_count)

                colours = [row[f'Colour #{i}'] for i in range(1, 6)]  # Get color values from the current row

                palette_layout = QtWidgets.QHBoxLayout()
                for colour in colours:
                    colour_label = QtWidgets.QLabel()
                    colour_label.setStyleSheet(f"background-color:{colour};")
                    colour_label.setFixedSize(20, 20)
                    palette_layout.addWidget(colour_label)
                result_layout.addLayout(palette_layout, row_count + 1, col_count)

                col_count += 1
                if col_count == 4:
                    col_count = 0
                    row_count += 2

            return2_btn = QtWidgets.QPushButton('Return')
            return2_btn.clicked.connect(self.on_returnButton_v3)

            plt_res_layout.addLayout(search_palette)
            plt_res_layout.addLayout(result_layout)
            plt_res_layout.addWidget(return2_btn)
       except Exception as e:
           traceback.print_exc()


    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if not self.photoViewer.pixmap():
            return
        self.photoViewer.set_image(self.photoViewer.pixmap().cacheKey())

    def onLabelClicked(self):
        folder_path = "C:/Users/alexa/Pictures/Saved Pictures"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(folder_path))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Smart Colour Picker"))
        self.option1.setText(_translate("MainWindow", "Analyse by picture"))
        self.option2.setText(_translate("MainWindow", "Analyse by palette"))
        self.logo.setText(_translate("MainWindow", u"Smart Colour Picker"))
        self.logo_label_3.setText(_translate("MainWindow", "Home Menu"))
        self.home_btn_2.setText(_translate("MainWindow", "Home"))
        self.folder_btn_2.setText(_translate("MainWindow", "Open Folders"))
        self.picture_btn_2.setText(_translate("MainWindow", "View Pictures"))
        self.data_btn_2.setText(_translate("MainWindow", "View Data Files"))

        self.exit_btn_2.setText(_translate("MainWindow", "Exit"))



