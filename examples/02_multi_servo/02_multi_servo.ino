/*
  Chapter 2: 複数サーボを「同時に命令」する（同期できていない例）

  ch0〜ch3 にサーボを4個接続。
  全部に同時に setPWM() するが、距離が違うので
  到着時刻がバラバラになる様子を観察するスケッチ。
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50
#define SERVOMIN 150
#define SERVOMAX 600

const int NUM_SERVOS = 4;
const int CH[NUM_SERVOS] = {0, 1, 2, 3};

void setup() {
  Serial.begin(9600);
  Serial.println(F("Multi servo (NOT synchronized) demo"));

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  // 全員ホームポジションへ（SERVOMIN）
  for (int i = 0; i < NUM_SERVOS; i++) {
    pwm.setPWM(CH[i], 0, SERVOMIN);
  }
  delay(1000);
}

void loop() {
  // 全員ホームへ
  Serial.println(F(">> Reset to SERVOMIN"));
  for (int i = 0; i < NUM_SERVOS; i++) {
    pwm.setPWM(CH[i], 0, SERVOMIN);
  }
  delay(1500);

  // 距離が違う目標を「一斉に」命令
  int targets[NUM_SERVOS] = {
    SERVOMIN + 50,    // ch0: ちょっとだけ
    SERVOMIN + 150,   // ch1: 少し
    SERVOMIN + 300,   // ch2: わりと大きく
    SERVOMAX          // ch3: 全力で
  };

  Serial.println(F(">> Fire! (different targets, simultaneous command)"));
  unsigned long t0 = millis();
  for (int i = 0; i < NUM_SERVOS; i++) {
    pwm.setPWM(CH[i], 0, targets[i]);
  }
  unsigned long t1 = millis();
  Serial.print(F("   command time = "));
  Serial.print(t1 - t0);
  Serial.println(F(" ms (commands finish almost instantly,"));
  Serial.println(F("   but the servos arrive at different times!)"));

  delay(1500);
}
