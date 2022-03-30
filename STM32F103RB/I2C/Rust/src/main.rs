#![deny(unsafe_code)]
#![no_std]
#![no_main]

use panic_semihosting as _;

use cortex_m_rt::entry;
use stm32f1xx_hal::{
    // delay::Delay,
    i2c::{BlockingI2c, DutyCycle, Mode},
    pac,
    prelude::*,
    serial::{Config, Serial},
};

use core::fmt::Write;

#[entry]
fn main() -> ! {
    // Get access to the core peripherals from the cortex-m crate
    let _cp = cortex_m::Peripherals::take().unwrap();
    // Get access to the device specific peripherals from the peripheral access crate
    let dp = pac::Peripherals::take().unwrap();

    // Take ownership over the raw flash and rcc devices and convert them into the corresponding
    // HAL structs
    let mut flash = dp.FLASH.constrain();
    let rcc = dp.RCC.constrain();
    let mut afio = dp.AFIO.constrain();
    // Freeze the configuration of all the clocks in the system and store the frozen frequencies in
    // `clocks`
    let clocks = rcc.cfgr.use_hse(8.mhz()).freeze(&mut flash.acr);

    // Acquire the GPIOB peripheral
    let mut gpiob = dp.GPIOB.split();

    let scl = gpiob.pb8.into_alternate_open_drain(&mut gpiob.crh);
    let sda = gpiob.pb9.into_alternate_open_drain(&mut gpiob.crh);

    let mut i2c = BlockingI2c::i2c1(
        dp.I2C1,
        (scl, sda),
        &mut afio.mapr,
        Mode::Fast {
            frequency: 400_000.hz(),
            duty_cycle: DutyCycle::Ratio16to9,
        },
        clocks,
        1000,
        10,
        1000,
        1000,
    );

    let mut gpioa = dp.GPIOA.split();

    // USART2
    let tx = gpioa.pa2.into_alternate_push_pull(&mut gpioa.crl);
    let rx = gpioa.pa3;

    // Set up the usart device. Taks ownership over the USART register and tx/rx pins. The rest of
    // the registers are used to enable and configure the device.
    let serial = Serial::usart2(
        dp.USART2,
        (tx, rx),
        &mut afio.mapr,
        Config::default().baudrate(115200.bps()),
        clocks,
    );

    let (mut tx, mut _rx) = serial.split();
    
    let mut data : [u8; 1] = [b'A'];
    match i2c.write(0x20, &mut data) {
        Ok(_)  => writeln!(tx, "ok.").unwrap(),
        Err(_) => writeln!(tx, "err.").unwrap(),        
    }
    
    match i2c.read(0x20, &mut data) {
        Ok(_)  => writeln!(tx, "ok.").unwrap(),
        Err(_) => writeln!(tx, "err.").unwrap(),        
    }

    loop {
        
    }
}