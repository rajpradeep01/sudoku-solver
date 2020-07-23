import cv2
import numpy as np

class Classifier():
	def __init__(self, path):
		self.model = cv2.dnn.readNetFromONNX(path)

	def preProcess(self, image):
		clearBorder = np.zeros_like(image).astype(np.uint8)
		clearBorder[4:24, 4:24] = image[4:24, 4:24]
		# cv2.imshow('dd', clearBorder)
		# cv2.waitKey(0)
		clearBorder = clearBorder.astype(np.float32) / 255.
		clearBorder = cv2.dnn.blobFromImage(clearBorder)
		self.input = clearBorder
		self.model.setInput(clearBorder)

	@staticmethod
	def softmax(vec):
		out = np.exp(vec)
		out /= out.sum()
		return out

	def predict(self, image):
		self.preProcess(image)
		out = self.softmax(self.model.forward())

		classId = np.argmax(out)
		confidence = out[0, classId]
		if self.input.sum() < 30:
			classId = 0
		return classId#, confidence

if __name__ == '__main__':
	model = Classifier('mnist-8.onnx')
	print('init')
	print(model.predict(cv2.imread('mnist/datasets_1272_2280_testSample_testSample_img_100.jpg', 0)))
	print(model.predict(cv2.imread('mnist/datasets_1272_2280_testSample_testSample_img_107.jpg', 0)))
	print(model.predict(cv2.imread('mnist/datasets_1272_2280_testSample_testSample_img_113.jpg', 0)))
	print(model.predict(cv2.imread('mnist/datasets_1272_2280_testSample_testSample_img_114.jpg', 0)))
