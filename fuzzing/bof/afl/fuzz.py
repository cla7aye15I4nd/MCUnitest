#!/usr/bin/env python3
# 
# Cross Platform and Multi Architecture Advanced Binary Emulation Framework
#

import os
import sys

from typing import Any, Optional

sys.path.append("../../../../qiling")
from qiling.core import Qiling
from qiling.const import QL_VERBOSE

from qiling.extensions.afl import ql_afl_fuzz
from qiling.extensions.mcu.stm32f4 import stm32f429


def main(input_file: str):
    ql = Qiling(["../build/bof.elf"], 
                archtype="cortex_m", 
                env=stm32f429, 
                ostype='mcu',
                verbose=QL_VERBOSE.DISABLED)

    ql.hw.create('pwr')
    ql.hw.create('rcc')
    ql.hw.create('flash interface')
    ql.hw.create('gpioa')
    ql.hw.create('gpioc')
    ql.hw.create('usart2')
    ql.hw.create('usart3')

    def place_input_callback(ql: Qiling, input_bytes: bytes, persistent_round: int) -> Optional[bool]:
        """Called with every newly generated input."""

        ql.hw.usart3.send(input_bytes)
        
        return True

    ql_afl_fuzz(ql, input_file, place_input_callback, exits=[0x8000677])

if __name__ == "__main__":
    if len(sys.argv) == 1:
        raise ValueError("No input file provided.")

    main(sys.argv[1])