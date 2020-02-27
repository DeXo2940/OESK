from subprocess import Popen, PIPE

class CustomError(Exception):
	pass

commands = ["avr-gcc -Wall -g -Os -mmcu=<processor> -o main.bin <program>" , "avr-objcopy -j .text -j .data -O ihex main.bin main.hex", "avrdude -c <programator> -p <processor> -U flash:w:main.hex - P usb", "rm main.bin main.hex"]


def prepareFiles(procName, progName = "bench.c", progrName = "usbasp", log = True):
	print ("Preparing files")
	for cmd in commands:
		cmd = cmd.replace("<processor>", procName).replace("<program>", progName).replace("<programator>", progrName)
		p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
		out, err = p.communicate()
		
		if log == True:
			print(cmd)
			print(out)		
			print(err)

		for line in err.splitlines():
			if "error" in line or "Double check chip" in line:
				raise CustomError(cmd, err)		
	
	print ("Files ready")

def findProc(progrName = "usbasp", log = True):
	command = "avrdude -c <programator> -p atmega8 - P usb"

	print ("Identyfying microcontroler")
	command = command.replace("<programator>", progrName)

	p = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()
		
	if log == True:
		print(command)
		print(out)		
		print(err)	

	for line in err.splitlines():
		if "rc=-1" in line:
			raise CustomError(command, err)
		if "Device signature =" in line:
			device = line[line.find("(probably")+10:line.find(")")]
			return device.replace("m", "atmega")