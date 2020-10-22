"""
@author: Furkan Guney 160403001

OpenCV is used for image processing transactions.
"""
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QImage
import sys
import os
import cv2
import time


class FurkansApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.my_window = uic.loadUi('fg_hw1_gui.ui', self)

        self.rgb_gray = 'gray'

        self.chooseImageBtn = self.my_window.chooseImageButton
        self.imageNameLabel = self.my_window.imageNameLabel

        self.kernelX = self.my_window.kernelLineX
        self.kernelY = self.my_window.kernelLineY
        self.kernelDefaultBtn = self.my_window.defaultKernelButton

        self.grayRadio = self.my_window.grayRadioButton
        self.rgbRadio = self.my_window.rgbRadioButton

        self.processBtn = self.my_window.processButton

        self.orgImLabel = self.my_window.originalImageLabel
        self.procImLabel = self.my_window.processedImageLabel

        self.show()

        self.popup = QMessageBox()
        self.popup.setWindowTitle("Ups!!")
        self.popup.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        self.chooseImageBtn.clicked.connect(self.choose_image)
        self.kernelDefaultBtn.clicked.connect(self.default_kernel)
        self.grayRadio.clicked.connect(self.use_grayscale)
        self.rgbRadio.clicked.connect(self.use_rgb)
        self.processBtn.clicked.connect(self.proc_btn_clicked)

    def choose_image(self):
        try:
            self.image, _ = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.png *.jpg *.jpeg)")
            if not self.image:
                self.popup.setIcon(QMessageBox.Warning)
                self.popup.setText("You didn't choose one of the '.png', '.jpg' or '.jpeg' files.")
                self.popup.exec_()
                return
        except:
            self.popup.setIcon(QMessageBox.Warning)
            self.popup.setText("Something went wrong! :(")
            self.popup.exec_()
            return

        im_name = str(os.path.basename(self.image))
        if not im_name.endswith('.png') and not im_name.endswith('.jpg') and not im_name.endswith('.jpeg'):
            self.popup.setIcon(QMessageBox.Warning)
            self.popup.setText("You didn't choose one of the '.png', '.jpg' or '.jpeg' files.")
            self.popup.exec_()
            return

        self.imageNameLabel.setText(im_name)

        self.gray_name = f'grayscaled_{im_name}'
        self.img = cv2.imread(self.image)
        if self.rgb_gray == 'gray':
            self.gray_im = cv2.cvtColor(self.img, cv2.COLOR_RGB2GRAY)
            cv2.imwrite(self.gray_name, self.gray_im)

            pixmap = QPixmap(self.gray_name)
            self.orgImLabel.setPixmap(pixmap)
        else:
            pixmap = QPixmap(im_name)
            self.orgImLabel.setPixmap(pixmap)

    def default_kernel(self):
        self.kernelX.setText("3")
        self.kernelY.setText("3")

    def use_grayscale(self):
        self.rgb_gray = 'gray'

        pixmap = QPixmap(self.gray_name)
        self.orgImLabel.setPixmap(pixmap)

    def use_rgb(self):
        self.rgb_gray = 'rgb'
        pixmap = QPixmap(self.image)
        self.orgImLabel.setPixmap(pixmap)

    def process(self, img, x, y):
        img2 = img.copy()

        # take the image shape for further process. height, width, and channel
        # if image is in grayscale there will be no channel, we can solve this with try except method
        try:
            h, w, d = img.shape
        except:
            h, w = img.shape
            d = None

        # if we have channel (image is not grayscaled)
        if d:
            # for each channel (r, g and b) we will do the same process
            dim = 0
            while dim < d:
                # for every 5 rows we will take array from t to t+y
                t = 0
                while t < (h - y):
                    # for every 5 columns we will take array from k to k+x
                    k = 0
                    while k < (w - x):
                        batch = img[t:t + y, k:k + x,
                                dim]  # taking the part of image per each channel into batch variable

                        # create variable summ for saving average
                        summ = 0
                        batch_h, batch_w = batch.shape  # batch shape for taking values of batch
                        for b_y in range(batch_h):
                            for b_x in range(batch_w):
                                summ += batch[b_y, b_x]  # sum all of the batch values and save into summ

                        # taken part of img is changed. Now apply those changes on img2.
                        # the value of each batch in image 2 will be -> summation of batch values / batch size
                        img2[t:t + y, k:k + x, dim] = int(summ / (x * y))

                        k += x
                    t += y
                dim += 1
        else:
            # If we are here, the image is grayscaled. All the process is the same with above but here is no channel.
            t = 0
            while t < (h - y):
                k = 0
                while k < (w - x):
                    batch = img[t:t + y, k:k + x]

                    summ = 0
                    batch_h, batch_w = batch.shape
                    for b_y in range(batch_h):
                        for b_x in range(batch_w):
                            summ += batch[b_y, b_x]
                    val = int(summ / (x * y))

                    img2[t:t + y, k:k + x] = val

                    k += x
                t += y
        return img2

    def proc_btn_clicked(self):
        if self.rgb_gray == 'gray':
            processed_name = 'processed_gray_image.jpg'
            img = self.gray_im
        else:
            processed_name = 'processed_image.jpg'
            img = self.img

        try:
            x = int(self.kernelX.text())
            y = int(self.kernelY.text())
        except:
            return
        processed_img = self.process(img, x, y)

        cv2.imwrite(processed_name, processed_img)

        pixmap = QPixmap(processed_name)
        self.procImLabel.setPixmap(pixmap)


app = QtWidgets.QApplication(sys.argv)
screen = FurkansApp()
sys.exit(app.exec_())

