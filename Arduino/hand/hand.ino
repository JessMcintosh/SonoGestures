// moves the fingers from 0 to 100. 10a moves thumb 10. 67c moves middle 67.

#include <Servo.h>


#define N_FINGERS 5

Servo myServo[N_FINGERS];
static const int FingerServo[N_FINGERS] = {3,5,10,6,9};
static const int FingerMin[N_FINGERS] = {180,180,0,177,180};
static const int FingerMax[N_FINGERS] = {107,87,125,50,105};

void setup() {

  //initialize the fingers
  for(int i = 0; i < N_FINGERS; ++i){
    myServo[i].attach( FingerServo[i] );
    myServo[i].write( FingerMin[i] );
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
        //if (v >= 0 && v <= 100){
          const int fingerN = ch - 'a';
          
          Serial.print("fingerN ");
          Serial.print(fingerN);
          Serial.print(" value ");
          Serial.print(v);
          v = map(v, 0, 100, FingerMin[fingerN], FingerMax[fingerN]);
          Serial.print(" angle ");
          Serial.println(v);

          
          myServo[fingerN].write( v );
        //}
        v = 0;
        break;
    }
  }

} 
