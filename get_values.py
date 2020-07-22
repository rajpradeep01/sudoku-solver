def getValues(imagePath):
	import cv2
	import numpy as np

	def orderPoints(pIn):
		pIn.reshape(4, 2)
		pOut = []
		s = np.sum(pIn, axis = 2)
		d = np.diff(pIn, axis = 2)
		pOut.append(pIn[np.argmin(s)])
		pOut.append(pIn[np.argmin(d)])
		pOut.append(pIn[np.argmax(s)])
		pOut.append(pIn[np.argmax(d)])
		return np.array(pOut, dtype = np.float32)

	image = cv2.imread(imagePath, 0)
	image = cv2.GaussianBlur(image, (5, 5), 0)
	cann = cv2.Canny(image, 100, 200)
	cann = cv2.dilate(cann, np.ones((2, 2)))
	conts = cv2.findContours(cann, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

	largestArea = 0.
	for cont in conts:
		epsilon = 0.02 * cv2.arcLength(cont, True)
		approx = cv2.approxPolyDP(cont, epsilon, True)
		if len(approx) == 4:
			x, y, w, h = cv2.boundingRect(approx)
			area = cv2.contourArea(approx)
			if area > largestArea:
				largestCnt = approx
				largestArea = area

	largestCnt
	M = cv2.getPerspectiveTransform(orderPoints(pIn = largestCnt), np.array([[0, 0], [180, 0], [180, 180], [0, 180]], dtype = np.float32))
	warped = cv2.warpPerspective(image, M, (180, 180))
	image = cv2.cvtColor(warped, cv2.COLOR_GRAY2BGR)

	cv2.imshow('disp', image)
	cv2.waitKey(0)

if __name__ == '__main__':
	from tkinter import Tk
	from tkinter.filedialog import askopenfilename

	Tk().withdraw()
	filename = askopenfilename()
	getValues(filename)
