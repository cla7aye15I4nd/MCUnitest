#!/bin/bash
AFL_AUTORESUME=1 afl-fuzz -i inputs -o outputs -U -- python3 ./fuzz.py @@
