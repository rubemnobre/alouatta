#Written by Rubem Nobre, you can find me at github.com/rubemnobre and linkedin.com/in/rubemjrx

import serial
import numpy.fft
import matplotlib.pyplot as plt
import sys
import time
import struct
import subprocess

#reads the 512 uint16_t samples from serial (the lora module or the actual node in debugging mode) to an integer array
def getSamplesArray():
	intArray = []
	bytes = arduino.read(1024)
	if len(bytes) == 1024: #checks if the serial buffer returned the right amount of data (it might not, if out of sync)
		for x in range(512):
			#the data is sent in byte pairs, so it gets converted before appending to the output array
			pair = bytes[2*x : 2*x + 1]
			intArray.append(int.from_bytes(pair, byteorder='little', signed=False) - 511) #removes the offset added by the amp before transmisson
		arduino.reset_input_buffer() #clear the input buffer
		return intArray
	else:
		arduino.reset_input_buffer() #clear the input buffer
		return []

portName = sys.argv[1] #the serial port name is read from the cli argument

#initializing the arduino Serial object
arduino = serial.Serial(
	port=portName,
	baudrate=9600,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

st = 0 #indicates if there is data in the buffer

frequencies = []
for x in range(0, 256):
	frequencies.append(x*2000/256) #calculate the frequencies in the 2kHz range in the 256 steps of the output data

arduino.inter_byte_timeout = 2
arduino.reset_input_buffer()
prevBufferSize = 0
bufferTime = 0.0

rst = 0 #indicates if the timing has been reset so it does not reset repeatedly when there is no new data
while 1:
	#these checks are intended to sync the data receiving timing
	if arduino.in_waiting > prevBufferSize: 
		bufferTime = time.process_time()
		rst = 0
	if time.process_time() - bufferTime > 0.5 and rst == 0: #resets the input buffer if the time between two bytes is > 0.5s
		arduino.reset_input_buffer()
		st = 0
		print('reset because deltat is %f' %(time.process_time() - bufferTime))
		rst = 1

#	if arduino.in_waiting > 0 and st == 0:
#		tstart = time.process_time() #gets the time the transmission starts for debugging
#		st = 1
	
	if arduino.in_waiting > 1023: 
		sampleInput = getSamplesArray()
		st = 0
		if sampleInput != []:
			#deltat = time.process_time() - tstart #measuring the time it took to receive all the data
			#print("%f segundos para receber" % deltat)
			compOutput = numpy.fft.rfft(sampleInput) #calculate the fft of the input data (time -> frequency) using NumPy
			realOutput = []
			for z in compOutput:
				realOutput.append(abs(z)) #converts the complex output to absolute values

			#sets up a plot to show the output to the user
			#note the first two numbers and the second half of the data is ommited because of 
			#the limitations of this implementation of the fourier transforms
			plt.ylabel('Magnitude')
			plt.xlabel('Frequência')
			plt.ylim(0, 25000)
			plt.plot(frequencies[2:256], realOutput[2:256]) #
			if sum(realOutput[2:256])/len(realOutput[2:256]) < max(realOutput[2:256])/4:
                               val = frequencies[realOutput.index(max(realOutput[2:256]))]
                               print(val)
                               if val > 600 and val < 1250: #checks if the amplitude peak is in the expected frequency range for the purpose of the project
                            	       print("macaco!")
									   #run the new.py script that logs the detection to a .txt file, the second argument indicates the data origin in the log
                            	       subprocess.run(["python", "./new.py", "musa"]) #you may have to put in the whole path to run this in windows
	prevBufferSize = arduino.in_waiting
