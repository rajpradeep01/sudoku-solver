def getValues(imagePath):
	import cv2
	import numpy as np
	from classifier import Classifier

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

	M = cv2.getPerspectiveTransform(orderPoints(pIn = largestCnt), np.array([[0, 0], [252, 0], [252, 252], [0, 252]], dtype = np.float32))

	image = cv2.GaussianBlur(image, (5, 5), 0)
	image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 2)
	warped = cv2.warpPerspective(image, M, (252, 252))
	warped = cv2.morphologyEx(warped, cv2.MORPH_OPEN, np.ones((1, 1)))


	classifier = Classifier('mnist-8.onnx')
	values = [[classifier.predict(warped[i*28:(i+1)*28, j*28:(j+1)*28]) for j in range(9)]for i in range(9)]
	for row in values:
		for number in row:
			print(number, end=' ')
		print()
	cv2.imshow('disp', warped)
	cv2.waitKey(0)
	return values

if __name__ == '__main__':
	from tkinter import Tk
	from tkinter.filedialog import askopenfilename

	Tk().withdraw()
	filename = askopenfilename()
	values = getValues(filename)
	# print(values)
