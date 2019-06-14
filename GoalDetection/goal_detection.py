
#! coding: Shift_JIS

import cv2
import numpy as np
import math

'''
引数	画像(cv::Mat)
戻り値	[距離,角度]

'''

def GoalDetection(img):

	#cv2.imshow('Input Image',img)

	#赤mask生成
	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]
	mask1 = np.zeros(h.shape, dtype=np.uint8)
	mask1[((h < 10) | (h > 200)) & (s > 120)] = 255
	#cv2.imshow('Red Zone', mask1)
	
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
	print('最大面積は',max_area)

	#goal未検出時
	if max_area <= 100:
		print( "コーンが検出されませんでした。" )
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [-1,-1]
	#goal判定
	if max_area >= 80000:
		print( "ゴール!!!!!!!!" )
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [0,0]
	
	#垂直な矩形
	x,y,w,h = cv2.boundingRect(cnt)
	#img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	print('ターゲットの中心座標は:',x+w/2) 
	img = cv2.circle(img,(int(x+w/2),int(y+h/2)), 5, (255,0,0), -1, cv2.LINE_AA)

	#距離計算
	L1 = 10		#基準距離
	S1 = 200	#基準面積
	L2 = L1*math.sqrt(S1)/math.sqrt(max_area)


	cv2.imshow("target", img);
	cv2.waitKey()	
	cv2.destroyAllWindows()

	return [L2,x+w/2]
		

im = cv2.imread('target10.jpg')
print (GoalDetection(im))