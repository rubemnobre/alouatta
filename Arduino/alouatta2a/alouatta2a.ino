#include <TimerOne.h>
#include <SoftwareSerial.h>

int useSerial = 0;
const int lorapin[] = {2, 3, 4, 5, 6};
const int sendpin = 11;

SoftwareSerial lora(lorapin[3], lorapin[2]);

int lorastate;

const int samples = 512;
const int frequency = 4000;
uint16_t amostras[samples];

void setup() {
  useSerial = 0;
  pinMode(lorapin[0], OUTPUT);
  pinMode(lorapin[1], OUTPUT);
  pinMode(sendpin, INPUT_PULLUP);
  digitalWrite(lorapin[0], LOW);
  digitalWrite(lorapin[1], LOW);
  attachInterrupt(digitalPinToInterrupt(lorapin[4]), loraevent, FALLING);
  attachInterrupt(digitalPinToInterrupt(sendpin), sendevent, FALLING);
  lora.begin(9600);
  Serial.begin(9600);
  Timer1.initialize(1e6 * ((double)1 / (double)frequency));
  Timer1.attachInterrupt(sampling);
}

volatile int samplen = 0;
void sampling() {
  if (samplen < samples) {
    amostras[samplen] = analogRead(0);
  }
  samplen++;
}

void loop() {
  if (samplen > samples) {
    Timer1.stop();
    byte buf[2];
    if (useSerial == 0) {
      for (int i = 0; i < 256; i++) {
        buf[0] = amostras[i] & 255;
        buf[1] = (amostras[i] >> 8)  & 255;
        lora.write(buf, 2);
      }
      while (digitalRead(lorapin[4]) == LOW);
      for (int i = 256; i < 512; i++) {
        buf[0] = amostras[i] & 255;
        buf[1] = (amostras[i] >> 8)  & 255;
        lora.write(buf, 2);
      }
      while (digitalRead(lorapin[4]) == LOW);
    } else {
      for (int i = 0; i < 512; i++) {
        buf[0] = amostras[i] & 255;
        buf[1] = (amostras[i] >> 8)  & 255;
        Serial.write(buf, 2);
      }
    }
    /*
      for (int i = 0; i < samples; i++) {
      byte buf[2];
      buf[0] = amostras[i] & 255;
      buf[1] = (amostras[i] >> 8)  & 255;
      Serial.write(buf, 2);
      }*/
    samplen = 0;
    Timer1.start();
    interrupts();
  }
  delay(1000);
}

void loraevent() {}


void sendevent() {
  Timer1.start();
  noInterrupts();
}
