/*
  Chapter 4: 1脚の逆運動学（IK）デモ

  ch0 = 股ヨー、ch1 = 股ピッチ、ch2 = 膝
  足先を (x, y, z) [mm] で指定して、対応するサーボ角度を計算 → 同期送信。
  デモでは足先で半径 20 mm の円を描く動きを行う。

  自分のロボットに合わせて L1, L2 と ServoCal を調整すること。
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <math.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50

// ===== リンク長 =====
const float L1 = 50.0f;  // 大腿 [mm]
const float L2 = 60.0f;  // 脛   [mm]

// ===== サーボキャリブレーション構造体 =====
struct ServoCal {
  uint8_t channel;
  int     pwmMin;
  int     pwmMax;
  float   angleAtMin;  // [rad]
  float   angleAtMax;  // [rad]
  float   offset;      // [rad]
  int     direction;   // +1 or -1
};

// 値は実機で調整してください（例として置いています）
ServoCal yawCal  = {0, 150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
ServoCal hipCal  = {1, 150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
ServoCal kneeCal = {2, 150, 600,  0.0f,   M_PI,   0.0f, +1};

// ===== IK =====
bool ik2d(float x, float y, float L1_, float L2_,
          float *hipAngle, float *kneeAngle) {
  float d = sqrtf(x * x + y * y);
  if (d > L1_ + L2_) return false;
  if (d < fabsf(L1_ - L2_)) return false;

  float alpha   = atan2f(x, y);
  float cosBeta = (L1_ * L1_ + d * d - L2_ * L2_) / (2.0f * L1_ * d);
  cosBeta = constrain(cosBeta, -1.0f, 1.0f);
  float beta    = acosf(cosBeta);

  float cosGamma = (L1_ * L1_ + L2_ * L2_ - d * d) / (2.0f * L1_ * L2_);
  cosGamma = constrain(cosGamma, -1.0f, 1.0f);
  float gamma   = acosf(cosGamma);

  *hipAngle  = alpha - beta;
  *kneeAngle = (float)M_PI - gamma;
  return true;
}

bool ik3d(float xf, float ys, float zd,
          float *yaw, float *hip, float *knee) {
  *yaw = atan2f(ys, xf);
  float xp = sqrtf(xf * xf + ys * ys);
  return ik2d(xp, zd, L1, L2, hip, knee);
}

// ===== 角度→PWM =====
int angleToPWM(const ServoCal &s, float angle_rad) {
  float a = s.direction * angle_rad + s.offset;
  float t = (a - s.angleAtMin) / (s.angleAtMax - s.angleAtMin);
  if (t < 0.0f) t = 0.0f;
  if (t > 1.0f) t = 1.0f;
  return s.pwmMin + (int)((s.pwmMax - s.pwmMin) * t);
}

// ===== 同期動作（Ch3 のミニ版） =====
const int NUM_LEG_SERVOS = 3;
int current[NUM_LEG_SERVOS];
int targetPwm[NUM_LEG_SERVOS];
int startPwm[NUM_LEG_SERVOS];
unsigned long t_start = 0;
unsigned long t_dur   = 0;
bool active = false;

void startMove(int targets[], int duration_ms) {
  for (int i = 0; i < NUM_LEG_SERVOS; i++) {
    startPwm[i]  = current[i];
    targetPwm[i] = targets[i];
  }
  t_start = millis();
  t_dur   = duration_ms;
  active  = true;
}

void updateMotion() {
  if (!active) return;
  unsigned long e = millis() - t_start;
  if (e >= t_dur) {
    for (int i = 0; i < NUM_LEG_SERVOS; i++) {
      pwm.setPWM(i == 0 ? yawCal.channel
              : i == 1 ? hipCal.channel : kneeCal.channel,
              0, targetPwm[i]);
      current[i] = targetPwm[i];
    }
    active = false;
    return;
  }
  float r = (float)e / (float)t_dur;
  r = r * r * (3.0f - 2.0f * r);  // smoothstep
  for (int i = 0; i < NUM_LEG_SERVOS; i++) {
    int p = startPwm[i] + (int)((targetPwm[i] - startPwm[i]) * r);
    pwm.setPWM(i == 0 ? yawCal.channel
            : i == 1 ? hipCal.channel : kneeCal.channel,
            0, p);
    current[i] = p;
  }
}

// ===== 足先指定で動かす =====
void moveFootTo(float xf, float ys, float zd, int duration_ms) {
  float yaw, hip, knee;
  if (!ik3d(xf, ys, zd, &yaw, &hip, &knee)) {
    Serial.println(F("IK unreachable"));
    return;
  }
  int targets[NUM_LEG_SERVOS] = {
    angleToPWM(yawCal,  yaw),
    angleToPWM(hipCal,  hip),
    angleToPWM(kneeCal, knee)
  };
  startMove(targets, duration_ms);
}

void setup() {
  Serial.begin(9600);
  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  // 初期姿勢：脚を真下に伸ばす
  current[0] = angleToPWM(yawCal,  0.0f);
  current[1] = angleToPWM(hipCal,  0.0f);
  current[2] = angleToPWM(kneeCal, 0.5f);
  pwm.setPWM(yawCal.channel,  0, current[0]);
  pwm.setPWM(hipCal.channel,  0, current[1]);
  pwm.setPWM(kneeCal.channel, 0, current[2]);
  delay(500);
}

// 足先で半径 r の円を描く
void loop() {
  static float t = 0.0f;
  static unsigned long last = 0;

  updateMotion();

  if (!active && millis() - last > 200) {
    float cx = 0.0f;     // 円の中心 x
    float cy = 0.0f;     // 円の中心 y (sideways)
    float cz = 80.0f;    // 円の中心 z (下方向)
    float r  = 20.0f;    // 半径

    float xf = cx + r * cosf(t);
    float zd = cz + r * sinf(t);
    moveFootTo(xf, cy, zd, 200);

    t += 0.3f;
    if (t > 2 * M_PI) t -= 2 * M_PI;
    last = millis();
  }
}
