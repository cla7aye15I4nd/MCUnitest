# name of your application
APPLICATION = uart

# If no BOARD is found in the environment, use this default:
BOARD ?= arduino-due

# This has to be the absolute path to the RIOT base directory:
RIOTBASE ?= $(CURDIR)/../../../library/RIOT

# Comment this out to disable code in RIOT that does safety checking
# which is not needed in a production environment but helps in the
# development process:
DEVELHELP ?= 0

# Change this to 0 show compiler invocation lines by default:
QUIET ?= 0

USEMODULE += periph_uart
USEMODULE += stdio_uart_rx

include $(RIOTBASE)/Makefile.include
