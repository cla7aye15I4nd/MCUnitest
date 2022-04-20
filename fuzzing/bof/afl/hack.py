#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import sys, os
sys.path.append("../../../../qiling")

from qiling.core import Qiling
from qiling.const import QL_VERBOSE
from qiling.extensions.mcu.stm32f4 import stm32f429

ql = Qiling(["../build/bof.elf"], archtype="cortex_m", env=stm32f429, ostype='mcu', verbose=QL_VERBOSE.DISABLED)

ql.hw.create('rcc')
ql.hw.create('usart2')
ql.hw.create('usart3')
ql.os.grain_size = 100

snapshot = ql.save(hw=True)

ql.restore(snapshot)
ql.hw.usart3.send(b'abc\n')
ql.run(count=20000)

print('[Normal]')
print('USART2 Output:', ql.hw.usart2.recv())
print('USART3 Output:', ql.hw.usart3.recv())

ql.restore(snapshot)
ql.hw.usart3.send(b'aaaaaaaaaaaaaaaaaaaa\x89\x05\n')
ql.run(count=20000)

print('[Overflow]')
print('USART2 Output:', ql.hw.usart2.recv())
print('USART3 Output:', ql.hw.usart3.recv())
