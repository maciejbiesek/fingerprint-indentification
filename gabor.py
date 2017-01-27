import numpy as np
import cv2

def build_filters():
	filters = []
	ksize = 31
	for theta in np.arange(0, np.pi, np.pi / 16):
		kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
		kern /= 1.5*kern.sum()
		filters.append(kern)
	return filters

def gabor(img):
	#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
	#img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

	filters = build_filters()
	accum = np.zeros_like(img)
	for kern in filters:
		fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
		accum = np.maximum(accum, fimg)
	return accum
