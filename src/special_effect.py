import sys

import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QComboBox,
    QLabel,
    QFileDialog,
    QApplication
)


class SpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('사진 특수 효과')
        self.setGeometry(200, 200, 800, 200)

        selectBtn = QPushButton('사진 선택', self)
        embossBtn = QPushButton('엠보싱', self)
        cartoonBtn = QPushButton('카툰', self)
        sketchBtn = QPushButton('연필 스케치', self)
        oilBtn = QPushButton('유화', self)
        saveBtn = QPushButton('저장하기', self)
        quitBtn = QPushButton('나가기', self)
        self.label = QLabel('환영합니다!', self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems([
            '엠보싱',
            '카툰',
            '연필 스케치(명암)',
            '연필 스케치(컬러)',
            '유화'
        ])

        selectBtn.setGeometry(10, 10, 100, 30)
        embossBtn.setGeometry(110, 10, 100, 30)
        cartoonBtn.setGeometry(210, 10, 100, 30)
        sketchBtn.setGeometry(310, 10, 100, 30)
        oilBtn.setGeometry(410, 10, 100, 30)
        saveBtn.setGeometry(510, 10, 100, 30)
        self.pickCombo.setGeometry(510, 40, 110, 30)
        quitBtn.setGeometry(620, 10, 100, 30)
        self.label.setGeometry(10, 40, 500, 170)

        selectBtn.clicked.connect(self.select_image)
        embossBtn.clicked.connect(self.embossing_effect)
        cartoonBtn.clicked.connect(self.cartoon_effect)
        sketchBtn.clicked.connect(self.sketch_effect)
        oilBtn.clicked.connect(self.oil_effect)
        saveBtn.clicked.connect(self.image_save)
        quitBtn.clicked.connect(self.app_quit)

    def select_image(self):
        fname = QFileDialog.getOpenFileName(self, '사진 읽기', './assets')
        self.img = cv.imread(fname[0])
        if self.img is None: self.label.setText('파일을 찾을 수 없습니다.')

        cv.imshow('Painting', self.img)

    def embossing_effect(self):
        femboss = np.array([[-1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0]])

        gray_img = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        gray16_img = np.int16(gray_img)
        self.emboss_img = np.uint8(np.clip(cv.filter2D(gray16_img, -1, femboss) + 128, 0, 255))

        cv.imshow('Emboss', self.emboss_img)

    def cartoon_effect(self):
        self.cartoon_img = cv.stylization(self.img, sigma_s=60, sigma_r=0.45)

        cv.imshow('Cartoon', self.cartoon_img)

    def sketch_effect(self):
        self.sketch_img = cv.pencilSketch(self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02)

        cv.imshow('Pencil sketch(gray)', self.sketch_img[0])
        cv.imshow('Pencil sketch(color)', self.sketch_img[1])

    def oil_effect(self):
        self.oil_img = cv.xphoto.oilPainting(self.img, 10, 1, cv.COLOR_BGR2Lab)

        cv.imshow('Oil painting', self.oil_img)

    def image_save(self):
        save_dir = './outputs'

        fname, _ = QFileDialog.getSaveFileName(self, '파일 저장', save_dir)
        if len(fname.split(".")) == 1: fname = f'{fname}.png'

        i = self.pickCombo.currentIndex()
        if i == 0: cv.imwrite(fname, self.emboss_img)
        elif i == 1: cv.imwrite(fname, self.cartoon_img)
        elif i == 2: cv.imwrite(fname, self.sketch_img[0])
        elif i == 3: cv.imwrite(fname, self.sketch_img[1])
        elif i == 4: cv.imwrite(fname, self.oil_img)

    def app_quit(self):
        cv.destroyAllWindows()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SpecialEffect()
    win.show()
    app.exec()