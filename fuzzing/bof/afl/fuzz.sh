#!/bin/bash
AFL_AUTORESUME=1 afl-fuzz -i inputs -o outputs -t 2000 -U -- python3 ./fuzz.py @@
