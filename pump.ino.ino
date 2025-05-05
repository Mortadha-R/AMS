int state =0;
void setup() {
  // put your setup code here, to run once:
  pinMode(2, INPUT);
  pinMode(3, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  state = digitalRead(2);
  digitalWrite(3, !state);


}
