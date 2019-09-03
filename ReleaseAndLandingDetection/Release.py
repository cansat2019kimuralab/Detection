import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
import time
import serial
import pigpio
import BME280
import BMX055
import IM920
import GPS
import TSL2561
import Capture
import cv2
import traceback
luxdata = []
bme280Data = [0.0,2000.0]
lcount = 0
acount = 0
fcount = 0

pressreleasejudge = 0
luxreleasejudge = 0
photoreleasejudge = 0
secondlatestPRESS = 0.0 #prevent first error judgemnt
latestPRESS = 0.0

def luxdetect(luxreleaseThd):
	global lcount
	luxreleasejudge = 0
	try:
		luxdata = TSL2561.readLux()
		if luxdata[0]>luxreleaseThd or luxdata[1]>luxreleaseThd:
			lcount += 1
			if lcount>4:
				luxreleasejudge = 1
				#print("luxreleasejudge")
		else:
			luxreleasejudge = 0
			lcount = 0
		#print("lux"+"	"+str(luxdata[0])+"	:	"+str(luxdata[1]))
	except:
		print(traceback.format_exc())
		lcount = 0
		luxreleasejudge = 2
	finally:
		return luxreleasejudge, lcount

def pressdetect(pressreleaseThd):
	global bme280Data
	global acount
	pressreleasejudge = 0
	try:
		secondlatestPRESS = bme280Data[1]
		bme280Data = BME280.bme280_read()	#update
		latestPRESS = bme280Data[1]
		deltA = latestPRESS - secondlatestPRESS
		if 0.0 in bme280Data:
			print("BMEerror!")
			pressreleasejudge=2
			acount=0
		elif deltA>pressreleaseThd:
			acount += 1
			if acount>4:
				pressreleasejudge = 1
				#print("presjudge")
		elif deltA<pressreleaseThd:
			acount = 0

		else:
			pressreleasejudge=0
		#print(str(latestPRESS)+"	:	"+str(secondlatestPRESS)+"	:	"+str(deltA))
	except:
		print(traceback.format_exc())
		acount = 0
		pressreleasejudge = 2
	finally:
		#pressreleasejudge =2 #for debug
		return pressreleasejudge,acount

def photoreleasedetect(photoName,photoreleaseThd):
	global fcount
	photoreleasejudge = 0
	img = cv2.imread(photoName,1) # 0=grayscale, 1=color
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	print("Shape: {0}".format(hsv.shape))
	print("Salute(mean): %.2f" % (hsv.T[1].flatten().mean()))
	print("Value(mean): %.2f" % (hsv.T[2].flatten().mean()))
	print(int(hsv.T[2].flatten().mean()))
	brightness=int(hsv.T[2].flatten().mean())
	if brightness>photoreleaseThd:
		fcount+=1
		if fcount > 5:
			photoreleasejudge=1
	elif brightness<=photoreleaseThd:
		fcount=0
	else:
		photoreleasejudge=0
	return photoreleasejudge,fcount

if __name__ == "__main__":
	photoName = "/home/pi/photo/photo34.jpg"
	photoreleaseThd=100
	photoreleasedetect(photoName,photoreleaseThd)
	print("finish")
