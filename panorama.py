import sys
import winsound

import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import QMainWindow, QPushButton, QLabel


class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파노라마 영상')
        self.setGeometry(200, 200, 700, 200)

        collectBtn = QPushButton('영상 수집', self)
        self.showBtn = QPushButton('영상 보기', self)
        self.stitchBtn = QPushButton('봉합', self)
        self.saveBtn = QPushButton('저장', self)
        quitBtn = QPushButton('나가기', self)
        self.label = QLabel('환영합니다!', self)

        collectBtn.setGeometry(10, 25, 100, 30)
        self.showBtn.setGeometry(110, 25, 100, 30)
        self.stitchBtn.setGeometry(210, 25, 100, 30)
        self.saveBtn.setGeometry(310, 25, 100, 30)
        quitBtn.setGeometry(450, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)

        self.showBtn.setEnabled(False)
        self.stitchBtn.setEnabled(False)
        self.saveBtn.setEnabled(False)

        collectBtn.clicked.connect(self.collectfn)
        self.showBtn.clicked.connect(self.collectfn)
        self.stitchBtn.clicked.connect(self.collectfn)
        self.saveBtn.clicked.connect(self.collectfn)
        quitBtn.clicked.connect(self.collectfn)