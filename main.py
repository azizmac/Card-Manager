import sys
from PyQt5.QtWidgets import QApplication, QInputDialog
from main_window import MainWindow
from PyQt5.QtCore import QDate, Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 