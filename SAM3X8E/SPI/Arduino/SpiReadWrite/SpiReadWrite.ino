#include <SPI.h>

void setup() {
    // initialize the bus for the device on pin 4
    SPI.begin(4);

    // Set clock divider on pin 4 to 21
    SPI.setClockDivider(4, 21);

    // initialize the bus for the device on pin 10
    SPI.begin(10);

    // Set clock divider on pin 10 to 84
    SPI.setClockDivider(10, 84);

    pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
    //transfer 0x0F to the device on pin 10, keep the chip selected
    SPI.transfer(10, 0xF0, SPI_CONTINUE);

    //transfer 0x00 to the device on pin 10, keep the chip selected
    SPI.transfer(10, 0x00, SPI_CONTINUE);

    // //transfer 0x00 to the device on pin 10, store byte received in response1, keep the chip selected
    byte response1 = SPI.transfer(10, 0x00, SPI_CONTINUE);

    // //transfer 0x00 to the device on pin 10, store byte received in response2, deselect the chip
    byte response2 = SPI.transfer(10, 0x00);

    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
