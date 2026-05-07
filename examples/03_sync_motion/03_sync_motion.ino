/*
  Chapter 3: 同期制御（時間補間）— ノンブロッキング版

  ch0〜ch3 にサーボを4個接続。
  目標 A と B を 2秒ごとに切り替え、
  1秒ずつかけて全サーボが同じ瞬間に到着するように動かす。

  loop() の中で updateMotion() を毎回呼ぶのがポイント。
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50
#define SERVOMIN 150
#define SERVOMAX 600

const int NUM_SERVOS = 4;
const int CH[NUM_SERVOS] = {0, 1, 2, 3};

// 各サーボの現在位置（最後に送った値）
int current[NUM_SERVOS] = {SERVOMIN, SERVOMIN, SERVOMIN, SERVOMIN};

// 補間動作の状態
struct MotionState {
  int   start[NUM_SERVOS];
  int   target[NUM_SERVOS];
  unsigned long t_start;
  unsigned long duration;
  bool  active;
};
MotionState motion = {{0}, {0}, 0, 0, false};

// イージング関数（直線にしたければ return t;）
float smoothstep(float t) {
  return t * t * (3.0f - 2.0f * t);
}

// 「targets[] へ duration_ms かけて移動」を開始
void startMove(int targets[], int duration_ms) {
  for (int i = 0; i < NUM_SERVOS; i++) {
    motion.start[i]  = current[i];
    motion.target[i] = targets[i];
  }
  motion.t_start  = millis();
  motion.duration = duration_ms;
  motion.active   = true;
}

// loop() のたびに呼ぶ：補間を1ステップ進める
void updateMotion() {
  if (!motion.active) return;

  unsigned long elapsed = millis() - motion.t_start;

  if (elapsed >= motion.duration) {
    for (int i = 0; i < NUM_SERVOS; i++) {
      pwm.setPWM(CH[i], 0, motion.target[i]);
      current[i] = motion.target[i];
    }
    motion.active = false;
    return;
  }

  float ratio = (float)elapsed / (float)motion.duration;
  float eased = smoothstep(ratio);
  for (int i = 0; i < NUM_SERVOS; i++) {
    int pos = motion.start[i]
            + (int)((motion.target[i] - motion.start[i]) * eased);
    pwm.setPWM(CH[i], 0, pos);
    current[i] = pos;
  }
}

// 目標 A / B
int targetA[NUM_SERVOS] = {SERVOMIN + 50, SERVOMIN + 150, SERVOMIN + 300, SERVOMAX};
int targetB[NUM_SERVOS] = {SERVOMIN, SERVOMIN, SERVOMIN, SERVOMIN};

unsigned long lastSwitch = 0;
bool gotoA = true;

void setup() {
  Serial.begin(9600);
  Serial.println(F("Synchronized motion demo"));

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  // ホームポジション
  for (int i = 0; i < NUM_SERVOS; i++) {
    pwm.setPWM(CH[i], 0, current[i]);
  }
  delay(500);

  startMove(targetA, 1000);
  lastSwitch = millis();
}

void loop() {
  updateMotion();

  // 2秒ごとに切り替え
  if (millis() - lastSwitch >= 2000) {
    if (gotoA) {
      Serial.println(F(">> move to B"));
      startMove(targetB, 1000);
    } else {
      Serial.println(F(">> move to A"));
      startMove(targetA, 1000);
    }
    gotoA = !gotoA;
    lastSwitch = millis();
  }

  // ここに他の処理を書いてもループは止まらない
}
