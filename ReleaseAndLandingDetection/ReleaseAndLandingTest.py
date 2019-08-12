# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/pi/git/kimuralab/Detection/ParachuteDetection')
sys.path.append('/home/pi/git/kimuralab/Detection/ReleaseAndLandingDetection')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Calibration')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Goal')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/ParaAvoidance')
sys.path.append('/home/pi/git/kimuralab/IntegratedProgram/Running')
sys.path.append('/home/pi/git/kimuralab/Mission')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BME280')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/BMX055')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Camera')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/GPS')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/IM920')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Melting')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/Motor')
sys.path.append('/home/pi/git/kimuralab/SensorModuleTest/TSL2561')
sys.path.append('/home/pi/git/kimuralab/Other')

import binascii
import difflib
import numpy as np
import pigpio
import serial
import time
import traceback

import BMX055
import BME280
import Capture
import Calibration
import Goal
import GPS
import IM920
import Land
import Melting
import Motor
import Other
import ParaDetection
import ParaAvoidance
import Release
import RunningGPS
import TSL2561

phaseChk = 0	#variable for phase Check

# --- variable of time setting --- #
t_start  = 0.0				#time when program started
t_sleep = 10				#time for sleep phase
t_release = 360				#time for release(loopx)
t_land = 300				#time for land(loopy)
t_melt = 5					#time for melting
t_sleep_start = 0			#time for sleep origin
t_release_start = 0			#time for release origin
t_land_start = 0			#time for land origin
t_calib_origin = 0			#time for calibration origin
t_paraDete_start = 0
t_takePhoto_start = 0		#time for taking photo
timeout_calibration = 180	#time for calibration timeout
timeout_parachute = 60
timeout_takePhoto = 10		#time for taking photo timeout

# --- variable for storing sensor data --- #
gpsData = [0.0,0.0,0.0,0.0,0.0]						#variable to store GPS data
bme280Data = [0.0,0.0,0.0,0.0]						#variable to store BME80 data
bmx055data = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]	#variable to store BMX055 data

# --- variable for Judgement --- #
lcount = 0		#lux count for release
acount = 0		#press count for release
Pcount = 0		#press count for land
GAcount = 0
gacount=0		#GPSheight count for land
luxjudge = 0	#for release
pressjudge = 0	#for release and land
gpsjudge = 0	#for land
paraExsist = 0 	#variable for Para Detection    0:Not Exsist, 1:Exsist
goalFlug = -1	#variable for GoalDetection		-1:Not Detect, 0:Goal, 1:Detect
goalBuf = -1
goalArea = 0	#variable for goal area
goalGAP = -1	#variable for goal gap
H_min = 200		#Hue minimam
H_max = 10		#Hue maximam
S_thd = 120		#Saturation threshold

# --- variable for Running --- #
fileCal = "" 						#file path for Calibration
ellipseScale = [0.0, 0.0, 0.0, 0.0] #Convert coefficient Ellipse to Circle
disGoal = 100.0						#Distance from Goal [m]
angGoal = 0.0						#Angle toword Goal [deg]
angOffset = -77.0					#Angle Offset towrd North [deg]
gLat, gLon = 35.742532, 140.011542	#Coordinates of That time
nLat, nLon = 0.0, 0.0		  		#Coordinates of That time
nAng = 0.0							#Direction of That time [deg]
relAng = [0.0, 0.0, 0.0]			#Relative Direction between Goal and Rober That time [deg]
rAng = 0.0							#Median of relAng [deg]
mP, mPL, mPR, mPS = 0, 0, 0, 0		#Motor Power
kp = 0.8							#Proportional Gain
maxMP = 60							#Maximum Motor Power
mp_min = 20							#motor power for Low level
mp_max = 50							#motor power fot High level
mp_adj = 2							#adjust motor power

# --- variable of Log path --- #
phaseLog =			"/home/pi/log/phaseLog.txt"
sleepLog = 			"/home/pi/log/sleepLog.txt"
releaseLog = 		"/home/pi/log/releaseLog.txt"
landingLog = 		"/home/pi/log/landingLog.txt"
meltingLog = 		"/home/pi/log/meltingLog.txt"
paraAvoidanceLog = 	"/home/pi/log/paraAvoidanceLog.txt"
runningLog = 		"/home/pi/log/runningLog.txt"
goalDetectionLog =	"/home/pi/log/goalDetectionLog.txt"
captureLog = 		"/home/pi/log/captureLog.txt"
missionLog = 		"/home/pi/log/missionLog.txt"
calibrationLog = 	"/home/pi/log/calibrationLog"
errorLog = 			"/home/pi/log/erroLog.txt"

photopath = 		"/home/pi/photo/photo"
photoName =			""

pi=pigpio.pi()	#object to set pigpio


def setup():
	global phaseChk
	pi.set_mode(17,pigpio.OUTPUT)
	pi.set_mode(22,pigpio.OUTPUT)
	pi.write(22,1)					#IM920	Turn On
	pi.write(17,0)					#Outcasing Turn Off
	time.sleep(1)
	BME280.bme280_setup()
	BME280.bme280_calib_param()
	BMX055.bmx055_setup()
	GPS.openGPS()

	with open(phaseLog, 'a') as f:
		pass

	#if it is End to End Test, then
	try:
		phaseChk = int(Other.phaseCheck(phaseLog))
	except:
		phaseChk = 0
	#if it is debug
	phaseChk = 3

def close():
	GPS.closeGPS()
	pi.write(22, 1)		#IM920 Turn On
	pi.write(17,0)
	Motor.motor(0, 0, 1)
	Motor.motor_stop()


if __name__ == "__main__":
	try:
		print("Program Start  {0}".format(time.time()))
		t_start = time.time()

		#-----setup phase ---------#
		setup()
		print("Start Phase is {0}".format(phaseChk))
		if(phaseChk <= 1):
			IM920.Send("P1S")
			Other.saveLog(phaseLog, "1", "Program Started", time.time() - t_start)
			IM920.Send("P1F")

		# ------------------- Sleep Phase --------------------- #
		if(phaseChk <= 2):
			Other.saveLog(phaseLog, "2", "Sleep Phase Started", time.time() - t_start)
			print("Sleep Phase Started  {0}".format(time.time() - t_start))
			IM920.Send("P2S")
			#pi.write(22, 0)			#IM920 Turn Off
			t_sleep_start = time.time()

			# --- Sleep --- #
			while(time.time() - t_sleep_start <= t_sleep):
				Other.saveLog(sleepLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), TSL2561.readLux(), BMX055.bmx055_read())
				photoName = Capture.Capture(photopath)
				Other.saveLog(captureLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), photoName)
				time.sleep(1)
				IM920.Send("P2D")
			IM920.Send("P2F")

		# ------------------- Release Phase ------------------- #
		if(phaseChk <= 3):
			Other.saveLog(phaseLog, "3", "Release Phase Started", time.time() - t_start)
			t_release_start = time.time()
			print("Releasing Phase Started  {0}".format(time.time() - t_start))
			#IM920.Send("P3S")

			# --- Release Judgement, "while" is for timeout --- #
			while (time.time() - t_release_start <= t_release):
				#luxjudge,lcount = Release.luxjudge()
				pressjudge,acount = Release.pressjudge()
				t1 = time.time()
				if luxjudge == 1 or pressjudge == 1:
					Other.saveLog(releaseLog, time.time() - t_start, "Release Judged by Sensor", luxjudge, pressjudge)
					print("Rover has released")
					break
				else:
					print("Rover is in rocket")
					IM920.Send("P3D")
				# --- Save Log and Take Photo --- #
				gpsData = GPS.readGPS()
				Other.saveLog(releaseLog, time.time() - t_start, acount, gpsData, TSL2561.readLux(), BME280.bme280_read(), BMX055.bmx055_read())
				photoName = Capture.Capture(photopath)
				Other.saveLog(captureLog, time.time() - t_start, gpsData, BME280.bme280_read(), photoName)

				IM920.Send("P3D")
			else:
				Other.saveLog(releaseLog, time.time() - t_start, "Release Judged by Timeout")
				print("Release Timeout")
			pi.write(22, 1)	#Turn on IM920
			time.sleep(1)
			IM920.Send("P3F")

		# ------------------- Landing Phase ------------------- #
		if(phaseChk <= 4):
			Other.saveLog(phaseLog, "4", "Landing Phase Started", time.time() - t_start)
			print("Landing Phase Started  {0}".format(time.time() - t_start))
			IM920.Send("P4S")
			t_land_start = time.time()

			# --- Landing Judgement, "while" is for timeout --- #
			while(time.time() - t_land_start <= t_land):
				pressjudge, Pcount = Land.pressjudge()
				#gpsjudge, gacount = Land.gpsjudge()

				if pressjudge == 1: #and gpsjudge == 1:
					Other.saveLog(landingLog, time.time() - t_start, "Land Judged by Sensor", pressjudge, gpsjudge)
					print("Rover has Landed")
					break
				elif pressjudge == 0: #and gpsjudge == 0:
				    print("Descend now taking photo")
				#elif pressjudge == 1 : #or gpsjudge == 1:
				#print("Landing JudgementNow")
				
				# --- Save Log and Take Photo--- #
				for i in range(3):
					Other.saveLog(landingLog ,time.time() - t_start, Pcount, gacount, GPS.readGPS(), BME280.bme280_read(), BMX055.bmx055_read())
					photoName = Capture.Capture(photopath)
					Other.saveLog(captureLog, time.time() - t_start, GPS.readGPS(), BME280.bme280_read(), photoName)

				IM920.Send("P4D")
			else:
				Other.saveLog(landingLog, time.time() - t_start, "Landing Judged by Timeout")
				print("Landing Timeout")
			IM920.Send("P4F")

		# ------------------- Melting Phase ------------------- #
		if(phaseChk <= 5):
			Other.saveLog(phaseLog,"5", "Melting Phase Started", time.time() - t_start)
			print("Melting Phase Started")
			IM920.Send("P5S")
			Other.saveLog(meltingLog, time.time() - t_start, GPS.readGPS(), "Melting Start")
			Melting.Melting(t_melt)
			Other.saveLog(meltingLog, time.time() - t_start, GPS.readGPS(), "Melting Finished")
			IM920.Send("P5F")
	except KeyboardInterrupt:
		close()
		print("Keyboard Interrupt")
		IM920.Send("KI")
	except:
		close()
		print(traceback.format_exc())
		Other.saveLog(errorLog, time.time() - t_start, "Error")
		Other.saveLog(errorLog, traceback.format_exc())
		Other.saveLog(errorLog, "\n")
		IM920.Send("EO")
