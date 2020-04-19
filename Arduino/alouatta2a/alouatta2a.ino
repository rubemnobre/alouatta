//Written by Rubem Nobre, you can find me at github.com/rubemnobre and linkedin.com/in/rubemjrx

#include <TimerOne.h>
#include <SoftwareSerial.h>

#define M0  lorapin[0]
#define M1  lorapin[1]
#define RX  lorapin[2]
#define TX  lorapin[3]
#define AUX lorapin[4]

int useSerial = 0; //this variable defines if the data output goes through the R232 port or the LoRa module (it exists for debugging)
const int lorapin[] = {2, 3, 4, 5, 6}; //these variables represent how the LoRa is wired to the microcontroller, as follows: M0 M1 RX TX AUX

SoftwareSerial lora(lorapin[3], lorapin[2]); //sets up a SoftwareSerial port with the LoRa module

//this sets the settings for the sound capturing
const int bufferSize = 512; //LoRa module buffer size in bytes
const int samples = 512; //number of samples per transmission (samples take two bytes), always a power of 2
const int frequency = 4000; //sampling frequency
uint16_t amostras[samples]; //sample data stack

void setup() {
  useSerial = 0;
  pinMode(M0, OUTPUT); //setting the M0 and M1 as outputs 
  pinMode(M1, OUTPUT);
  pinMode(sendpin, INPUT_PULLUP);
  digitalWrite(lorapin[0], LOW); //setting the LoRa mode pins to Mode 0
  digitalWrite(lorapin[1], LOW);
  attachInterrupt(digitalPinToInterrupt(AUX), loraevent, FALLING); //assigns a function to treat an event signaled by the AUX pin
  lora.begin(9600);
  Serial.begin(9600);
  Timer1.initialize(1e6 * ((double)1 / (double)frequency)); //set the sampling function timing on microsseconds
  Timer1.attachInterrupt(sampling);
}

volatile int samplen = 0;

//sampling function
void sampling() {
  if (samplen < samples) {
    amostras[samplen] = analogRead(0);
  }
  samplen++;
}

void loop() {
  if (samplen > samples) {
    Timer1.stop(); //stops the timer, so no timer interrupts while this procedure is running

    while (digitalRead(AUX) == LOW); //wait until the LoRa module is free to start sending data

    byte buf[2];
    if (useSerial == 0) {
      for (int i = 0; i < samples; i++) {
        //if the ammount of data to be transmitted is larger than the module buffer, wait until the end of the LoRa transmission
        if(i != 0 && i % bufferSize/2 == 0)
          while (digitalRead(AUX) == LOW); //the aux pin goes LOW when the module is transmitting data, so the loop will only exit when it's done
        
        //the write function only takes a single byte or a byte array, so this splits the uint16 to a 2-byte array and writes it
        buf[0] = amostras[i] & 255;
        buf[1] = (amostras[i] >> 8)  & 255;
        lora.write(buf, 2); 
      }
    } else {
      //send debugging data in the same format so the same software can be used in the receiving end
      for (int i = 0; i < 512; i++) {
        buf[0] = amostras[i] & 255;
        buf[1] = (amostras[i] >> 8)  & 255;
        Serial.write(buf, 2);
      }
    }
    samplen = 0;
    Timer1.start();
    interrupts();
  }
  delay(1000); //deliberately stop the node every cycle as a power saving measure
}

void loraevent() {}