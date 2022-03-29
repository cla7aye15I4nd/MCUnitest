TARGET = Button

all:
	arduino-cli compile -b arduino:sam:arduino_due_x_dbg $(TARGET)/$(TARGET).ino --build-path build/$(TARGET)

clean:
	rm -rf build
