#define echoPinLeft 3
#define triggerPinLeft 2

#define echoPinRight 5
#define triggerPinRight 4

unsigned long durationLeft, durationRight;
unsigned long distanceLeft, distanceRight;

unsigned long distanceLeftFiltered = 0;
unsigned long distanceLeftDelay = 0;
unsigned long distanceRightFiltered = 0;
unsigned long distanceRightDelay = 0;

bool flip = false;

void setup() {
  // setup the first sensor
  pinMode(triggerPinLeft, OUTPUT);
  pinMode(echoPinLeft, INPUT);
  
  // setup the second sensor
  pinMode(triggerPinRight, OUTPUT);
  pinMode(echoPinRight, INPUT);

  Serial.begin(115200);
}

void loop() {
  if(flip == false)
  {
    digitalWrite(triggerPinLeft, LOW);
    delayMicroseconds(2);
  
    digitalWrite(triggerPinLeft, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPinLeft, LOW);
  
    durationLeft = pulseIn(echoPinLeft, HIGH, 10000);

    distanceLeft = durationLeft * 0.034 / 2;

    distanceLeftFiltered = (((distanceLeftDelay + distanceLeft) >> 1) + distanceLeftFiltered * 15) >> 4;
    distanceLeftDelay = distanceLeft;
  
//    distanceLeftFiltered = (((distanceLeftDelay + durationLeft) >> 1) + distanceLeftFiltered * 15) >> 4;
//    distanceLeftDelay = durationLeft;
//    distanceLeft = distanceLeftFiltered * 0.034 / 2;
    
    Serial.write(distanceLeftFiltered);
    Serial.write(0);
  }
  else
  {
    digitalWrite(triggerPinRight, LOW);
    delayMicroseconds(2);
  
    digitalWrite(triggerPinRight, HIGH);
    delayMicroseconds(10);
    digitalWrite(triggerPinRight, LOW);
  
    durationRight = pulseIn(echoPinRight, HIGH, 10000);

    distanceRight = durationRight * 0.034 / 2;

    distanceRightFiltered = (((distanceRightDelay + distanceRight) >> 1) + distanceRightFiltered * 15) >> 4;
    distanceRightDelay = distanceRight;
  
//    distanceRightFiltered = (((distanceRightDelay + durationRight) >> 1) + distanceRightFiltered * 15) >> 4;
//    distanceRightDelay = durationRight;
//    distanceRight = distanceRightFiltered * 0.034 / 2;

    Serial.write(distanceRightFiltered);
    Serial.write(1);
  }

//  Serial.println(distanceLeftFiltered);
//  Serial.print(",");
//  Serial.println(distanceRightFiltered);
  flip = !flip;
  delay(10);
}
