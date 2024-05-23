#include <Arduino.h>

#define GPIO1_PIN 9  // Use the correct pin number for GPIO1
#define GPIO2_PIN 10 // Use the correct pin number for GPIO2

void setup() {
  Serial.begin(9600);
  pinMode(GPIO1_PIN, OUTPUT);
  pinMode(GPIO2_PIN, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    int gpio1_percentage_index = data.indexOf("GPIO1: ");
    int gpio2_percentage_index = data.indexOf("GPIO2: ");
    
    if (gpio1_percentage_index != -1 && gpio2_percentage_index != -1) {
      String gpio1_percentage_str = data.substring(gpio1_percentage_index + 7, data.indexOf("%", gpio1_percentage_index));
      String gpio2_percentage_str = data.substring(gpio2_percentage_index + 7, data.indexOf("%", gpio2_percentage_index));
      
      int gpio1_percentage = gpio1_percentage_str.toInt();
      int gpio2_percentage = gpio2_percentage_str.toInt();
      
      analogWrite(GPIO1_PIN, map(gpio1_percentage, 0, 100, 0, 255));
      analogWrite(GPIO2_PIN, map(gpio2_percentage, 0, 100, 0, 255));
    }
  }
}