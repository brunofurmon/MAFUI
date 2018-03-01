# Main WINDOW
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QWidget, QPushButton, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
class MainWindow(QMainWindow):
 
    def __init__(self):
        super().__init__()
        self.title = 'Multi-axial Fatigue calculator'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480

        # Cria um menu principal
        mainMenu = self.menuBar() 
        fileMenu = mainMenu.addMenu('File')
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        toolsMenu = mainMenu.addMenu('Tools')
        helpMenu = mainMenu.addMenu('Help')

        # Ação para carregar arquivo .csv
        loadFileButton = QAction(QIcon('open24.png'), 'Open File', self)
        loadFileButton.setShortcut('Ctrl+O')
        loadFileButton.setStatusTip('Open .CSV file')
        loadFileButton.triggered.connect(self.openFileNameDialog)
        fileMenu.addAction(loadFileButton)

        fileMenu.addSeparator()

        # Ação para sair do programa
        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        # Inicia a janela
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.show()
 
    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","CSV Files (*.csv)", options=options)
        if fileName:
            print(fileName)
