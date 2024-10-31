import os
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
        self.setWindowTitle('이미지 특수 효과')
        self.setGeometry(200, 200, 600, 100)

        selectBtn = QPushButton('이미지 선택', self)
        self.saveBtn = QPushButton('저장하기', self)
        quitBtn = QPushButton('나가기', self)
        self.label = QLabel('환영합니다', self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems([
            '효과 선택',
            '엠보싱',
            '카툰',
            '연필 스케치(명암)',
            '연필 스케치(컬러)',
            '유화',
            '세피아'
        ])

        selectBtn.setGeometry(20, 20, 120, 40)
        self.pickCombo.setGeometry(150, 20, 120, 40)
        self.saveBtn.setGeometry(280, 20, 120, 40)
        quitBtn.setGeometry(460, 20, 120, 40)
        self.label.setGeometry(30, 70, 580, 20)

        selectBtn.clicked.connect(self.select_image)
        self.saveBtn.clicked.connect(self.save_image)
        quitBtn.clicked.connect(self.app_quit)

        self.saveBtn.setEnabled(False)
        self.pickCombo.setEnabled(False)

        self.pickCombo.currentIndexChanged.connect(self.update_save_button)

    def update_save_button(self):
        if self.pickCombo.currentIndex() == 0:
            self.saveBtn.setEnabled(False)

        elif self.pickCombo.currentIndex() == 1:
            self.embossing_effect()
            self.saveBtn.setEnabled(True)

        elif self.pickCombo.currentIndex() == 2:
            self.cartoon_effect()
            self.saveBtn.setEnabled(True)

        elif self.pickCombo.currentIndex() == 3:
            self.gray_sketch_effect()
            self.saveBtn.setEnabled(True)

        elif self.pickCombo.currentIndex() == 4:
            self.color_sketch_effect()
            self.saveBtn.setEnabled(True)

        elif self.pickCombo.currentIndex() == 5:
            self.oil_effect()
            self.saveBtn.setEnabled(True)

        elif self.pickCombo.currentIndex() == 6:
            self.sepia_effect()
            self.saveBtn.setEnabled(True)

    def select_image(self):
        fname = QFileDialog.getOpenFileName(self, 'Select image', './')
        with open(fname[0], 'rb') as f:
            image_data = f.read()

        np_array = np.frombuffer(image_data, np.uint8)
        self.img = cv.imdecode(np_array, cv.IMREAD_COLOR)
        
        if self.img is None:
            self.label.setText('이미지 선택 실패')
            return 

        self.pickCombo.setEnabled(True)
        self.label.setText('원하는 특수 효과 선택')
        cv.imshow('Original Image', self.img)

    def embossing_effect(self):
        femboss = np.array([[-1.0, 0.0, 0.0],
                            [0.0, 0.0, 0.0],
                            [0.0, 0.0, 1.0]])
        gray_img = np.int16(cv.cvtColor(self.img, cv.COLOR_BGR2GRAY))
        self.emboss_img = np.uint8(np.clip(cv.filter2D(gray_img, -1, femboss) + 128, 0, 255))
        cv.imshow('Effected Image', self.emboss_img)

    def cartoon_effect(self):
        self.cartoon_img = cv.stylization(self.img, sigma_s=60, sigma_r=0.45)
        cv.imshow('Effected Image', self.cartoon_img)

    def gray_sketch_effect(self):
        self.gray_sketch_img = cv.pencilSketch(self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02)[0]
        cv.imshow('Effected Image', self.gray_sketch_img)
    
    def color_sketch_effect(self):
        self.color_sketch_img = cv.pencilSketch(self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02)[1]
        cv.imshow('Effected Image', self.color_sketch_img)

    def oil_effect(self):
        self.oil_img = cv.xphoto.oilPainting(self.img, 10, 1, cv.COLOR_BGR2Lab)
        cv.imshow('Effected Image', self.oil_img)

    def sepia_effect(self):
        sepia_kernel = np.array([[0.272, 0.534, 0.131],
                        [0.349, 0.686, 0.168],
                        [0.393, 0.769, 0.189]])
        self.sepia_img = cv.transform(self.img, sepia_kernel)
        cv.imshow('Effected Image', self.sepia_img)

    def save_image(self):
        fname, _ = QFileDialog.getSaveFileName(self, '이미지 저장', './')
        file_name, file_extension = os.path.splitext(fname)
        if not file_extension: file_extension = '.png'

        i = self.pickCombo.currentIndex()
        if i == 1: self.write_image(file_name, file_extension, self.emboss_img)
        elif i == 2: self.write_image(file_name, file_extension, self.cartoon_img)
        elif i == 3: self.write_image(file_name, file_extension, self.gray_sketch_img)
        elif i == 4: self.write_image(file_name, file_extension, self.color_sketch_img)
        elif i == 5: self.write_image(file_name, file_extension, self.oil_img)
        elif i == 6: self.write_image(file_name, file_extension, self.sepia_img)

        self.label.setText('특수 효과 이미지 저장 완료')

    def write_image(self, file_name, file_extension, img):
        _, image_data = cv.imencode(file_extension, img)
        print(image_data)

        with open(f'{file_name}{file_extension}', 'wb') as f:
            f.write(image_data)

    def app_quit(self):
        cv.destroyAllWindows()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SpecialEffect()
    win.show()
    app.exec()