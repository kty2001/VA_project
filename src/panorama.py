import sys
import winsound

import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QFileDialog,
    QApplication
)


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

        collectBtn.clicked.connect(self.image_collect)
        self.showBtn.clicked.connect(self.collected_image_show)
        self.stitchBtn.clicked.connect(self.collected_image_stitch)
        self.saveBtn.clicked.connect(self.stitched_image_save)
        quitBtn.clicked.connect(self.app_quit)
        

    def image_collect(self):
        self.showBtn.setEnabled(False)
        self.stitchBtn.setEnabled(False)
        self.saveBtn.setEnabled(False)
        self.label.setText('c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다.')

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened():
            self.label.setText('카메라 연결 실패')
        else:
            self.imgs = []
            while True:
                ret, frame = self.cap.read()
                if not ret: break

                cv.imshow('Video display', frame)
                cv.moveWindow('Video display', 200, 410)

                key = cv.waitKey(1)
                if key == ord('c'):
                    self.imgs.append(frame)
                elif key == ord('q'):
                    self.cap.release()
                    cv.destroyWindow('Video display')
                    break
            
            if len(self.imgs) >= 2:
                self.showBtn.setEnabled(True)
                self.stitchBtn.setEnabled(True)
                self.saveBtn.setEnabled(True)

            self.label.setText(f'수집된 영상은 {len(self.imgs)} 장입니다.')

    def collected_image_show(self):
        stack = cv.resize(self.imgs[0], dsize=(0,0), fx=0.25, fy=0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], dsize=(0,0), fx=0.25, fy=0.25)))
        cv.imshow('Image collection', stack)
        cv.moveWindow('Image collection', 200, 10)

    def collected_image_stitch(self):
        stitcher = cv.Stitcher.create()
        status, self.img_stitched = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:
            cv.imshow('Image stitched panorama', self.img_stitched)
            cv.moveWindow('Image stitched panorama', 200, 410)
            self.label.setText("파노라마 이미지 제작 완료")
        else:
            winsound.Beep(1000, 500)
            self.label.setText("파노라마 이미지 제작 실패")

    def stitched_image_save(self):
        save_dir = './outputs'

        fname, _ = QFileDialog.getSaveFileName(self, '파일 저장', save_dir)
        if len(fname.split(".")) == 1: fname = f'{fname}.png'
            
        cv.imwrite(fname, self.img_stitched)

        self.label.setText(f"{save_dir} 디렉토리에 파노라마 이미지 저장 완료")

    def app_quit(self):
        self.cap.release()
        cv.destroyAllWindows()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Panorama()
    win.show()
    app.exec()