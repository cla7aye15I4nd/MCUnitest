#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <periph/spi.h>
#include <board.h>

int main(void)
{    
    spi_init(SPI_DEV(0));
    spi_acquire(SPI_DEV(0), SPI_CS_UNDEF, SPI_MODE_0, SPI_CLK_1MHZ);

    uint8_t data = 'a';   
    data = spi_transfer_byte(SPI_DEV(0), SPI_CS_UNDEF, false, data);

    spi_release(SPI_DEV(0));
   
    while(1) { };
    return 0;
}
