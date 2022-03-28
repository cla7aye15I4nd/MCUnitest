void setup() {
    pinMode(LED_BUILTIN, OUTPUT);
    analogWriteResolution(12);
}

void loop() {
    analogWrite(DAC1, 0);
    delay(5);

    analogWrite(DAC1, 1023);
    delay(5);

    analogWrite(DAC1, 2047);
    delay(5);

    analogWrite(DAC1, 4095);
    delay(5);

    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW);
    delay(500);
}
