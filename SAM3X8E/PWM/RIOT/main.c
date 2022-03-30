#include <stdio.h>
#include <board.h>
#include <periph/pwm.h>

int main(void) {
    pwm_init(PWM_DEV(0), PWM_LEFT, 1000, 10);
    pwm_set(PWM_DEV(0), 1, 100);
    pwm_poweroff(PWM_DEV(0)); 
    pwm_poweron(PWM_DEV(0));

    while(1);

    return 0;
}