void setup() {
  Serial.begin(9600);
  Serial.write('A');
}

void loop() {
  if (Serial.available()) {
    Serial.write(Serial.read());
  }
}
