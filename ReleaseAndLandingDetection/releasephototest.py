
import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
import cv2
import numpy as np
import math
import Capture

def DarkDetection(imgpath, V_thd, D_thd):
	global i
	try:
		imgname = Capture.Capture(imgpath)
		img = cv2.imread(imgname)

		#make mask
		img_HSV = cv2.cvtColor(cv2.GaussianBlur(img,(15,15),0),cv2.COLOR_BGR2HSV_FULL)
		h = img_HSV[:, :, 0]
		s = img_HSV[:, :, 1]
		v = img_HSV[:, :, 2]
		mask = np.zeros(h.shape, dtype=np.uint8)
		mask[v < V_thd] = 255

		#black area
		area = countNonZero(mask)
		print('area is',area)
        
		if area > D_thd:
			return [0, area, imgname]
		else:
			return [1, area, imgname]

	except:
		print('error')
		return [1, 0,  "Null"]

if __name__ == "__main__":
	try:
		while 1:
			Darkflug, DarkArea, photoname = DarkDetection("/home/pi/photo/photo", 40, 30000)
			print("Darkflug", Darkflug, "DarkArea",DarkArea, "name", photoname)
	except KeyboardInterrupt:
		print('stop')
	except:
		print('error')
