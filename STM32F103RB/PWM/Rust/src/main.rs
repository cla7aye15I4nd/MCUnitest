//! Testing PWM output for pre-defined pin combination: all pins for default mapping

#![deny(unsafe_code)]
#![allow(clippy::empty_loop)]
#![no_main]
#![no_std]

use panic_halt as _;

use cortex_m_rt::entry;
use stm32f1xx_hal::{
    pac,
    prelude::*,
    time::ms,
    timer::{Channel, Tim2NoRemap},
};

#[entry]
fn main() -> ! {
    let p = pac::Peripherals::take().unwrap();

    let mut flash = p.FLASH.constrain();
    let rcc = p.RCC.constrain();

    let clocks = rcc.cfgr.freeze(&mut flash.acr);

    let mut afio = p.AFIO.constrain();

    let mut gpioa = p.GPIOA.split();
    // let mut gpiob = p.GPIOB.split();

    // TIM2
    let c1 = gpioa.pa0.into_alternate_push_pull(&mut gpioa.crl);
    let c2 = gpioa.pa1.into_alternate_push_pull(&mut gpioa.crl);
    let c3 = gpioa.pa2.into_alternate_push_pull(&mut gpioa.crl);
    // If you don't want to use all channels, just leave some out
    // let c4 = gpioa.pa3.into_alternate_push_pull(&mut gpioa.crl);
    let pins = (c1, c2, c3);

    let mut pwm = p
        .TIM2
        .pwm_hz::<Tim2NoRemap, _, _>(pins, &mut afio.mapr, 1.kHz(), &clocks);

    // Enable clock on each of the channels
    pwm.enable(Channel::C1);
    pwm.enable(Channel::C2);
    pwm.enable(Channel::C3);

    //// Operations affecting all defined channels on the Timer

    // Adjust period to 0.5 seconds
    pwm.set_period(ms(500).into_rate());

    // Return to the original frequency
    pwm.set_period(1.kHz());

    let max = pwm.get_max_duty();

    //// Operations affecting single channels can be accessed through
    //// the Pwm object or via dereferencing to the pin.

    // Use the Pwm object to set C3 to full strength
    pwm.set_duty(Channel::C3, max);

    // Use the Pwm object to set C3 to be dim
    pwm.set_duty(Channel::C3, max / 4);

    // Use the Pwm object to set C3 to be zero
    pwm.set_duty(Channel::C3, 0);

    // Extract the PwmChannel for C3
    let mut pwm_channel = pwm.split().2;

    // Use the PwmChannel object to set C3 to be full strength
    pwm_channel.set_duty(max);

    // Use the PwmChannel object to set C3 to be dim
    pwm_channel.set_duty(max / 4);

    // Use the PwmChannel object to set C3 to be zero
    pwm_channel.set_duty(0);

    loop {}
}
