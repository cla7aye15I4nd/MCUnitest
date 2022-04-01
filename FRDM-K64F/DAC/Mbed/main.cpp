#include "mbed.h"
 
// DAC 20khz
#define DAC_Frequency 20000
 
AnalogOut dac(DAC0_OUT);


int main()
{
    dac = sin(1 * 3.14f * 2 / (1000000 / 262)) / 2.0f + 0.5f;
    dac = sin(2 * 3.14f * 2 / (1000000 / 262)) / 2.0f + 0.5f;
    dac = sin(3 * 3.14f * 2 / (1000000 / 262)) / 2.0f + 0.5f;
 
    while(1) {
    }
}
 