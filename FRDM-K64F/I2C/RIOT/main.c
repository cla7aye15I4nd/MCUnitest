#include <stdio.h>
#include <board.h>
#include <periph/i2c.h>

int  main(void){
    int device_addr = 0x03;
    int reg_addr = 0x01;
    int reg_value = 0;

    char reg_data[2];

    reg_data[0] = 0xde;
    reg_data[1] = 0xbe;

    i2c_init(I2C_DEV(0));
    i2c_acquire(I2C_DEV(0));
    i2c_write_byte(I2C_DEV(0), device_addr, reg_addr, (I2C_NOSTOP | I2C_ADDR10));
    i2c_read_byte(I2C_DEV(0), device_addr, &reg_value, I2C_ADDR10);
    i2c_release(I2C_DEV(0));

    i2c_init(I2C_DEV(0));
    i2c_acquire(I2C_DEV(0));
    i2c_write_byte(I2C_DEV(0), device_addr, reg_addr, I2C_NOSTOP);
    i2c_write_bytes(I2C_DEV(0), device_addr, reg_data, 2, 0);
    i2c_release(I2C_DEV(0));

    while(1);
    return 0;
}