from PyQt6.QtWidgets import QMainWindow, QFileDialog, QPushButton, QLabel, QVBoxLayout, QWidget
from icon_extractor import extract_icon
from model_renderer import render_3d_model

class Icon3DGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_generate = None
        self.button_select = None
        self.label = None
        self.file_path = None
        self.icon_path = None
        self.setWindowTitle('3D 图标生成器')
        self.setGeometry(100, 100, 800, 600)
        self.initui()

    def initui(self):
        layout = QVBoxLayout()

        self.label = QLabel('请选择一个文件（PNG、快捷方式、EXE）')
        layout.addWidget(self.label)

        self.button_select = QPushButton('选择文件')
        self.button_select.clicked.connect(self.open_file)
        layout.addWidget(self.button_select)

        self.button_generate = QPushButton('生成 3D 图标')
        self.button_generate.clicked.connect(self.generate_3d_icon)
        layout.addWidget(self.button_generate)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', '支持文件 (*.png *.lnk *.exe)')
        if file_path:
            self.label.setText(f'已选择文件: {file_path}')
            self.file_path=file_path

    def generate_3d_icon(self):
        if self.file_path:
            self.icon_path = extract_icon(self.file_path)
            print(self.file_path)
        if not hasattr(self, 'icon_path') or not self.icon_path:
            self.label.setText('请先选择一个有效的文件！')
            return
        render_3d_model(self.icon_path,100)