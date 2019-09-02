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
luxmax = 100
deltAmax = 0.25
pressjudge = 0
luxjudge = 0
photojudge = 0
secondlatestPRESS = 0.0 #prevent first error judgemnt
latestPRESS = 0.0

def luxdetect():
	global lcount
	luxjudge = 0
	try:
		luxdata = TSL2561.readLux()
		if luxdata[0]>luxmax or luxdata[1]>luxmax:
			lcount += 1
			if lcount>4:
				luxjudge = 1
				#print("luxreleasejudge")
		else:
			luxjudge = 0
			lcount = 0
		#print("lux"+"	"+str(luxdata[0])+"	:	"+str(luxdata[1]))
	except:
		print(traceback.format_exc())
		lcount = 0
		luxjudge = 2
	finally:
		return luxjudge, lcount

def pressdetect():
	global bme280Data
	global acount
	pressjudge = 0
	try:
		secondlatestPRESS = bme280Data[1]
		bme280Data = BME280.bme280_read()	#更新
		latestPRESS = bme280Data[1]
		deltA = latestPRESS - secondlatestPRESS
		if 0.0 in bme280Data:
			print("BMEerror!")
			pressjudge=2
			acount=0
		elif deltA>deltAmax:
			acount += 1
			if acount>4:
				pressjudge = 1
				#print("presjudge")
		elif deltA<deltAmax:
			acount = 0

		else:
			pressjudge=0
		#print(str(latestPRESS)+"	:	"+str(secondlatestPRESS)+"	:	"+str(deltA))
	except:
		print(traceback.format_exc())
		acount = 0
		pressjudge = 2
	finally:
		return pressjudge,acount

def photoreleasedetect(photoname):
	global fcount
	photojudge = 0
	img = cv2.imread(photoname,1) # 0=grayscale, 1=color
	hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	print("Shape: {0}".format(hsv.shape))
	print("Salute(mean): %.2f" % (hsv.T[1].flatten().mean()))
	print("Value(mean): %.2f" % (hsv.T[2].flatten().mean()))
	print(int(hsv.T[2].flatten().mean()))
	brightness=int(hsv.T[2].flatten().mean())
	if brightness>100:
		fcount+=1
		if fcount > 5:
			photojudge=1
	elif brightness<=200:
		fcount=0
	else:
		photojudge=0
	return photojudge,fcount

if __name__ == "__main__":
	photoname = "/home/pi/photo/photo34.jpg"
	photoreleasedetect(photoname)
	print("finish")
