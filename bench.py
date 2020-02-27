#!/usr/bin/env python
# -*- coding: utf-8 -*-

import helpersBench
import OPi.GPIO as GPIO

from time import sleep, time

outPin = 16
inPin = 7

GPIO.setboard(GPIO.PCPCPLUS)    # Orange Pi PC board
GPIO.setmode(GPIO.BOARD)        # set up BOARD BCM numbering
GPIO.setup(outPin, GPIO.OUT)
GPIO.setup(inPin, GPIO.IN)

progName = "bench.c"	# <program>
progrName = "usbasp"	# <programator>

log = False

numbersOfRevolutions = 10

plotData = []

try:
	GPIO.output(outPin, 0) 
	procName = helpersBench.findProc(progrName, log) #find what is this microcontroler
	fuses = helpersBench.getFuse(procName)
	helpersBench.prepareFiles(procName, log = log) #perpare hex for microcontroler
	print(procName)

	if not fuses:
		raise helpersBench.CustomError(["Unsuported Microcontroler"])
	
	for fuse in fuses:
		helpersBench.setFuse(fuse,log)	#set h,l,e Fuses
		
		print("START")
		totalTime = 0
		for i in range(0, numbersOfRevolutions):		
			GPIO.output(outPin, 1)       # avr start computing
			startTime = time()
			while(GPIO.input(inPin) == 0): #wait for avr to finish
				pass
			GPIO.output(outPin, 0) 		
			while(GPIO.input(inPin) == 1): #wait for avr to reset
				pass
			elapsedTime = time() - startTime
			totalTime += elapsedTime
			plotData.append(elapsedTime)
	
	
		print("meanTime = " + str(totalTime/numbersOfRevolutions))
		#print(plotData)
except KeyboardInterrupt:
	print (" Keyboard interupt")
except helpersBench.CustomError as err:
	print("Error occured:")
	for e in err:
		print(e)
finally:
	GPIO.output(outPin, 0)       
	GPIO.cleanup()              # Clean GPIO