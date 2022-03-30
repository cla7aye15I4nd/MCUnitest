APPLICATION = pwm

BOARD ?= frdm-k64f

RIOTBASE ?= $(CURDIR)/../../../library/RIOT

USEMODULE += periph_gpio
USEMODULE += periph_pwm

DISABLE_MODULE += cortexm_fpu

DEVELHELP ?= 0
QUIET ?= 0

include $(RIOTBASE)/Makefile.include
