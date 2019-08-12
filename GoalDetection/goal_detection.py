
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
import cv2
import numpy as np
import math
import Capture

def curvingSwitch(GAP, add):
	if abs(GAP) > 144:
		return add
	elif abs(GAP) > 128:
		return add*0.9
	elif abs(GAP) > 112:
		return add*0.8
	elif abs(GAP) > 96:
		return add*0.7
	elif abs(GAP) > 80:
		return add*0.6
	elif abs(GAP) > 64:
		return add*0.5
	elif abs(GAP) > 48:
		return add*0.4
	elif abs(GAP) > 32:
		return add*0.3
	elif abs(GAP) > 16:
		return add*0.2
	elif abs(GAP) >= 0:
		return 0

def calR2G(nowArea, nowGAP, SampArea, SampL, SampX, SampGAP):
	nowL = SampL*math.sqrt(SampArea)/math.sqrt(nowArea)
	print("nowL",nowL)
	print("nowGAP",nowGAP)
	nowX = SampX * math.sqrt((1000*nowL)**2 - nowGAP**2) / math.sqrt((1000*SampL)**2 - SampGAP**2) * nowGAP / SampGAP
	print("nowX",nowX)
	angR2G = math.degrees(math.asin(nowX/nowL))
	print("angR2G",angR2G)
	return [nowL, angR2G]

def GoalDetection(imgpath, H_min, H_max, S_thd, G_thd):
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

	#no goal
	if max_area_contour == -1:
		return [-1, 0, -1, imgname]

	elif max_area <= 100:
		return [-1, 0, -1, imgname]

	#goal
	elif max_area >= G_thd:
		return [0, -1 ,0, imgname]
	else:
		#rectangle
		cnt = contours[max_area_contour]
		x,y,w,h = cv2.boundingRect(cnt)
		GAP = x+w/2-160
		return [1, max_area, GAP, imgname]

if __name__ == "__main__":
	try:
		while 1:
			goalflug, goalarea, goalGAP, photoname = GoalDetection("photo/photo",200 ,10, 120, 20000)
			print("goalarea",goalarea, "goalGAP", goalGAP)
	except KeyboardInterrupt:
		print('stop')
	except:
		print('error')