import sys
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
import time
import serial
import pigpio
import BME280
import BMX055
import IM920
import GPS
bme280Data = [0.0,0.0]
deltAmax=0.5
acount=0
launchpressjudge=0
secondlatestPRESS = 0.0 #prevent first error judgemnt
latestPRESS = 0.0

def launchpressjudge():
    global bme280data
    global acount
    secondlatestPRESS = bme280Data[1]
    bme280Data = BME280.bme280_read()	
    latestPRESS = bme280Data[1]
    deltA = secondlatestPRESS-latestPRESS 

    if deltA>deltAmax:
        acount += 1
    elif deltA<deltAmax:
        acount = 0
    if acount>4:
        pressjudge = 1
		#print("presjudge")
    else:
        pressjudge=0
    print(str(latestPRESS)+"	:	"+str(secondlatestPRESS)+"	:	"+str(deltA))
    return pressjudge,acount

