/*
  Chapter 1: 1個のサーボを動かす（基本動作）

  PCA9685 の ch0 に接続したサーボを、
  最小角度 ⇄ 最大角度 でゆっくり往復させます。

  配線:
    Arduino 5V  -> PCA9685 VCC
    Arduino GND -> PCA9685 GND
    Arduino A4  -> PCA9685 SDA
    Arduino A5  -> PCA9685 SCL
    別電源 +5V  -> PCA9685 V+ (緑端子)
    別電源 GND  -> PCA9685 GND (緑端子)
    サーボ      -> ch0 の 3pin
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

// ===== サーボのキャリブレーション値（要調整） =====
#define SERVO_FREQ   50    // 50 Hz (周期 20 ms)
#define SERVOMIN    150    // パルス幅の最小カウント（約 0.6 ms）
#define SERVOMAX    600    // パルス幅の最大カウント（約 2.4 ms）
// ================================================

#define CH 0  // 動かすチャンネル

void setup() {
  Serial.begin(9600);
  Serial.println(F("Single servo test start"));

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  delay(10);
}

void loop() {
  // 最小 → 最大
  for (int p = SERVOMIN; p <= SERVOMAX; p++) {
    pwm.setPWM(CH, 0, p);
    delay(5);
  }
  delay(500);

  // 最大 → 最小
  for (int p = SERVOMAX; p >= SERVOMIN; p--) {
    pwm.setPWM(CH, 0, p);
    delay(5);
  }
  delay(500);
}
