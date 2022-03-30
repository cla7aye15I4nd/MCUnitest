#include <stdio.h>
#include <board.h>
#include <periph/timer.h>


timer_cb_t time;
int counter[0x100];

void timer_callback(void *unused, int channel)
{
    counter[channel] += 1;
    (void) (unused);
}

int main(void)
{
    int a;

    a=5; 

    timer_init(TIMER_DEV(0), 1000, timer_callback, &a); // 1000 is the number of ticks per second, "time" is the callback and "a" is an optional parameter passed to callback
    
    timer_read(TIMER_DEV(0)); // reads count register of timer, does not affect fucntionality  is only a read of current count 
    timer_set(TIMER_DEV(0),1,100); //set a timeout in ticks (100 ticks)  for channel 1 of timer(0), which calls "time" callback defined in timer_init when timeout ticks have passed 
    timer_stop(TIMER_DEV(0));  // stop the timer
    timer_start(TIMER_DEV(0)); // start de timer this is unnecessary (part of timer_init) unless stop was called previously

    while(1);
    return 0;
}
