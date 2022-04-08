import sys, unittest
sys.path.append('../../qiling')

from qiling.core import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions.mcu.atmel import sam3x8e
from qiling.extensions.mcu.nxp import mk64f12


class SAM3X8ETest(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=sam3x8e)
        
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
        ql.hw.uart.watch()
        
        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'ABCDE')
        del ql

    def test_uart_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_UART_RIOT.elf')
        ql.hw.uart.watch()

        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nABCDE')
        del ql

    def test_adc_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_ADC_Arduino.elf')
        ql.hw.adc.watch()

        ql.run(count=100000)
        self.assertTrue(ql.hw.uart.recv().startswith(b'5.00\r\n5.00\r\n'))
        del ql

    def test_adc_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_ADC_RIOT.elf')
        ql.hw.adc.watch()

        ql.run(count=100000)
        self.assertTrue(ql.hw.uart.recv().startswith(b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nadc = 4095\n'))
        del ql

    def test_dac_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_DAC_Arduino.elf')
        ql.hw.create('dac')        

        flags = [False, False]
        def hook_set():
            print("LED on")
            flags[0] = True
        
        def hook_rst():
            print("LED off")
            flags[1] = True

        ql.hw.piob.hook_set  (27, hook_set)
        ql.hw.piob.hook_reset(27, hook_rst)

        ql.hw.systick.ratio = 0xfff
        ql.run(count=50000)

        self.assertTrue(flags[0] and flags[1])
        
        del ql

    def test_dac_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_DAC_RIOT.elf')
        ql.hw.create('dac').watch()

        ql.hw.systick.ratio = 0xfff
        ql.run(count=200000)
        self.assertTrue(ql.hw.uart.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nok\n')
        
        del ql

    def test_gpio_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_GPIO_Arduino.elf')        
        # ql.hw.piob.watch()

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
        ql.hw.create('tc0').watch()

        ql.hw.systick.ratio = 0xfff
        ql.run(count=20000)
        
        del ql

    def test_pwm_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_PWM_RIOT.elf')                
        ql.hw.create('pwm').watch()

        ql.hw.systick.ratio = 0xfff
        ql.run(count=20000)
        
        del ql

    def test_tim_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_TIM_Arduino.elf')                
        
        
        ql.hw.piob.hook_set  (27, lambda : print('LED on'))
        ql.hw.piob.hook_reset(27, lambda : print('LED off'))

        ql.hw.systick.ratio = 0xfff        
        ql.run(count=30000)
        
        del ql

    def test_tim_riot(self):
        # FIXME: some bugs here
        ql = self.qiling_common_setup('../target/other/SAM3X8E_TIM_RIOT.elf')                
        ql.hw.create('tc0').watch()
        
        ql.run(count=200000)        
        del ql
    
    # TODO: spi transfer / receive
    def test_spi_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_SPI_Arduino.elf')                
        ql.hw.create('spi0').watch()

        ql.hw.systick.ratio = 0xfff
        ql.run(count=100000)

        del ql

    def test_spi_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_SPI_RIOT.elf')                
        ql.hw.create('spi0').watch()

        ql.hw.systick.ratio = 0xfff
        ql.run(count=1000000)
        
        del ql

class FRDMK64FTest(unittest.TestCase):
    def qiling_common_setup(self, path):
        ql = Qiling([path], archtype="cortex_m", ostype="mcu", env=mk64f12)

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

        ql.hw.create('uart0').watch()        

        ql.hw.uart0.send(b'BCDEF')
        ql.run(count=10000)

        self.assertTrue(ql.hw.uart0.recv() == b'ABCDEF')
        del ql

    # TODO: test uart with RIOT
    @unittest.skip('')
    def test_uart_riot(self):        
        ql = self.qiling_common_setup('../target/other/FRDM-K64F_UART_RIOT.elf')
        ql.hw.create('uart0').watch()        
        ql.hw.create('smc')
        
        del ql

    def test_adc_sdk(self):        
        ql = self.qiling_common_setup('../target/official/FRDM-K64F_ADC_SDK.elf')
        
        ql.hw.create('adc0').watch()
        ql.hw.create('uart0')
        
        ql.run(count=5000)
        self.assertTrue(ql.hw.uart0.recv().startswith(b'ADC Value: '))

    def test_adc_riot(self):        
        ql = self.qiling_common_setup('../target/other/FRDM-K64F_ADC_RIOT.elf')
        
        ql.hw.create('adc0')
        ql.hw.create('uart0')
        
        ql.run(count=10000)
        self.assertTrue(ql.hw.uart0.recv().startswith(b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nadc = '))        
        

if __name__ == '__main__':
    unittest.main()
