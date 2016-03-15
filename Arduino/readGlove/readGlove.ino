// connect servos to the indicated pins. Send 90a to set the first servo at neutral position. Send 15c to rotate the 3rd servo towards 15deg.

#include <Servo.h>

#define N_SENSORS 5
#define N_FINGERS 5

unsigned long lastTimeMicro;

int stringBufferIndex = 0;
char stringBuffer[255];
boolean readyFlag = false;
int counter = 0;

#define START = 1
#define STOP = 0

char bufferByte;

int minVals[N_SENSORS] = {330, 320, 330, 360, 325};
int maxVals[N_SENSORS] = {600, 500, 600, 650, 650};
static const int sensorPin[N_SENSORS] = {0,1,2,3,4};

int sensorValues[N_SENSORS] = {500,500,500,500,500};

void setup() {

  for(int i = 0; i < N_SENSORS; ++i){
    pinMode(sensorPin[i], INPUT);
  }  
  
      // zero out string buffer for serial reads
    for(int i = 0; i < 255; i++) {
        stringBuffer[i] = '\0';
    }
    stringBufferIndex = 0;

  Serial.begin(9600);
  delay(30);
  
}

void calibrateRelaxed(){
  Serial.println("Calibrating relaxed posture...");
  for(int i = 0; i < N_SENSORS; ++i)
    minVals[i] = sensorValues[i];
}

void calibrateClosedThumb(){
  Serial.println("Calibrating closed thumb...");
  maxVals[0] = sensorValues[0];
}
  
void calibrateClosedFingers(){
  Serial.println("Calibrating closed fingers...");
  for(int i = 1; i < N_SENSORS; ++i)
    maxVals[i] = sensorValues[i];
}

void loop() {
    static int v = 0;
  // send data only when you have received "ready" command:
  if(readyFlag == true){
    /*
    const unsigned currentMicros = millis();
    Serial.print( currentMicros - lastTimeMicro);
    Serial.print(" "); */
   
    for(int i = 0; i < N_SENSORS; i++){
      // Smoothing to stop jagged movements
      sensorValues[i] = (sensorValues[i]*0.5)+(analogRead(sensorPin[i])*0.5);
      v = map(sensorValues[i], minVals[i], maxVals[i], 0, 100);  
      v = constrain(v, 0, 100);
      Serial.print(v);
      Serial.print(" ");
    }
    Serial.println();
    delay(50);
  }
} 

// called once per loop after loop() function if there is data on the bus
void serialEvent() {

    int bytes = Serial.available();
    for( int j = 0; j < bytes; j++ ) {
      char inChar = (char)Serial.read();
      if(inChar == '0')
        calibrateRelaxed();
      if(inChar == '1')
        calibrateClosedThumb();
      if(inChar == '2')
        calibrateClosedFingers();
    
      if( inChar == '\t' || inChar == '\n' || inChar == '\r' || inChar == ' ' ) {

          if(strcmp(stringBuffer, "ready") == 0) {
            //Serial.print(":READY:\n");
            // zero out string buffer for serial reads
            for(int i = 0; i < 255; i++) {
                stringBuffer[i] = '\0';
            }
            stringBufferIndex = 0;
            lastTimeMicro = millis();
            readyFlag = true;
          }

          if(strcmp(stringBuffer, "stop") == 0) {
            //Serial.print(":STOP:\n");
            //Serial.print(":Listening...:\n");
            // zero out string buffer for serial reads
            for(int i = 0; i < 255; i++) {
                stringBuffer[i] = '\0';
            }
            stringBufferIndex = 0;

            readyFlag = false;
          }

          // zero out string buffer
          for(int i = 0; i <= stringBufferIndex; i++) {
              stringBuffer[i] = '\0';
          }
          stringBufferIndex = 0;


      } else {
          stringBuffer[stringBufferIndex] = inChar;
          stringBufferIndex++;
      }
    }
}
