#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helpersBench
import OPi.GPIO as GPIO

outPin = 16
inPin = 7
 

from time import sleep, time     
 
GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board
GPIO.setmode(GPIO.BOARD)        # set up BOARD BCM numbering
GPIO.setup(outPin, GPIO.OUT)
GPIO.setup(inPin, GPIO.IN)

progName = "bejch.c"	# <program>
progrName = "usbasp"	# <programator>

log = False

numbersOfRevolutions = 10

plotData = []

try:
	procName = helpersBench.findProc(progrName, log)
	helpersBench.prepareFiles(procName, log = log)
	
	GPIO.output(outPin, 0) 

	print("START")
	totalTime = 0
	for i in range(0, numbersOfRevolutions):

		GPIO.output(outPin, 1)       # avr start computing
		startTime = time()
		while(GPIO.input(inPin) == 0): #wait for avr to finish
			pass
		while(GPIO.input(inPin) == 1): #wait for avr to reset
			pass
		elapsedTime = time() - startTime
		GPIO.output(outPin, 0) 

		totalTime += elapsedTime
		
		plotData.append(elapsedTime)
		
		
	print("meanTime = " + str(totalTime/numbersOfRevolutions))
	print(plotData)
except KeyboardInterrupt:
	print (" Keyboard interupt")
except helpersBench.CustomError as err:
	print("Error occured:")
	for e in err:
		print(e)
finally:
	GPIO.output(outPin, 0)       
	GPIO.cleanup()              # Clean GPIO