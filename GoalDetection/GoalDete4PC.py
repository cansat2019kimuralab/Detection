import cv2
import numpy as np
import math

i =  100

def GoalDetection(img, H_min, H_max, S_thd, G_thd):
	global i
	try:
		cv2.imshow('Input Image',img)
		hig, wid, col = img.shape

		#mask生成

		img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)

		h = img_HSV[:, :, 0]
		s = img_HSV[:, :, 1]

		mask1 = np.zeros(h.shape, dtype=np.uint8)
		mask1[((h < H_max) | (h > H_min)) & (s > S_thd)] = 255

		cv2.imshow('Red Zone', mask1)

		#輪郭処理
		contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


		#最大面積
		max_area = 0
		max_area_contour = -1

		for j in range(0,len(contours)):
			area = cv2.contourArea(contours[j])
			if max_area < area:
				max_area = area
				max_area_contour = j

		cnt = contours[max_area_contour]

		print('Max area is',max_area)

		#goal未検出時

		if max_area_contour == -1:
			print("there is the no goal")
			cv2.waitKey()
			cv2.destroyAllWindows()

		elif max_area <= 30:
			print("there is the no goal")
			cv2.waitKey()
			cv2.destroyAllWindows()
				
		#goal判定
		elif max_area >= G_thd:
			print( "GOAL" )
			cv2.waitKey()
			cv2.destroyAllWindows()

		#垂直な矩形
		x,y,w,h = cv2.boundingRect(cnt)

		img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

		GAP = x+w/2-wid/2

		if GAP >= 0:
			print('The target is', GAP, 'degrees to the right')

		if GAP < 0:
			print('The target is', abs(GAP), 'degrees to the left')

		img = cv2.circle(img,(int(x+w/2),int(y+3*h/4)), 2, (255,0,0), -1, cv2.LINE_AA)

		print('The target is', '{:.1f}'.format(L), 'm from here')

		cv2.imshow("target", img)
		cv2.waitKey()
		cv2.destroyAllWindows()

		return 0
	except:
		i = i + 1
		cv2.imshow("target", img)
		cv2.waitKey()
		cv2.destroyAllWindows()
		return 0

if __name__ == "__main__":
	im = cv2.imread('photo/photo52.jpg')
	GoalDetection(im, 200 , 10, 130, 7000)