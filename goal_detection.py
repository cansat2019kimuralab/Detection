#! coding: Shift_JIS

import cv2
import numpy as np
import sys

#���͉摜�̎擾
img = cv2.imread('target18.jpg')
img = cv2.resize(img,(640,480))
Height, Width =img.shape[:2]
s1 = (Height,Width)
cv2.imshow('���摜',img)

#���͉摜�̃R�s�[(�t�B���^�p)
img_gauss=img.copy()

#�t�B���^����(�ڂ���)
img_gauss = cv2.GaussianBlur(img_gauss, (9, 9), 3)

#BGR->HSV
img_HSV = cv2.cvtColor(img_gauss,cv2.COLOR_BGR2HSV)

#H,S�͈̔͐ݒ�
lower_red = np.array([0,80,0])
upper_red = np.array([10,255,255])

#HSV��H,S����}�X�N�摜����
mask1 = cv2.inRange(img_HSV, lower_red, upper_red)
cv2.imshow('�F���ʓx�A�_���ό�摜', mask1)

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
#�d�S�v�Z
M = cv2.moments(cnt)
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print("�d�S��(",cx,",",cy,")")

#�ő�ʐς̒��o
print('�ő�ʐς�',max_area)		

#goal���o�s��
if max_area <= 100:
	print( "�R�[�������o����܂���ł����B" )
	cv2.waitKey()
	cv2.destroyAllWindows()
	sys.exit()
#goal����
if max_area >= 80000:
	print( "�S�[��!!!!!!!!" )
	cv2.waitKey()
	cv2.destroyAllWindows()
	sys.exit()
		
#�X������`
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
img = cv2.drawContours(img,[box],0,(0,0,255),2)

#rotated_center = rect.center()
img = cv2.circle(img,(cx,cy), 5, (255,0,0), -1, cv2.LINE_AA)						#���S�`��


#�����ȋ�`
x,y,w,h = cv2.boundingRect(cnt)
im = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

#print("�摜�̒��S��x���W��", s1.width/2, "\n")								#�摜�̒��S���W�̕\
#print("�X�����^�[�Q�b�g��x���W��", rect.center.x ,"\n")				#�^�[�Q�b�g�̒��S���W�̕\��

cv2.imshow("�^�[�Q�b�g", img);														#�}�X�N�\��
cv2.waitKey()	
cv2.destroyAllWindows()
