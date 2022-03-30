#include <stdio.h>
#include <board.h>
#include <periph/dac.h>

int Error_Handler(void) {
    while (1);
}

int main(void)
{
    if (dac_init(ARDUINO_DAC0) != DAC_OK)
        Error_Handler();
    dac_set(ARDUINO_DAC0, 2047);
    
    puts("ok");
    while(1) {}

    return 0;
}
