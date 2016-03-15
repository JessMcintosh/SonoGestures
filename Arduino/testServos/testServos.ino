// connect servos to the indicated pins. Send 90a to set the first servo at neutral position. Send 15c to rotate the 3rd servo towards 15deg.

#include <Servo.h>

#define N_SERVOS 5

static const int servoPin[N_SERVOS] = {3,5,6,9,10};
Servo myServo[N_SERVOS];


void setup() {

  for(int i = 0; i < N_SERVOS; ++i){
    myServo[i].attach( servoPin[i] );
  }  

  Serial.begin(115200);
  Serial.println("Ready");
  delay(30); 
}

void loop() {

  static int v = 0;

  if ( Serial.available()) {
    char ch = Serial.read();

    switch(ch) {
      case '0'...'9':
        v = v * 10 + ch - '0';
        break;
      case 'a' ... 'e':
        if (v >= 0 && v <= 180){
          const int servoN = ch - 'a';
          
          Serial.print("Servo ");
          Serial.print(servoN);
          Serial.print(" value ");
          Serial.println(v);
          
          myServo[servoN].write( v );
        }
        v = 0;
        break;
    }
  }

} 
