from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os
import cv2
from tqdm import tqdm

anchors = [(9, 4), (9, 6), (9, 3), (9, 1), (9, 5), (9, 5), (9, 2), (9, 2), (9, 2), (9, 3)]
fonts = [ImageFont.truetype(f"fonts/{os.listdir('fonts')[i]}", 18) for i in range(10)]

def generate(number):
	number = ' ' if number == 0 else number
	buff = []
	for i, font in enumerate(fonts):
		for j in range(4):
			img = Image.new('1', (28, 28))
			d = ImageDraw.Draw(img, '1')
			d.text(anchors[i], f'{number}', True, font)
			cvimage = np.array(img)

			if j > 0:
				rr = (np.random.normal(0.5, 0.5, (14, 14)))
				rr[2:12, 4:10] = 0
				rr = cv2.resize(rr, (28, 28))
				cvimage[np.where(rr > 0.6+0.1*j)] = True

			buff.append(cvimage)
	return np.array(buff)

np.savez_compressed(f'compressed/data.npz', *([generate(i) for i in tqdm(range(10))]))
