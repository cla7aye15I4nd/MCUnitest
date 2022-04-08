#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <periph/spi.h>
#include <board.h>

uint8_t data[] = "a";
int main(void)
{    
    spi_init(SPI_DEV(0));
    spi_acquire(SPI_DEV(0), SPI_CS_UNDEF, SPI_MODE_0, SPI_CLK_1MHZ);

    for (int i = 0; i < 10; ++i) {
        data[0] = spi_transfer_byte(SPI_DEV(0), SPI_CS_UNDEF, false, data[0]);
        printf("%c", data[0]);
    }

    spi_release(SPI_DEV(0));
   
    while(1) { };
    return 0;
}
