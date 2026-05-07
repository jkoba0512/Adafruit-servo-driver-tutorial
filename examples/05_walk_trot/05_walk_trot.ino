/*
  Chapter 6: 4脚歩行ゲイトジェネレータ（完成版）

  4脚 × 3 DOF（股ヨー + 股ピッチ + 膝） = 計 12 サーボ
  PCA9685 の ch 0〜11 に下記のように接続:

      yaw   hip   knee
  FR  ch0   ch1   ch2
  FL  ch3   ch4   ch5
  RR  ch6   ch7   ch8
  RL  ch9   ch10  ch11

  ※ 自分のロボットに合わせて Leg[] を必ず調整してください。
  ※ いきなり地面で動かさず、まず空中で動作確認すること。
*/

#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
#include <math.h>

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVO_FREQ 50

// ===== サーボキャリブレーション =====
struct ServoCal {
  uint8_t channel;
  int     pwmMin, pwmMax;
  float   angleAtMin, angleAtMax;  // [rad]
  float   offset;                  // [rad]
  int     direction;               // +1 or -1
};

int angleToPWM(const ServoCal &s, float angle_rad) {
  float a = s.direction * angle_rad + s.offset;
  float t = (a - s.angleAtMin) / (s.angleAtMax - s.angleAtMin);
  if (t < 0.0f) t = 0.0f;
  if (t > 1.0f) t = 1.0f;
  return s.pwmMin + (int)((s.pwmMax - s.pwmMin) * t);
}

// ===== Leg 構造体 =====
enum LegId { FR = 0, FL, RR, RL, NUM_LEGS };

struct Leg {
  ServoCal yaw, hip, knee;
  float    L1, L2;        // [mm]
  float    offset;        // ゲイト位相オフセット
  float    side_sign;     // +1 = 右, -1 = 左
};

Leg legs[NUM_LEGS];

// ===== IK =====
bool ik2d(float x, float y, float L1, float L2,
          float *hip, float *knee) {
  float d = sqrtf(x * x + y * y);
  if (d > L1 + L2) return false;
  if (d < fabsf(L1 - L2)) return false;
  float alpha = atan2f(x, y);
  float cb = (L1*L1 + d*d - L2*L2) / (2.0f * L1 * d);
  cb = constrain(cb, -1.0f, 1.0f);
  float beta = acosf(cb);
  float cg = (L1*L1 + L2*L2 - d*d) / (2.0f * L1 * L2);
  cg = constrain(cg, -1.0f, 1.0f);
  float gamma = acosf(cg);
  *hip  = alpha + beta;        // 膝前構成
  *knee = (float)M_PI - gamma;
  return true;
}

bool ik3d(float xf, float ys, float zd, float L1, float L2,
          float *yaw, float *hip, float *knee) {
  *yaw = atan2f(ys, xf);
  float xp = sqrtf(xf * xf + ys * ys);
  return ik2d(xp, zd, L1, L2, hip, knee);
}

// ===== 歩行パラメータ =====
float cycle_time   = 2.0f;     // [sec/cycle]
float duty         = 0.75f;    // クロール = 0.75, トロット = 0.5
float stride       = 50.0f;    // [mm]
float step_height  = 25.0f;    // [mm]
float z_default    = 90.0f;    // [mm] 標準接地高
float forward_x    = 30.0f;    // [mm] 中立位置の前後オフセット

// ゲイトプリセット
const float OFFSET_CRAWL[NUM_LEGS] = {0.00f, 0.50f, 0.75f, 0.25f};
const float OFFSET_TROT [NUM_LEGS] = {0.00f, 0.50f, 0.50f, 0.00f};

// ===== 足先軌跡 =====
void footTrajectory(float p, float *xf, float *ys, float *zd) {
  float swing_dur = 1.0f - duty;
  if (p < swing_dur) {
    float u = p / swing_dur;            // 0..1 in swing
    *xf = forward_x + (-stride/2 + stride * u);
    *zd = z_default - step_height * sinf((float)M_PI * u);
  } else {
    float u = (p - swing_dur) / duty;   // 0..1 in stance
    *xf = forward_x + (stride/2 - stride * u);
    *zd = z_default;
  }
  *ys = 0.0f;
}

// ===== グローバル状態 =====
float phase_global = 0.0f;
unsigned long last_t = 0;

void update(float dt_sec) {
  phase_global += dt_sec / cycle_time;
  while (phase_global >= 1.0f) phase_global -= 1.0f;

  for (int i = 0; i < NUM_LEGS; i++) {
    float p = phase_global + legs[i].offset;
    while (p >= 1.0f) p -= 1.0f;

    float xf, ys, zd;
    footTrajectory(p, &xf, &ys, &zd);
    ys *= legs[i].side_sign;

    float yaw, hip, knee;
    if (!ik3d(xf, ys, zd, legs[i].L1, legs[i].L2, &yaw, &hip, &knee)) {
      continue;  // 到達不能ならスキップ
    }

    pwm.setPWM(legs[i].yaw.channel,  0, angleToPWM(legs[i].yaw,  yaw));
    pwm.setPWM(legs[i].hip.channel,  0, angleToPWM(legs[i].hip,  hip));
    pwm.setPWM(legs[i].knee.channel, 0, angleToPWM(legs[i].knee, knee));
  }
}

// ===== セットアップ：脚の定義 =====
void setupLegs() {
  // すべて同じリンク長と仮定（自機に合わせて変えること）
  const float L1 = 50.0f;
  const float L2 = 60.0f;

  // ---- FR (前右) ----
  legs[FR].yaw  = {0,  150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
  legs[FR].hip  = {1,  150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
  legs[FR].knee = {2,  150, 600,  0.0f,    M_PI,  0.0f, +1};
  legs[FR].L1 = L1; legs[FR].L2 = L2;
  legs[FR].side_sign = +1;

  // ---- FL (前左) ----
  legs[FL].yaw  = {3,  150, 600, -M_PI/2, M_PI/2, 0.0f, -1}; // ミラー
  legs[FL].hip  = {4,  150, 600, -M_PI/2, M_PI/2, 0.0f, -1};
  legs[FL].knee = {5,  150, 600,  0.0f,    M_PI,  0.0f, -1};
  legs[FL].L1 = L1; legs[FL].L2 = L2;
  legs[FL].side_sign = -1;

  // ---- RR (後右) ----
  legs[RR].yaw  = {6,  150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
  legs[RR].hip  = {7,  150, 600, -M_PI/2, M_PI/2, 0.0f, +1};
  legs[RR].knee = {8,  150, 600,  0.0f,    M_PI,  0.0f, +1};
  legs[RR].L1 = L1; legs[RR].L2 = L2;
  legs[RR].side_sign = +1;

  // ---- RL (後左) ----
  legs[RL].yaw  = {9,  150, 600, -M_PI/2, M_PI/2, 0.0f, -1};
  legs[RL].hip  = {10, 150, 600, -M_PI/2, M_PI/2, 0.0f, -1};
  legs[RL].knee = {11, 150, 600,  0.0f,    M_PI,  0.0f, -1};
  legs[RL].L1 = L1; legs[RL].L2 = L2;
  legs[RL].side_sign = -1;

  // ゲイト適用：クロール
  for (int i = 0; i < NUM_LEGS; i++) {
    legs[i].offset = OFFSET_CRAWL[i];
  }
}

void setup() {
  Serial.begin(9600);
  Serial.println(F("Quadruped gait generator"));

  pwm.begin();
  pwm.setPWMFreq(SERVO_FREQ);

  setupLegs();

  // ===== 起動時：中立姿勢へ =====
  // 安全のため p=0.99 (= スタンス期の終端) で停止状態を作る
  phase_global = 0.99f;
  update(0.0f);
  delay(2000);  // 全脚が中立姿勢に落ち着くまで待機

  Serial.println(F("Starting walk in 3..2..1"));
  delay(3000);

  last_t = millis();
}

void loop() {
  unsigned long now = millis();
  float dt = (now - last_t) * 0.001f;
  last_t = now;

  update(dt);

  delay(20);  // 50 Hz の更新レート
}
