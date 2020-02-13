import serial
import numpy.fft
import matplotlib.pyplot as plt
import sys
import time
import struct
import subprocess

def readFromFile():
	dataSource = open("alo.bin", 'rb')
	n0 = int.from_bytes(dataSource.read(2), byteorder='little', signed=False)
	n1 = int.from_bytes(dataSource.read(2), byteorder='little', signed=False)
	output = []
	for i in range(n0):
		fmt = '>' + 'f'*n1
		output.append(list(struct.unpack(fmt, dataSource.read(4*n1))))
	dataSource.close()
	return output

def writeToFile(toWrite):
	n0 = len(toWrite)
	n1 = len(toWrite[0])
	dataSource = open("alo.bin", 'wb')
	dataSource.write(int.to_bytes(n0, 2, byteorder='little', signed=False))
	dataSource.write(int.to_bytes(n1, 2, byteorder='little', signed=False))
	for sublist in toWrite:
		for n in sublist:
			dataSource.write(struct.pack(">f", n))
	dataSource.close()
def appendToFile(toAppend):
	read = readFromFile()
	read.append(toAppend)
	writeToFile(read)

def getSamplesArray():
	#print("lendo")
	intArray = []
	bytes = arduino.read(1024)
	if len(bytes) == 1024:
		for x in range(512):
			pair = bytes[2*x : 2*x + 1]
			intArray.append(int.from_bytes(pair, byteorder='little', signed=False) - 511)
		#print("%d bytes lidos" % len(bytes))
		arduino.reset_input_buffer()
		return intArray
	else:
		arduino.reset_input_buffer()
		return []

portName = sys.argv[1]
arduino = serial.Serial(
	port=portName,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

st = 0
frequencies = []
for x in range(0, 256):
	frequencies.append(x*2000/256)
arduino.inter_byte_timeout = 2
arduino.reset_input_buffer()
prevBufferSize = 0
bufferTime = 0.0
rst = 0
while 1:
	if arduino.in_waiting > prevBufferSize:
		bufferTime = time.process_time()
		rst = 0
	if time.process_time() - bufferTime > 0.5 and rst == 0:
		arduino.reset_input_buffer()
		st = 0
		print('reset because deltat is %f' %(time.process_time() - bufferTime))
		rst = 1
	if arduino.in_waiting > 0 and st == 0:
		tstart = time.process_time()
		st = 1
	if arduino.in_waiting > 1023:
		sampleInput = getSamplesArray()
		st = 0
		if sampleInput != []:
			deltat = time.process_time() - tstart
			#print("%f segundos para receber" % deltat)
			compOutput = numpy.fft.rfft(sampleInput)
			realOutput = []
			for z in compOutput:
				realOutput.append(abs(z))
			#print("fft pronta")
			plt.ylabel('Magnitude')
			plt.xlabel('Frequência')
			plt.ylim(0, 25000)
			plt.plot(frequencies[2:256], realOutput[2:256])
			if sum(realOutput[2:256])/len(realOutput[2:256]) < max(realOutput[2:256])/4:
                               val = frequencies[realOutput.index(max(realOutput[2:256]))]
                               print(val)
                               if val > 600 and val < 1250:
                                       print("macaco!")
                                       subprocess.run(["python", "c://users/3aemaq21/downloads/alo/new.py", "a"])
			#plt.show()
			#input()
			##if save == '1':
			##	appendToFile(realOutput)
	prevBufferSize = arduino.in_waiting
