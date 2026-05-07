/*
  Chapter 1: サーボのキャリブレーション用スケッチ

  シリアルモニタから 100〜700 のカウント値を入力すると、
  その値で setPWM します。

  使い方:
    1. このスケッチを書き込む
    2. ツール → シリアルモニタを開く（9600 baud）
    3. 「行末: 改行」に設定
    4. 「150」「200」「300」「500」など入力 → サーボの動きを観察
    5. 「ガクッ」と限界に当たる手前を SERVOMIN / SERVOMAX として記録
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50
#define CH 0

void setup() {
  Serial.begin(9600);
  Serial.println(F("Calibration mode."));
  Serial.println(F("Type pulse count (100-700) and press Enter."));

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  // 安全な中央位置からスタート
  pwm.setPWM(CH, 0, 375);
  delay(500);
}

void loop() {
  if (Serial.available() > 0) {
    int p = Serial.parseInt();
    // ゴミ文字対策: バッファを空にする
    while (Serial.available() > 0) Serial.read();

    if (p >= 100 && p <= 700) {
      Serial.print(F("setPWM("));
      Serial.print(p);
      Serial.println(F(")"));
      pwm.setPWM(CH, 0, p);
    } else if (p != 0) {
      Serial.println(F("Out of range (100-700)"));
    }
  }
}
