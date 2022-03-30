#include <stdio.h>
#include <board.h>
#include <periph/adc.h>

int Error_Handler(void) {
    while (1);
}


int main(void)
{
    if (adc_init(ADC_LINE(0)) < 0)
        Error_Handler();

    if (adc_sample(ADC_LINE(0), ADC_RES_10BIT) < 0)
        Error_Handler();
    
    int v = adc_sample(ADC_LINE(0), ADC_RES_10BIT);
    printf("adc = %d\n", v);

    while (1) {        
    }

    return 0;
}