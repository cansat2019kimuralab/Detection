import cv2
import numpy as np
import math

def DarkDetection(img, V_thd, D_thd):
	cv2.imshow('Input Image',img)

	#make mask
	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]
	v = img_HSV[:, :, 2]
	mask = np.zeros(h.shape, dtype=np.uint8)
	mask[v < V_thd] = 255

	cv2.imshow('Red Zone', mask)

	#black area
	area = cv2.countNonZero(mask)
	print('area is',area)
	
	if area > D_thd:
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [0, area]
	else:
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [1, area]

	cv2.waitKey()
	cv2.destroyAllWindows()
	return [L,GAP]

if __name__ == "__main__":
	im = cv2.imread('photo3.jpg')
	Darkflug, DarkArea= DarkDetection(im, 40, 30000)
	print("Darkflug", Darkflug, "DarkArea",DarkArea)
