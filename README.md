# Alouatta
Final project for my formation as an electronics technician at Fundação Matias Machline in Manaus, Brazil.

## Hardware considerations
- You can adapt the Arduino code to match your hardware if you change the wiring.
- The LoRa module will work with the default settings, but reducing the Air Data Rate can make the transmission more reliable at longer ranges. The manual for the specified module can be found [here](http://www.ebyte.com/en/product-view-news.aspx?id=130). 
- The power source for the Node should match the voltage requirements of the [LM317T](https://www.st.com/resource/en/datasheet/lm217.pdf "Datasheet") Regulator and be able to deliver at least 500mA at peak (during transmission)
- To receive the data, use a LoRa receiver with matching settings (operating frequency, air data rate) and connect it to a serial port in the computer (you can use a UART-USB converter module)

## How to use the software
On the /Central directory, you will find `alouatta1f.py` and `new.py`. 
### Setting it up
- If you are running Windows, you might need to change the `subprocess.run(["python", "./new.py", "musa"])` line in `alouatta1f.py` to match the location of the `new.py` file to it's location in your machine.
- You need to change the `arquivo = open("C:/Users/3AEMAQ21/Desktop/log.txt", "a")` line in `new.py` to match your own log file location
### Running the Scripts
- You need [Python 3](https://www.python.org/downloads/ "Python Download page") with the following libraries:
  - [PySerial](https://pypi.org/project/pyserial/)  
  - [NumPy](https://pypi.org/project/numpy/)  
  - [Matplotlib](https://pypi.org/project/matplotlib/)  
- To start monitoring for new data, run:  
  `python3 ./Central/alouatta1f.py [insert serial port name here]`  
  or, depending on your system,  
  `python ./Central/alouatta1f.py [insert serial port name here]`  
