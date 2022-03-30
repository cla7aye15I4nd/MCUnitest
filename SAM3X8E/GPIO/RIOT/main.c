#include <stdio.h>
#include <board.h>
#include <periph/gpio.h>

int main(void) {
    gpio_init(ARDUINO_PIN_2, GPIO_IN);
    gpio_init(ARDUINO_PIN_13, GPIO_OUT);

    while(1){
        if (gpio_read(ARDUINO_PIN_2)) {
            gpio_set(ARDUINO_PIN_13);
        }
        else{
            gpio_clear(ARDUINO_PIN_13);
        }
    };
}