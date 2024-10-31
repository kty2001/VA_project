import os
import sys
import winsound

from ultralytics import YOLO
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
        self.segmentBtn = QPushButton('세그멘트', self)
        self.pano_saveBtn = QPushButton('파노라마 이미지저장', self)
        self.seg_saveBtn = QPushButton('세그멘테이션 이미지 저장', self)
        quitBtn = QPushButton('나가기', self)
        self.label = QLabel('환영합니다!', self)

        collectBtn.setGeometry(10, 25, 100, 30)
        self.showBtn.setGeometry(10, 55, 100, 30)
        self.stitchBtn.setGeometry(210, 25, 100, 30)
        self.segmentBtn.setGeometry(210, 55, 100, 30)
        self.pano_saveBtn.setGeometry(310, 25, 180, 30)
        self.seg_saveBtn.setGeometry(310, 55, 180, 30)
        quitBtn.setGeometry(590, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)

        self.showBtn.setEnabled(False)
        self.stitchBtn.setEnabled(False)
        self.segmentBtn.setEnabled(False)
        self.pano_saveBtn.setEnabled(False)
        self.seg_saveBtn.setEnabled(False)

        collectBtn.clicked.connect(self.collect_image)
        self.showBtn.clicked.connect(self.show_collected_image)
        self.stitchBtn.clicked.connect(self.stitch_collected_image)
        self.segmentBtn.clicked.connect(self.segment_image)
        self.pano_saveBtn.clicked.connect(self.stitched_image_save)
        self.seg_saveBtn.clicked.connect(self.segmented_image_save)
        quitBtn.clicked.connect(self.app_quit)
        

    def collect_image(self):
        self.showBtn.setEnabled(False)
        self.stitchBtn.setEnabled(False)
        self.pano_saveBtn.setEnabled(False)
        self.seg_saveBtn.setEnabled(False)
        self.label.setText('c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다.')

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened():
            self.label.setText('카메라 연결 실패')
        else:
            self.images = []
            while True:
                ret, frame = self.cap.read()
                if not ret: break

                cv.imshow('Video display', frame)
                cv.moveWindow('Video display', 200, 410)

                key = cv.waitKey(1)
                if key == ord('c'):
                    self.images.append(frame)
                elif key == ord('q'):
                    self.cap.release()
                    cv.destroyWindow('Video display')
                    break
            
            if len(self.images) >= 2:
                self.showBtn.setEnabled(True)
                self.stitchBtn.setEnabled(True)

            self.label.setText(f'수집된 영상은 {len(self.images)} 장입니다.')

    def show_collected_image(self):
        stack = cv.resize(self.images[0], dsize=(0,0), fx=0.5, fy=0.5)
        for i in range(1, len(self.images)):
            stack = np.hstack((stack, cv.resize(self.images[i], dsize=(0,0), fx=0.5, fy=0.5)))
        cv.imshow('Image collection', stack)
        cv.moveWindow('Image collection', 200, 10)

    def stitch_collected_image(self):
        stitcher = cv.Stitcher.create()
        status, self.stitched_image = stitcher.stitch(self.images)
        if status == cv.STITCHER_OK:
            cv.imshow('Image stitched panorama', self.stitched_image)
            cv.moveWindow('Image stitched panorama', 200, 410)
            self.label.setText("파노라마 이미지 제작 완료")
            self.pano_saveBtn.setEnabled(True)
            self.segmentBtn.setEnabled(True)
        else:
            winsound.Beep(1000, 500)
            self.label.setText("파노라마 이미지 제작 실패")

    def segment_image(self):
        try:
            model = YOLO("../assets/yolo11n-seg.pt")
            results = model(self.stitched_image)[0]

            mask_data = results.masks.data

            mask_image = np.max(mask_data.cpu().numpy(), axis=0).astype(np.uint8) * 255

            mask_image = cv.cvtColor(mask_image, cv.COLOR_GRAY2BGR)
            mask_image = cv.resize(mask_image, (self.stitched_image.shape[1], self.stitched_image.shape[0]))

            self.segmented_image = cv.addWeighted(self.stitched_image, 0.5, mask_image, 0.5, 0)

            cv.imshow("Segmented Image", self.segmented_image)

            self.label.setText("세그멘테이션 이미지 제작 완료")
            self.seg_saveBtn.setEnabled(True)

        except:
            self.label.setText("세그멘테이션 이미지 제작 실패")

    def stitched_image_save(self):
        try:
            fname, _ = QFileDialog.getSaveFileName(self, '파일 저장', './')
            file_name, file_extension = os.path.splitext(fname)
            if not file_extension: file_extension = '.png'
                
            _, image_data = cv.imencode(file_extension, self.stitched_image)

            with open(f'{file_name}{file_extension}', 'wb') as f:
                f.write(image_data)

            self.label.setText(f"파노라마 이미지 저장 완료")

        except:
            self.label.setText(f"파노라마 이미지 저장 실패")

    def segmented_image_save(self):
        try:
            fname, _ = QFileDialog.getSaveFileName(self, '파일 저장', './')
            file_name, file_extension = os.path.splitext(fname)
            if not file_extension: file_extension = '.png'

            _, image_data = cv.imencode(file_extension, self.segmented_image)
            with open(f'{file_name}{file_extension}', 'wb') as f:
                f.write(image_data)

            self.label.setText(f"세그멘테이션 이미지 저장 완료")
        
        except:
            self.label.setText(f"세그멘테이션 이미지 저장 실패")

    def app_quit(self):
        try:
            self.cap.release()
        except:
            pass

        cv.destroyAllWindows()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Panorama()
    win.show()
    app.exec()