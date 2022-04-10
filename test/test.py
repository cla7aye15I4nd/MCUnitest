import sys, unittest
sys.path.append('../../qiling')

from qiling.core import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions.mcu.stm32f1 import stm32f103
from qiling.extensions.mcu.stm32f4 import stm32f429
from qiling.extensions.mcu.atmel import sam3x8e
from qiling.extensions.mcu.nxp import mk64f12


class STM32F429Test(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=stm32f429)

        ql.hw.create('rcc')
        ql.hw.create('flash interface')
        ql.hw.create('pwr')
        ql.hw.create('exti')
        ql.hw.create('syscfg')
        ql.hw.create('gpioa')
        ql.hw.create('gpiob')
        ql.hw.create('gpioc')

        return ql

    def test_dac_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F429ZI_DAC_Cube.elf')
        ql.hw.create('dac1')
        
        counter = False
        def hook_set(): 
            nonlocal counter
            counter += 1

        ql.hw.gpiob.hook_set(0, hook_set)
        ql.hw.systick.ratio = 0xfff
        ql.run(count=100000)
        self.assertTrue(counter > 2)

        del ql

    ## TODO: Handle Interrupt
    def test_gpio_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F429ZI_GPIO_Cube.elf')
        
        ql.run(count=3000)

        for i in range(5):
            ql.hw.gpioc.set_pin(13)
            ql.run(count=100)
            self.assertTrue(ql.hw.gpiob.pin(7))

            ql.hw.gpioc.reset_pin(13)
            ql.run(count=100)
            self.assertFalse(ql.hw.gpiob.pin(7))     
        
        del ql


class STM32F103Test(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=stm32f103, verbose=QL_VERBOSE.DISABLED)

        ql.hw.create('rcc')
        ql.hw.create('flash interface')
        ql.hw.create('afio')
        ql.hw.create('exti')
        ql.hw.create('gpioa')
        ql.hw.create('gpiob')
        ql.hw.create('gpioc')
        ql.hw.create('gpiod')
        ql.hw.create('gpioe')

        return ql

    def test_uart_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F103RB_USART_Cube.elf')

        ql.hw.create('usart2')
        ql.hw.usart2.send(b'B')
        ql.hw.systick.ratio = 0xfff
        ql.run(count=10000)
        
        self.assertTrue(ql.hw.usart2.recv().startswith(b'ABB'))

        del ql

    def test_uart_rust(self):
        ql = self.qiling_common_setup('../target/other/STM32F103RB_USART_Rust.elf')

        ql.hw.create('usart2')
        ql.hw.usart2.send(b'_YZ')
        ql.hw.systick.ratio = 0xfff
        ql.run(count=10000)

        self.assertTrue(ql.hw.usart2.recv() == b'XYZ')

        del ql

    def test_adc_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F103RB_ADC_Cube.elf')

        ql.hw.create('adc1')
        ql.hw.create('usart2')
        
        ql.run(count=5000)        
        self.assertTrue(ql.hw.usart2.recv().startswith(b'adc_value = '))

        del ql

    def test_adc_rust(self):
        ql = self.qiling_common_setup('../target/other/STM32F103RB_ADC_Rust.elf')

        ql.hw.create('adc1')
        ql.hw.create('usart2')
        
        ql.run(count=1000)        
        self.assertTrue(ql.hw.usart2.recv().startswith(b'adc1: '))

        del ql

    def test_pwm_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F103RB_PWM_Cube.elf')

        ql.hw.create('tim3')
        ql.hw.create('usart2')
        
        flags = [0, 0]
        def hook_set(): flags[0] = 1
        def hook_rst(): flags[1] = 1

        ql.hw.gpioa.hook_set(5, hook_set)
        ql.hw.gpioa.hook_reset(5, hook_rst)
        
        ql.hw.systick.ratio = 0xfff
        ql.run(count=250000)
        self.assertTrue(flags[0] == 1 and flags[1] == 1)

        del ql

    def test_pwm_rust(self):
        ql = self.qiling_common_setup('../target/other/STM32F103RB_PWM_Rust.elf')

        ql.hw.create('tim2')
        ql.hw.create('usart2')
        
        ql.hw.systick.ratio = 0xfff
        ql.run(count=10000)        

        del ql

    def test_tim_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F103RB_TIM_Cube.elf')

        ql.hw.create('tim2')

        counter = [0, 0]
        def hook_set(): counter[0] += 1
        def hook_rst(): counter[1] += 1

        ql.hw.gpioa.hook_set(5, hook_set)
        ql.hw.gpioa.hook_reset(5, hook_rst)
        
        ql.hw.tim2.ratio = 0xfff
        ql.run(count=50000)

        self.assertTrue(counter[0] > 10 and counter[1] > 10)

        del ql

    def test_tim_rust(self):
        ql = self.qiling_common_setup('../target/other/STM32F103RB_TIM_Rust.elf')

        ql.hw.create('tim2')

        counter = [0, 0]
        def hook_set(): counter[0] += 1
        def hook_rst(): counter[1] += 1

        ql.hw.gpioa.hook_set(5, hook_set)
        ql.hw.gpioa.hook_reset(5, hook_rst)
        
        ql.hw.tim2.ratio = 0xfff
        ql.run(count=50000)
        
        self.assertTrue(counter[0] > 10 and counter[1] > 10)

        del ql

    def test_spi_cube(self):
        ql = self.qiling_common_setup('../target/official/STM32F103RB_SPI_Cube.elf')

        ql.hw.create('spi1')        
        
        ql.hw.spi1.send(b'BB')
        ql.hw.systick.ratio = 0xfff
        ql.run(count=10000)
        
        buf = ql.hw.spi1.recv()
        self.assertTrue(b'A' in buf and b'B' in buf)

        del ql

    def test_spi_rust(self):
        ql = self.qiling_common_setup('../target/other/STM32F103RB_SPI_Rust.elf')

        ql.hw.create('spi1')        
        ql.hw.create('usart2')        
        
        ql.hw.systick.ratio = 0xfff
        ql.run(count=10000)

        self.assertTrue(ql.hw.usart2.recv() == b'Success\n')
        del ql

class SAM3X8ETest(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=sam3x8e, verbose=QL_VERBOSE.DISABLED)
        
        ql.hw.create('wdt')
        ql.hw.create('efc0')
        ql.hw.create('efc1')
        ql.hw.create('pmc')
        ql.hw.create('uotghs')
        ql.hw.create('pioa')
        ql.hw.create('piob')
        ql.hw.create('pioc')
        ql.hw.create('piod')
        ql.hw.create('adc')
        ql.hw.create('uart')
        ql.hw.create('pdc_uart')

        return ql

    def test_uart_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_UART_Arduino.elf')        
        
        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'ABCDE')
        del ql

    def test_uart_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_UART_RIOT.elf')


        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nABCDE')
        del ql

    def test_adc_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_ADC_Arduino.elf')

        ql.run(count=100000)
        self.assertTrue(ql.hw.uart.recv().startswith(b'5.00\r\n5.00\r\n'))
        del ql

    def test_adc_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_ADC_RIOT.elf')

        ql.run(count=100000)
        self.assertTrue(ql.hw.uart.recv().startswith(b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nadc = 4095\n'))
        del ql

    def test_dac_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_DAC_Arduino.elf')
        ql.hw.create('dac')        

        flags = [False, False]
        def hook_set():
            flags[0] = True
        
        def hook_rst():
            flags[1] = True

        ql.hw.piob.hook_set  (27, hook_set)
        ql.hw.piob.hook_reset(27, hook_rst)

        ql.hw.systick.ratio = 0xfff
        ql.run(count=50000)

        self.assertTrue(flags[0] and flags[1])
        
        del ql

    def test_dac_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_DAC_RIOT.elf')
        ql.hw.create('dac')

        ql.hw.systick.ratio = 0xfff
        ql.run(count=200000)
        self.assertTrue(ql.hw.uart.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nok\n')
        
        del ql

    def test_gpio_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_GPIO_Arduino.elf')        


        status = 0
        def hook_set():
            nonlocal status
            status = 1
        
        def hook_rst():            
            nonlocal status
            status = 0

        ql.hw.piob.hook_set  (27, hook_set)
        ql.hw.piob.hook_reset(27, hook_rst)

        ql.run(count=200000)
        ql.hw.piob.set_pin(25)
        ql.run(count=2000)
        self.assertTrue(status == 1)

        ql.hw.piob.reset_pin(25)
        ql.run(count=2000)
        self.assertTrue(status == 0)
        
        del ql

    def test_gpio_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_GPIO_RIOT.elf')                

        status = 0
        def hook_set():
            nonlocal status
            status = 1
        
        def hook_rst():            
            nonlocal status
            status = 0

        ql.hw.piob.hook_set  (27, hook_set)
        ql.hw.piob.hook_reset(27, hook_rst)

        
        ql.run(count=200000)

        ql.hw.piob.set_pin(25)
        ql.run(count=2000)
        self.assertTrue(status == 1)

        ql.hw.piob.reset_pin(25)
        ql.run(count=2000)
        self.assertTrue(status == 0)
        
        del ql

    def test_pwm_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_PWM_Arduino.elf')                
        ql.hw.create('tc0')

        ql.hw.systick.ratio = 0xfff
        ql.run(count=20000)
        
        del ql

    def test_pwm_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_PWM_RIOT.elf')                
        ql.hw.create('pwm')

        ql.hw.systick.ratio = 0xfff
        ql.run(count=20000)
        
        del ql

    def test_tim_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_TIM_Arduino.elf')                
        
        
        # ql.hw.piob.hook_set  (27, lambda : print('LED on'))
        # ql.hw.piob.hook_reset(27, lambda : print('LED off'))

        ql.hw.systick.ratio = 0xfff        
        ql.run(count=30000)
        
        del ql

    # FIXME: some bugs here
    def test_tim_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_TIM_RIOT.elf')                
        ql.hw.create('tc0')
        
        ql.run(count=200000)        
        del ql
    
    def test_spi_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_SPI_Arduino.elf')                
        ql.hw.create('spi0')

        ql.hw.spi0.send(b'abcdefghij')
        ql.run(count=100000)
        
        self.assertTrue(b'\xeeabcdefghi' == ql.hw.spi0.recv())
        self.assertTrue(b'abcdefghij' == ql.hw.uart.recv())  

        del ql

    def test_spi_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_SPI_RIOT.elf')                
        ql.hw.create('spi0')

        ql.hw.spi0.send(b'bcdefghijk')
        ql.run(count=100000)
        
        self.assertTrue(b'success' in ql.hw.uart.recv())
        self.assertTrue(b'abcdefghij' == ql.hw.spi0.recv())        
        
        del ql

class FRDMK64FTest(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=mk64f12, verbose=QL_VERBOSE.DISABLED)

        ql.hw.create('wdog')
        ql.hw.create('sim')
        ql.hw.create('osc')
        ql.hw.create('mcg')

        ql.hw.create('porta')
        ql.hw.create('portb')
        ql.hw.create('portc')
        ql.hw.create('portd')
        ql.hw.create('porte')

        ql.hw.create('gpioa')
        ql.hw.create('gpiob')
        ql.hw.create('gpioc')
        ql.hw.create('gpiod')
        ql.hw.create('gpioe')        

        return ql

    def test_uart_sdk(self):        
        ql = self.qiling_common_setup('../target/official/FRDM-K64F_UART_SDK.elf')

        ql.hw.create('uart0')        

        ql.hw.uart0.send(b'BCDEF')
        ql.run(count=10000)

        self.assertTrue(ql.hw.uart0.recv() == b'ABCDEF')
        del ql

    def test_uart_riot(self):        
        ql = self.qiling_common_setup('../target/other/FRDM-K64F_UART_RIOT.elf')
        ql.hw.create('uart0')        
        ql.hw.create('smc')

        ql.hw.uart0.send(b'BCDEF')
        ql.run(count=10000)
        self.assertTrue(ql.hw.uart0.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nABCDEF')
        
        del ql

    def test_adc_sdk(self):        
        ql = self.qiling_common_setup('../target/official/FRDM-K64F_ADC_SDK.elf')
        
        ql.hw.create('adc0')
        ql.hw.create('uart0')
        
        ql.run(count=5000)
        self.assertTrue(ql.hw.uart0.recv().startswith(b'ADC Value: '))

        del ql

    def test_adc_riot(self):        
        ql = self.qiling_common_setup('../target/other/FRDM-K64F_ADC_RIOT.elf')
        
        ql.hw.create('adc0')
        ql.hw.create('uart0')
        
        ql.run(count=10000)
        self.assertTrue(ql.hw.uart0.recv().startswith(b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nadc = '))        

        del ql
        
    def test_gpio_sdk(self):
        ql = self.qiling_common_setup('../target/official/FRDM-K64F_GPIO_SDK.elf')
        
        ql.hw.create('uart0')

        ql.run(count=10000)
        
        status = ql.hw.gpiob.pin(22)
        for i in range(10):
            ql.hw.gpioa.set_pin(4)
            ql.hw.gpioa.reset_pin(4)
            ql.run(count=1000)
            
            now = ql.hw.gpiob.pin(22)
            self.assertTrue(now != status)
            status = now            

        del ql

    def test_gpio_riot(self):
        ql = self.qiling_common_setup('../target/other/FRDM-K64F_GPIO_RIOT.elf')
        
        ql.hw.create('smc')
        ql.hw.create('rtc')
        ql.hw.create('uart0')
        
        ql.run(count=10000)
        self.assertFalse(ql.hw.gpiob.pin(22))
        
        for i in range(10):
            ql.hw.gpioc.set_pin(6)
            ql.run(count=100)
            self.assertTrue(ql.hw.gpiob.pin(22))
            
            ql.hw.gpioc.reset_pin(6)
            ql.run(count=100)
            self.assertFalse(ql.hw.gpiob.pin(22))

        del ql    

if __name__ == '__main__':
    unittest.main(verbosity=2)
