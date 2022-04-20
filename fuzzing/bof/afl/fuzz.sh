#!/bin/bash
AFL_AUTORESUME=1 afl-fuzz -i inputs -o outputs -t 20000 -U -- python3 ./fuzz.py @@
