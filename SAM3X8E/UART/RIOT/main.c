#include <stdio_base.h>

char buf[] = "A\n";

int main(void)
{    
    stdio_write(buf, 1);

    while (1) {
        if (stdio_read(buf, 1)) {
           stdio_write(buf, 1);
        }
    }

    return 0;
}