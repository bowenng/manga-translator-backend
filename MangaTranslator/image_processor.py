import cv2
import numpy as np


class ImageProcessor:
    def __init__(self):
        self.image = None

    # get grayscale image
    def get_grayscale(self):
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        return self

    # noise removal
    def remove_noise(self):
        self.image = cv2.medianBlur(self.image, 5)
        return self

    # thresholding
    def thresholding(self):
        self.image = cv2.threshold(self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        return self

    # dilation
    def dilate(self):
        kernel = np.ones((5, 5), np.uint8)
        self.image = cv2.dilate(self.image, kernel, iterations=1)
        return self

    # erosion
    def erode(self):
        kernel = np.ones((5, 5), np.uint8)
        self.image = cv2.erode(self, kernel, iterations=1)
        return self

    # opening - erosion followed by dilation
    def opening(self):
        kernel = np.ones((5, 5), np.uint8)
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, kernel)
        return self

    # canny edge detection
    def canny(self):
        self.image = cv2.Canny(self.image, 100, 200)
        return self

    # skew correction
    def deskew(self):
        coords = np.column_stack(np.where(self.image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(self.image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        self.image = rotated
        return self

    def start_processing_image(self, image_uri):
        self.image = cv2.imread(image_uri)
        return self

    def finish(self):
        image = self.image
        self.image = None
        return image