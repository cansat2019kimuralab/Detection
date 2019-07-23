
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
import cv2
import numpy as np
import math
import Capture

'''
input	imgpath
output	[distance,angle]

'''



def GoalDetection(imgpath):
	imgname = Capture.Capture(imgpath)
	img = cv2.imread(imgname)
	#cv2.imshow('Input Image',img)
	hig, wid, col = img.shape

	#make mask

	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)

	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]

	mask = np.zeros(h.shape, dtype=np.uint8)
	mask[((h < 10) | (h > 200)) & (s > 120)] = 255

	#cv2.imshow('Red Zone', mask)

	#contour
	mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


	#max area
	max_area = 0
	max_area_contour = -1

	for j in range(0,len(contours)):
		area = cv2.contourArea(contours[j])
		if max_area < area:
			max_area = area
			max_area_contour = j

	cnt = contours[max_area_contour]

	#print('Max area is',max_area)

	#no goal
	if max_area <= 100:
		print( "There is not the target" )
		return [-1,-1,imgname]

	#goal

	if max_area >= 1000:
		print( "GOAL" )
		return [0,0,imgname]

	#rectangle
	x,y,w,h = cv2.boundingRect(cnt)

	#img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

	GAP = x+w/2-wid/2

	if GAP >= 0:
		print('The target is', GAP, 'degrees to the right')

	if GAP < 0:
		print('The target is', abs(GAP), 'degrees to the left')

	#img = cv2.circle(img,(int(x+w/2),int(y+3*h/4)), 2, (255,0,0), -1, cv2.LINE_AA)


	#calculate distance
	L_samp = 10		#standard distance
	S_samp = 200	#standard area
	L = L_samp*math.sqrt(S_samp)/math.sqrt(max_area)

	print('The target is', '{:.1f}'.format(L), 'm from here')

	#cv2.imshow("target", img)
	#cv2.waitKey()
	#cv2.destroyAllWindows()

	return [L,GAP,imgname]

if __name__ == "__main__":
	GoalDetection(photo)
