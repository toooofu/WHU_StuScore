#-*- coding:utf-8 -*-
from PIL import Image
import pytesseract
import re
import random

#img = Image.open('captcha.tiff')
def binarize_image(img):
	pixdata = img.load()
	for y in xrange(img.size[1]):
		for x in xrange(img.size[0]):
			if pixdata[x, y][0] < 100 or pixdata[x, y][1] <100 or pixdata[x, y][2] < 100:
				pixdata[x, y] = (0, 0, 0, 255)
			else:
				pixdata[x, y] = (255, 255, 255, 255)
	return img

def tesseract(img):
	text = pytesseract.image_to_string(img)
	text = re.sub('[\W]', '', text)
	return text

def image_to_text(img):
	return tesseract(img)

# 降噪
# 根据一个点A的RGB值，与周围的8个点的RBG值比较，设定一个值N（0 <N <8），当A的RGB值与周围8个点的RGB相等数小于N时，此点为噪点
# N: Integer 降噪率 0 <N <8
# Z: Integer 降噪次数
def clearnoise(img,N,Z):
	pixdata = img.load()
	for i in xrange(0, Z):
		pixdata[0, 0] = (0, 0, 0)
		pixdata[img.size[0]-1, img.size[1]-1] = (0, 0, 0)
		for x in xrange(1, img.size[0] - 1):
			for y in xrange(1, img.size[1] - 1):
				nearDots = 0
#				print pixdata[x,y]
				if pixdata[x, y] == (0, 0, 0):
					if pixdata[x-1, y-1] == (0, 0, 0):
						nearDots += 1
					if pixdata[x-1, y] == (0, 0, 0):
						nearDots += 1
					if pixdata[x-1, y+1] == (0, 0, 0):
						nearDots += 1
					if pixdata[x, y-1] == (0, 0, 0):
						nearDots += 1
					if pixdata[x, y+1] == (0, 0, 0):
						nearDots += 1
					if pixdata[x+1, y-1] == (0, 0, 0):
						nearDots += 1
					if pixdata[x+1, y] == (0, 0, 0):
						nearDots += 1
					if pixdata[x+1, y+1] == (0, 0, 0):
						nearDots += 1
					if nearDots < N:
						pixdata[x, y] = (255, 255, 255)
#						print pixdata[x, y]
				else:
					continue
	return img

# def img_crop(img):
# 	inletter = False
# 	foundletter = False
# 	start = 0
# 	end = 0
# 	pixdata = img.load()
# 	letters = []
#
# 	for y in range(img.size[0]):
# 		for x in range(img.size[1]):
# 			if pixdata[y,x] != (255, 255, 255):
# 				inletter = True
# 		if foundletter == False and inletter == True:
# 			foundletter = True
# 			start = y
#
# 		if foundletter == True and inletter == False:
# 			foundletter = False
# 			end = y
# 			letters.append((start,end))
#
# 		inletter = False
#
# 	return letters


# bin_img = binarize_image(img)
# bin_cl_img = clearnoise(bin_img, 3, 1)
#bin_cl_img.show()
# letters = img_crop(bin_cl_img)
# print letters
#text = ''
# for letter in letters:
# 	word = bin_cl_img.crop((letter[0]-4, 0, letter[1]+4, bin_cl_img.size[1]))
# 	word.show()
# 	word.save(str(random.randint(1,100))+'.tif')
# 	print image_to_text(word)
# 	text.join(image_to_text(word))
# text = image_to_text(bin_cl_img)
# print "result:"+text