import sys
from PyQt6.QtWidgets import QApplication
from ui import Icon3DGenerator

def main():
    app = QApplication(sys.argv)
    window = Icon3DGenerator()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
