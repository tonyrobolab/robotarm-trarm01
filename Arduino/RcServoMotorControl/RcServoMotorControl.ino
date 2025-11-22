//--------------------------------------------------------------------------------
//  File      RcServoMotorControl.ino
//
//  Version   
//            v0.1  2025.11.05  Tony Kwon
//                Initial revision
//--------------------------------------------------------------------------------

//--------------------------------------------------------------------------------
//  Serial communication
//--------------------------------------------------------------------------------
#define SERIAL_BAUD 115200

void setupSerial() {
  Serial.begin(SERIAL_BAUD);
  while (! Serial);
}

//--------------------------------------------------------------------------------
//  Servo motor driver for PCA9685
//--------------------------------------------------------------------------------
#include <Adafruit_PWMServoDriver.h>

#define MOTOR_PWM_FREQ  50  // 50[Hz] frequency = 20[ms] period
#define MOTOR_CH_MAX    16
 
Adafruit_PWMServoDriver servoDriver = Adafruit_PWMServoDriver(0x40);

void setupMotor() {
  servoDriver.begin();
  servoDriver.setPWMFreq(MOTOR_PWM_FREQ);
  for(int i = 0; i < MOTOR_CH_MAX; i++) {
    servoDriver.setPWM(i, 0, 320);
  }
}

//--------------------------------------------------------------------------------
//  RX state process
//--------------------------------------------------------------------------------
#define RX_STATE_START  0
#define RX_STATE_COUNT  1
#define RX_STATE_DATA   2
#define RX_STATE_RUN    3

int rxState = RX_STATE_START;
int rxMotorCnt;
int rxDataCnt;
byte rxData[256];
byte rxDataPre = 0x00;

void processRxState(byte data, bool isRead) {

  //  'Start' state
  if(rxState == RX_STATE_START) {    
    if(isRead == true) {
      if(rxDataPre == 0xFF && data == 0xFF) {
        rxState = RX_STATE_COUNT;              
      }
    }

  //  'Count' state
  } else if(rxState == RX_STATE_COUNT) {
    if(isRead == true) {
      if(data == 0xFF || data == 0x00) {
        rxState = RX_STATE_START;
      } else {
        rxMotorCnt = data;
        rxDataCnt = 0;
        rxState = RX_STATE_DATA;      
      }
    }    
    
  //  'Data' state
  } else if(rxState == RX_STATE_DATA) {
    if(isRead == true) {    
      if(rxDataPre == 0xFF && data == 0xFF) {
        rxState = RX_STATE_COUNT;      
      } else {      
        rxData[rxDataCnt] = data;
        rxDataCnt++;
        if((rxMotorCnt * 2) <= rxDataCnt) {
          rxState = RX_STATE_RUN;
        }
      }
    }

  //  'Run' state
  } else if(rxState == RX_STATE_RUN) {    
    for(int i = 0; i < rxMotorCnt; i++) {
      int motorTick = (((int)rxData[i * 2]) << 8) + rxData[(i * 2) + 1];
      servoDriver.setPWM(i, 0, motorTick); 
    }    
    rxState = RX_STATE_START;

  //  Else
  } else {
    rxState = RX_STATE_START;
     
  }

  rxDataPre = data;
}

//--------------------------------------------------------------------------------
//  Setup
//--------------------------------------------------------------------------------
void setup() { 
  setupSerial();
  setupMotor();
}

//--------------------------------------------------------------------------------
//  Loop
//--------------------------------------------------------------------------------
void loop() {
  byte data;
  bool isRead = false;

  //  Read serial comm data
  if(Serial.available()) {
    data = Serial.read();  
    isRead = true;
  }

  //  Process RX state
  processRxState(data, isRead);  
}