#![deny(unsafe_code)]
#![no_std]
#![no_main]

use cortex_m_rt::entry;
use panic_halt as _;

use embedded_hal::spi::{Mode, Phase, Polarity};
pub const MODE: Mode = Mode {
    phase: Phase::CaptureOnSecondTransition,
    polarity: Polarity::IdleHigh,
};

use stm32f1xx_hal::{
    // gpio::gpioa::PA4,
    // gpio::{Output, PushPull},
    pac::{
        Peripherals, 
        // SPI1
    },
    prelude::*,
    spi::{
        // Pins, 
        Spi, 
        // Spi1NoRemap
    },
    serial::{Config, Serial},
};

use core::fmt::Write;

#[entry]
fn main() -> ! {
    let dp = Peripherals::take().unwrap();

    let mut flash = dp.FLASH.constrain();
    let rcc = dp.RCC.constrain();

    let clocks = rcc.cfgr.freeze(&mut flash.acr);

    let mut afio = dp.AFIO.constrain();
    let mut gpioa = dp.GPIOA.split();

    // SPI1
    let sck = gpioa.pa5.into_alternate_push_pull(&mut gpioa.crl);
    let miso = gpioa.pa6;
    let mosi = gpioa.pa7.into_alternate_push_pull(&mut gpioa.crl);
    // let cs = gpioa.pa4.into_push_pull_output(&mut gpioa.crl);

    let mut spi = Spi::spi1(
        dp.SPI1,
        (sck, miso, mosi),
        &mut afio.mapr,
        MODE,
        1_u32.mhz(),
        clocks,
    );

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

    let (mut tx, _rx) = serial.split();
    
    let mut data = [0];
    match spi.transfer(&mut data) {
        Err(_) => {
            writeln!(tx, "Error").unwrap();
        },
        Ok(_) => {
            writeln!(tx, "Success").unwrap();
        },
    }
    
    loop {
    }
}