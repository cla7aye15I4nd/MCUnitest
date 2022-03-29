#![deny(unsafe_code)]
#![no_main]
#![no_std]

use panic_semihosting as _;

use cortex_m_rt::entry;
use stm32f1xx_hal::{
    adc, 
    pac, 
    prelude::*,
    serial::{Config, Serial},
};

use core::fmt::Write;

#[entry]
fn main() -> ! {
    let p = pac::Peripherals::take().unwrap();
    let mut flash = p.FLASH.constrain();
    let rcc = p.RCC.constrain();

    let clocks = rcc.cfgr.adcclk(2.mhz()).freeze(&mut flash.acr);
    
    let mut afio = p.AFIO.constrain();
    let mut gpioa = p.GPIOA.split();

    let tx = gpioa.pa2.into_alternate_push_pull(&mut gpioa.crl);
    let rx = gpioa.pa3;

    let serial = Serial::usart2(
        p.USART2,
        (tx, rx),
        &mut afio.mapr,
        Config::default().baudrate(115200.bps()),
        clocks,
    );

    let (mut tx, _rx) = serial.split();

    // Setup ADC
    let mut adc1 = adc::Adc::adc1(p.ADC1, clocks);

    // Setup GPIOB
    let mut gpiob = p.GPIOB.split();

    // Configure pb0, pb1 as an analog input
    let mut ch0 = gpiob.pb0.into_analog(&mut gpiob.crl);
    let data: u16 = adc1.read(&mut ch0).unwrap();

    writeln!(tx, "adc1: {}", data).unwrap();

    loop {}
}
