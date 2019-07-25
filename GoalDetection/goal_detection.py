
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
import cv2
import numpy as np
import math
import Capture

def GoalDetection(imgpath, H_min, H_max, S_thd):
	imgname = Capture.Capture(imgpath)
	img = cv2.imread(imgname)
	hig, wid, col = img.shape

	#make mask
	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]
	mask = np.zeros(h.shape, dtype=np.uint8)
	mask[((h < H_max) | (h > H_min)) & (s > S_thd)] = 255

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

	if max_area_contour == -1:
		print( "There is not the target" )
		return [-1,-1,imgname]
		
	cnt = contours[max_area_contour]
	print('Max area is',max_area)

	#no goal
	if max_area <= 100:
		print( "There is not the target" )
		return [-1,-1,imgname]

	#goal
	if max_area >= 70000:
		print( "GOAL" )
		return [0,0,imgname]

	#rectangle
	x,y,w,h = cv2.boundingRect(cnt)

	#center of the target <-> center of the picture (pixel)
	GAP = x+w/2-wid/2

	if GAP > 0:
		print('The target is', GAP, 'degrees to the right')

	elif GAP < 0:
		print('The target is', abs(GAP), 'degrees to the left')

	else :
		print('The target is center')

	#calculate distance
	L_samp = 10		#standard distance
	S_samp = 200	#standard area
	L = L_samp*math.sqrt(S_samp)/math.sqrt(max_area)
	#print('The target is', '{:.1f}'.format(L), 'm from here')
	return [L,GAP,imgname]

if __name__ == "__main__":
	GoalDetection("photo",200 ,10, 120)
