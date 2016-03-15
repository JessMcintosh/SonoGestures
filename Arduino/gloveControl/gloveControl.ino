// connect servos to the indicated pins. Send 90a to set the first servo at neutral position. Send 15c to rotate the 3rd servo towards 15deg.

#include <Servo.h>

#define N_SERVOS 5
#define N_SENSORS 5
#define N_FINGERS 5


char bufferByte;

int minVals[N_SENSORS] = {330, 320, 330, 360, 325};
int maxVals[N_SENSORS] = {600, 500, 600, 650, 650};
static const int sensorPin[N_SENSORS] = {0,1,2,3,4};
static const int FingerServo[N_FINGERS] = {3,5,10,6,9};
static const int FingerMin[N_FINGERS] = {180,180,0,177,180};
static const int FingerMax[N_FINGERS] = {107,87,125,50,105};
Servo myServo[N_SERVOS];

int sensorValues[N_SENSORS] = {500,500,500,500,500};
int servoValues[N_SERVOS] = {90,90,90,90,90};

void setup() {

  for(int i = 0; i < N_FINGERS; ++i){
    myServo[i].attach( FingerServo[i] );
    myServo[i].write( FingerMin[i] );
  } 
  for(int i = 0; i < N_SENSORS; ++i){
    pinMode(sensorPin[i], INPUT);
  }  

  Serial.begin(9600);
  Serial.println("Ready");
  delay(30); 
}

void calibrateRelaxed(){
  Serial.print("Calibrating relaxed posture...");
  for(int i = 0; i < N_SENSORS; ++i)
    minVals[i] = sensorValues[i];
}

void calibrateClosedThumb(){
  Serial.print("Calibrating closed thumb...");
  maxVals[0] = sensorValues[0];
}
  
void calibrateClosedFingers(){
  Serial.print("Calibrating closed fingers...");
  for(int i = 1; i < N_SENSORS; ++i)
    maxVals[i] = sensorValues[i];
}

void loop() {
    static int v = 0;
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    bufferByte = Serial.read();
    switch(bufferByte){
      case('r'):
        calibrateRelaxed();
        break;
      case('t'):
        calibrateClosedThumb();
        break;
      case('f'):
        calibrateClosedFingers();
        break;
    }
  }
  
  for(int i = 0; i < N_SENSORS; i++){
  //for(int i = 1; i < 2; ++i){
    // Smoothing to stop jagged movements
    sensorValues[i] = (sensorValues[i]*0.5)+(analogRead(sensorPin[i])*0.5);
    servoValues[i] = map(sensorValues[i], minVals[i], maxVals[i], 0, 100);  
    servoValues[i] = constrain(servoValues[i], 0, 100);
    v = map(servoValues[i], 0, 100, FingerMin[i], FingerMax[i]);
    myServo[i].write(v);
    Serial.print(v);
    Serial.print(" ");
  }
  delay(10);
  Serial.println();

} 
