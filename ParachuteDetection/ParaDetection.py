import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import cv2
import numpy as np
import difflib
import TSL2561


def ParaJudge(LuxThd):
	Motor.motor(30,30,0.2)
	Motor.motor(0,0,0.2)
	lux=TSL2561.readLux()
	#print("lux1: "+str(lux[0]))

	if lux[0] < LuxThd:
		time.sleep(1)
		return [0, lux[0]]

	else:
		return [1, lux[0]]


def ParaDetection(img):
	#make mask
	img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
	h = img_HSV[:, :, 0]
	s = img_HSV[:, :, 1]
	mask = np.zeros(h.shape, dtype=np.uint8)
	mask[((h < 10) | (h > 200)) & (s > 120)] = 255

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
	#print('Max area is',max_area)

	#No Parachute 
	if max_area <= 100:
		#print( "There is not the Parachute" )
		return [0, max_area, img]

	#Prachute 

	else:
		#print( "There is the Parachute" )
		return [1, max_area, img]

if __name__ == "__main__":
	im = cv2.imread('photo/photo1.jpg')
	ParaDetection(im)

