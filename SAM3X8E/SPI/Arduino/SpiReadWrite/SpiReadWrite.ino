#include <SPI.h>

void setup() {
    Serial.begin(115200);
    // initialize the bus for the device on pin 4
    SPI.begin(4);

    // Set clock divider on pin 4 to 21
    SPI.setClockDivider(4, 21);

    // initialize the bus for the device on pin 10
    SPI.begin(10);

    // Set clock divider on pin 10 to 84
    SPI.setClockDivider(10, 84);

    pinMode(LED_BUILTIN, OUTPUT);
    
    byte rep = 0xee;

    for (int i = 0; i < 10; ++i) {
        rep = SPI.transfer(10, rep, SPI_CONTINUE);
        Serial.write(rep);
    }
}

void loop() {
    
}
