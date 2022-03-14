#include "test.h"

volatile static char flag = 0;

void mcg_test_begin(void) { flag++; }
void mcg_test_end(void)   { flag--; }
