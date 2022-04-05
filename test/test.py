import sys, unittest
sys.path.append('../../qiling')

from qiling.core import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions.mcu.atmel import sam3x8e


class SAM3X8ETest(unittest.TestCase):
    def qiling_common_setup(self, path):
        return Qiling([path], archtype="cortex_m", ostype="mcu", env=sam3x8e)

    def test_uart_arduino(self):
        ql = self.qiling_common_setup('../target/official/SAM3X8E_UART_Arduino.elf')

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
        ql.hw.create('uart').watch()
        ql.hw.create('pdc_uart')

        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'ABCDE')

        del ql

    def test_uart_riot(self):
        ql = self.qiling_common_setup('../target/other/SAM3X8E_UART_RIOT.elf')

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
        ql.hw.create('uart').watch()
        ql.hw.create('pdc_uart')

        ql.hw.uart.send(b'BCDE')
        ql.run(count=100000)

        self.assertTrue(ql.hw.uart.recv() == b'main(): This is RIOT! (Version: 2022.04-devel-1050-gfca56)\nABCDE')

        del ql

if __name__ == '__main__':
    unittest.main()