#include <stdio.h>
#include <board.h>
#include <periph/gpio.h>

int main(void) {
    gpio_init(BTN0_PIN, GPIO_IN);
    gpio_init(LED0_PIN, GPIO_OUT);

    while(1){
        if (gpio_read(BTN0_PIN)) {
            gpio_write(LED0_PIN, 1);
        } else {
            gpio_write(LED0_PIN, 0);
        }
    };
}