TARGET = uart

all:
	cargo build --release	

	cargo objcopy --release -- target/$(TARGET).elf
	cargo objcopy --release -- -O ihex target/$(TARGET).hex
	cargo objcopy --release -- -O binary target/$(TARGET).bin
	
flash:	
	st-flash --format=ihex write target/$(TARGET).hex

format:
	cargo fmt
	
clean:
	cargo clean