#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import sys, os, lief
sys.path.append("../../../../qiling")

from qiling.core import Qiling
from qiling.extensions.mcu.stm32f4 import stm32f429

path = "../build/bof.elf"

elf = lief.parse(path)

vuln = next(filter(lambda o: o.name == 'vuln', elf.exported_functions))

ql = Qiling([path], archtype="cortex_m", env=stm32f429, ostype='mcu')

ql.hw.create('pwr')
ql.hw.create('rcc')
ql.hw.create('flash interface')
ql.hw.create('gpioa')
ql.hw.create('gpioc')
ql.hw.create('usart2')
ql.hw.create('usart3')

snapshot = ql.save(hw=True)

ql.restore(snapshot)
ql.hw.usart3.send(b'abc\n')
ql.run(count=100000)

print('[Normal]')
print('USART2 Output:', ql.hw.usart2.recv())
print('USART3 Output:', ql.hw.usart3.recv())

ql.restore(snapshot)
ql.hw.usart3.send(b'aaaaaaaaaaaaaaaaaaaa\x89\x05\n')
ql.run(count=100000)

print('[Overflow]')
print('USART2 Output:', ql.hw.usart2.recv())
print('USART3 Output:', ql.hw.usart3.recv())
