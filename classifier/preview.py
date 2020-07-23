import cv2
import numpy as np

def show(image):
	mat = (255 * image).astype(np.uint8)
	cv2.imshow('disp', mat)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

def see(num, i):
	show(data[f'arr_{num}'][i])

data = np.load('compressed/data.npz')
