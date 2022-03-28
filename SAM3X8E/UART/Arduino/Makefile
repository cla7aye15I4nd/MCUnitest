TARGET = EchoServer

all:
	arduino-cli compile -b arduino:sam:arduino_due_x_dbg $(TARGET)/$(TARGET).ino --build-path build

clean:
	rm -rf build
