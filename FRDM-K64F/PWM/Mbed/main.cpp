#include "mbed.h"

//PWM output channel
PwmOut PWM1(A5);

int main() 
{
    PWM1.period_ms(500);
    
    while (1) {
        for (int x = 1; x < 500; x++) {
            PWM1.pulsewidth_ms(x);
            wait(.1);
        }
    }
}

// compiled on online compiler