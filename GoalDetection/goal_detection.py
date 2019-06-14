
#! coding: Shift_JIS

import cv2
import numpy as np
import math

'''
����	�摜(cv::Mat)
�߂�l	[����,�p�x]

'''

def GoalDetection(img):

	#cv2.imshow('Input Image',img)

	#��mask����
	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]
	mask1 = np.zeros(h.shape, dtype=np.uint8)
	mask1[((h < 10) | (h > 200)) & (s > 120)] = 255
	#cv2.imshow('Red Zone', mask1)
	
	#�֊s����
	contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	
	#�ő�ʐ�	
	max_area = 0
	max_area_contour = -1
	for j in range(0,len(contours)):
		area = cv2.contourArea(contours[j])
		if max_area < area:
			max_area = area
			max_area_contour = j
	
	cnt = contours[max_area_contour]
	print('�ő�ʐς�',max_area)

	#goal�����o��
	if max_area <= 100:
		print( "�R�[�������o����܂���ł����B" )
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [-1,-1]
	#goal����
	if max_area >= 80000:
		print( "�S�[��!!!!!!!!" )
		cv2.waitKey()
		cv2.destroyAllWindows()
		return [0,0]
	
	#�����ȋ�`
	x,y,w,h = cv2.boundingRect(cnt)
	#img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
	print('�^�[�Q�b�g�̒��S���W��:',x+w/2) 
	img = cv2.circle(img,(int(x+w/2),int(y+h/2)), 5, (255,0,0), -1, cv2.LINE_AA)

	#�����v�Z
	L1 = 10		#�����
	S1 = 200	#��ʐ�
	L2 = L1*math.sqrt(S1)/math.sqrt(max_area)


	cv2.imshow("target", img);
	cv2.waitKey()	
	cv2.destroyAllWindows()

	return [L2,x+w/2]
		

im = cv2.imread('target10.jpg')
print (GoalDetection(im))