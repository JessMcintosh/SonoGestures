// 0 -> calibrate on relaxed, 1 -> calibrate closed thumb, 2 -> calibrated closed fingers, b -> begin capture, s -> stop capture


#define N_SENSORS 5

unsigned long lastTimeMicro;
boolean readyFlag = false;

int minVals[N_SENSORS] = {330, 320, 330, 360, 325};
int maxVals[N_SENSORS] = {600, 500, 600, 650, 650};
static const int sensorPin[N_SENSORS] = {0, 1, 2, 3, 4};

int sensorValues[N_SENSORS] = {500, 500, 500, 500, 500};

void setup() {

  for (int i = 0; i < N_SENSORS; ++i) {
    pinMode(sensorPin[i], INPUT);
  }

  Serial.begin(19200);
  delay(30);

}

void calibrateRelaxed() {
  Serial.println("Calibrating relaxed posture...");
  for (int i = 0; i < N_SENSORS; ++i)
    minVals[i] = analogRead(sensorPin[i]);
}

void calibrateClosedThumb() {
  Serial.println("Calibrating closed thumb...");
  maxVals[0] = analogRead(sensorPin[0]);
}

void calibrateClosedFingers() {
  Serial.println("Calibrating closed fingers...");
  for (int i = 1; i < N_SENSORS; ++i)
    maxVals[i] = analogRead(sensorPin[i]);
}

void loop() {
  // send data only when you have received "ready" command:
  if (readyFlag == true) {

    //write the timestamp
    const unsigned long currentMicros = millis();
    Serial.print( currentMicros - lastTimeMicro);
    Serial.print(" ");

    //write the data from the sensors
    for (int i = 0; i < N_SENSORS; i++) {
      // Smoothing to stop jagged movements
      //sensorValues[i] = (sensorValues[i]*0.5)+(analogRead(sensorPin[i])*0.5);

      sensorValues[i] = analogRead(sensorPin[i]);
      int v = map(sensorValues[i], minVals[i], maxVals[i], 0, 100);
      v = constrain(v, 0, 100);
      Serial.print(v);
      Serial.print(" ");
    }

    Serial.println();
    delay(20);
  }

}

// called once per loop after loop() function if there is data on the bus
void serialEvent() {

  for (int j = Serial.available(); j >= 0; --j) {
    char inChar = (char)Serial.read();
    if (inChar == '0') {
      calibrateRelaxed();
    } else if (inChar == '1') {
      calibrateClosedThumb();
    } else if (inChar == '2') {
      calibrateClosedFingers();
    } else if (inChar == 'b') { //start
      lastTimeMicro = millis();
      readyFlag = true;
    } else if (inChar == 's') { //stop
      readyFlag = false;
    }
  }

}
