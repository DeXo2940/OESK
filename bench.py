#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helpersBench
import OPi.GPIO as GPIO

from time import time
from datetime import datetime

outPin = 16
inPin = 7

GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board
GPIO.setmode(GPIO.BOARD)        # set up BOARD BCM numbering
GPIO.setup(outPin, GPIO.OUT)
GPIO.setup(inPin, GPIO.IN)

progName = "bench.c"	# <program>
progrName = "usbasp"	# <programator>
fileName = "results.csv" # result file

log = False

numbersOfRevolutions = 1000

plotData = []

try:
	GPIO.output(outPin, 0) 
	procName = helpersBench.findProc(progrName, log) #find what is this microcontroler
	fuses = helpersBench.getFuse(procName)
	helpersBench.prepareFiles(procName, log = log) #perpare hex for microcontroler
	print(procName)
	dateTime = datetime.now().strftime("%d/%m/%y_%H:%M")

	if not fuses:
		raise helpersBench.CustomError(["Unsuported Microcontroler"])
	
	f = open(fileName,"a")

	for fuse in fuses:
		helpersBench.setFuse(fuse,log)	#set h,l,e Fuses
		
		plotPrint = ""
		for i in range(0, numbersOfRevolutions):		
			GPIO.output(outPin, 1)       # avr start computing
			startTime = time()
			while(GPIO.input(inPin) == 0): #wait for avr to finish
				pass
			GPIO.output(outPin, 0) 		
			while(GPIO.input(inPin) == 1): #wait for avr to reset
				pass
			elapsedTime = time() - startTime
			plotData.append(elapsedTime)
			plotPrint += "\t"+str(elapsedTime)
	
		#print("meanTime = " + str(totalTime/numbersOfRevolutions))
		#print(plotData)
		f.write(dateTime+"\t"+fuse[0]+plotPrint+"\n")

except KeyboardInterrupt:
	print (" Keyboard interupt")
except helpersBench.CustomError as err:
	print("Error occured:")
	for e in err:
		print(e)
finally:
	GPIO.output(outPin, 0)       
	GPIO.cleanup()              # Clean GPIO
	f.close()