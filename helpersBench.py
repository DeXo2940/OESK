from subprocess import Popen, PIPE

class CustomError(Exception):
	pass

commands = ["avr-gcc -Wall -g -Os -mmcu=<processor> -o main.bin <program>" , "avr-objcopy -j .text -j .data -O ihex main.bin main.hex", "avrdude -c <programator> -p <processor> -U flash:w:main.hex - P usb", "rm main.bin main.hex"]

atmegaFuse = {
	"atmega8:1MHz":"<l>0xE1:m <h>0xD9:m",
	"atmega8:2MHz":"<l>0xE2:m <h>0xD9:m",
	"atmega8:4MHz":"<l>0xD3:m <h>0xD9:m",
	"atmega8:8MHz":"<l>0xE4:m <h>0xD9:m", 
	"atmega8:extHigh":"<l>0xFF:m <h>0xD9:m",
	"atmega88p:8MHz":"<l>0x62:m <h>0xDF:m <e>0xF9:m",
	"atmega88p:128kHz":"<l>0x63:m <h>0xDF:m <e>0xF9:m",
	"atmega88p:extHigh":"<l>0x7F:m <h>0xDF:m <e>0xF9:m",
	"atmega328p:8MHz":"<l>0x62:m <h>0xD9:m <e>0xFF:m",
	"atmega328p:128kHz":"<l>0x63:m <h>0xD9:m <e>0xFF:m",
	"atmega328p:8MHz":"<l>0x7F:m <h>0xD9:m <e>0xFF:m"
}

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

def getFuse(procName, progrName = "usbasp"):
	command = "avrdude -c <programator> -p <processor> - P usb "
	command = command.replace("<processor>", procName).replace("<programator>", progrName)
	retCmd = []
	for fus in atmegaFuse.items():
		if procName + ":" in fus[0]:
			fs = command + fus[1].replace("<l>","-U lfuse:w:").replace("<h>","-U hfuse:w:").replace("<e>","-U efuse:w:")
			retCmd.append([fus[0], fs])
	return retCmd

def setFuse(cmd,log=True):
	print ("SetingFuses " + cmd[0])

	p = Popen(cmd[1], shell=True, stdout=PIPE, stderr=PIPE)
	out, err = p.communicate()
		
	if log == True:
		print(cmd[1])
		print(out)		
		print(err)	

	for line in err.splitlines():
		if "rc=-1" in line:
			raise CustomError(cmd[1], err)
