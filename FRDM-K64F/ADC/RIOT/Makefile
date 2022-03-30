APPLICATION = adc

BOARD ?= frdm-k64f

RIOTBASE ?= $(CURDIR)/../../../library/RIOT

USEMODULE += periph_adc
USEMODULE += periph_gpio
USEMODULE += periph_pwm
USEMODULE += periph_spi
USEMODULE += periph_timer
USEMODULE += periph_uart

DISABLE_MODULE += cortexm_fpu

DEVELHELP ?= 0
QUIET ?= 0

include $(RIOTBASE)/Makefile.include
