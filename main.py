import sys
from PyQt6.QtWidgets import QApplication
from app.ui import GAApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = GAApp()
    window.resize(700, 600)
    window.show()
    sys.exit(app.exec())
