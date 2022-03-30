#include "DueTimer.h"

int myLed = 13;

bool ledOn = false;
void myHandler(){
	ledOn = !ledOn;

	digitalWrite(LED_BUILTIN, ledOn);
}

void setup(){
	pinMode(myLed, OUTPUT);

	Timer3.attachInterrupt(myHandler);
	Timer3.start(50000);
}

void loop(){
	while(1) {}
}
