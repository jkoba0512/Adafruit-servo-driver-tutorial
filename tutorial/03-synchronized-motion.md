---
title: "Ch 3: 同期制御 = 時間補間"
parent: チュートリアル
nav_order: 3
---

# Chapter 3: 同期制御 = 時間補間

## 学習目標

- 「同期して動かす」を **時間補間（time-based interpolation）** で実現する考え方を理解する
- 線形補間（Linear Interpolation, lerp）の式を書ける
- ブロッキング版・ノンブロッキング版の両方を実装できる
- ノンブロッキングでは `millis()` を使って `delay()` を避ける理由を説明できる

## 考え方：「目標」ではなく「軌跡」を送る

Chapter 2 で見たように、`pwm.setPWM(ch, 0, target)` を一発送るだけでは、
サーボはそれぞれ自分のペースで動いてしまいます。

そこで発想を変えます。

> **「目標値」を1回送るのではなく、
>  「現在 → 目標」の途中の値を細かく刻んで何回も送る。**

すべてのサーボに対して、**同じ刻み幅・同じ間隔**で命令を送れば、
**全部が同じ瞬間にゴールへ到着**します。

```
時刻 →

ch0 (短距離)  ●─●─●─●─●─●─●─●─●─●─●●  (毎回ちょっとずつ進む)
ch1 (中距離)  ●─●──●──●──●──●──●──●─●●
ch3 (長距離)  ●──●──●──●──●──●──●──●──●●

              ↑                       ↑
            スタート               全員同じ時刻に到着！
```

## 線形補間（Linear Interpolation, lerp）の式

スタート位置を `start`、目標位置を `end`、所要時間を `duration` 、
スタートからの経過時間を `t` とすると、現時点の位置は次の式で求まります。

```
position(t) = start + (end - start) * (t / duration)
```

- `t = 0` のとき → `position = start`
- `t = duration` のとき → `position = end`
- 途中は **直線的に** 補間される（だから "linear")

C 言語的には:

```cpp
float ratio = (float)t / (float)duration;     // 0.0 ～ 1.0
int   pos   = start + (int)((end - start) * ratio);
```

## まずはブロッキング版で実装

理解しやすさ優先で、**`delay()` を使った実装**から始めます。

```cpp
void moveAllToBlocking(int targets[], int n, int duration_ms) {
  static int current[NUM_SERVOS];  // 現在位置を記憶
  const int STEP_MS = 20;          // 何 ms ごとに更新するか
  int steps = duration_ms / STEP_MS;

  for (int s = 1; s <= steps; s++) {
    float ratio = (float)s / (float)steps;
    for (int i = 0; i < n; i++) {
      int pos = current[i] + (int)((targets[i] - current[i]) * ratio);
      pwm.setPWM(CH[i], 0, pos);
    }
    delay(STEP_MS);
  }

  // 最終位置を記憶
  for (int i = 0; i < n; i++) current[i] = targets[i];
}
```

### 使い方

```cpp
int A[NUM_SERVOS] = {SERVOMIN+50, SERVOMIN+150, SERVOMIN+300, SERVOMAX};
int B[NUM_SERVOS] = {SERVOMIN, SERVOMIN, SERVOMIN, SERVOMIN};

void loop() {
  moveAllToBlocking(A, NUM_SERVOS, 1000);  // 1秒かけて A へ
  delay(500);
  moveAllToBlocking(B, NUM_SERVOS, 1500);  // 1.5秒かけて B へ
  delay(500);
}
```

これだけで Chapter 2 の問題は解決します。
4 個のサーボが **1 秒ぴったりで一斉に** 目標位置に到着します。

## ブロッキングの限界

ブロッキング版（`delay()` あり）は分かりやすいですが、欠点があります。

- 動作中は他の処理（センサ読み、シリアル受信など）ができない
- 連続的な歩行ゲイトを作るとき、隙間時間がもったいない
- 「動かしながら同時にボタン入力を受け付けたい」が無理

そこで本格運用では **ノンブロッキング版** に書き直します。

## ノンブロッキング版

`delay()` をやめて、`loop()` のたびに「今の経過時間に対応する位置」を計算します。

```cpp
struct MotionState {
  int   start[NUM_SERVOS];     // 開始位置
  int   target[NUM_SERVOS];    // 目標位置
  unsigned long t_start;       // 開始時刻 [ms]
  unsigned long duration;      // 所要時間 [ms]
  bool  active;
};

MotionState motion;

// 現在位置を記憶しておく
int current[NUM_SERVOS] = {SERVOMIN, SERVOMIN, SERVOMIN, SERVOMIN};

// 「targets へ duration ms かけて移動開始」
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
    // 完了：終端値で固定
    for (int i = 0; i < NUM_SERVOS; i++) {
      pwm.setPWM(CH[i], 0, motion.target[i]);
      current[i] = motion.target[i];
    }
    motion.active = false;
    return;
  }

  float ratio = (float)elapsed / (float)motion.duration;
  for (int i = 0; i < NUM_SERVOS; i++) {
    int pos = motion.start[i]
            + (int)((motion.target[i] - motion.start[i]) * ratio);
    pwm.setPWM(CH[i], 0, pos);
    current[i] = pos;
  }
}
```

### メインループ側

```cpp
unsigned long lastSwitch = 0;
bool atA = false;

void loop() {
  updateMotion();   // 毎回呼ぶだけ

  // 2秒ごとに目標を切り替え
  if (millis() - lastSwitch > 2000) {
    int A[NUM_SERVOS] = {SERVOMIN+50, SERVOMIN+150, SERVOMIN+300, SERVOMAX};
    int B[NUM_SERVOS] = {SERVOMIN, SERVOMIN, SERVOMIN, SERVOMIN};
    startMove(atA ? B : A, 1000);
    atA = !atA;
    lastSwitch = millis();
  }

  // ここに他の処理（センサ・通信）を書ける ↓↓↓
  // readSensors();
  // checkButtons();
}
```

### 重要ポイント

- `loop()` の中で `updateMotion()` を **毎回呼ぶ**
- `startMove()` を呼んだら、あとは勝手に補間が進む
- 補間中でも他の処理を並行して書ける
- `current[]` 配列に「最後にどこへ送ったか」を覚えておくのが肝心
  （次の動作の「開始位置」に使うため）

## 補間カーブを変える（応用）

直線補間（lerp）だと **動き始めと終わりが急** で、機械的に見えます。
**イージング（easing）** を入れると滑らかになります。

代表的な「smoothstep」関数:

```cpp
float smoothstep(float t) {
  // t は 0.0〜1.0
  return t * t * (3.0 - 2.0 * t);
}

// 使い方: ratio をそのまま使う代わりに
float ratio   = (float)elapsed / motion.duration;
float eased   = smoothstep(ratio);
int   pos     = start + (int)((target - start) * eased);
```

```
直線補間:        smoothstep:
1 ┤    ╱        1 ┤      ╱──
  │   ╱           │    ╱
  │  ╱            │  ╱
  │ ╱             │ ╱
0 ┤╱           0 ┤╱
  └─────────      └─────────
  0       1       0       1
  急発進・急停止   ゆっくり始まり、ゆっくり止まる
```

ロボットの歩行では `smoothstep` を入れるとサーボへの負荷が下がり、
電流ピークも減って電源にも優しくなります。

## やってみよう（演習）

1. ブロッキング版 `moveAllToBlocking()` を実装し、Chapter 2 の "バラバラ問題" が
   解決していることを目視で確認せよ
2. ノンブロッキング版に書き換え、`loop()` の中で `Serial.println("alive")` を
   毎回呼んでも、補間が止まらないことを確認せよ
3. `duration` を 200 ms と 3000 ms で比べ、サーボの動きの違いを観察せよ
4. `smoothstep` を入れて、見た目の滑らかさが変わることを確認せよ
5. （発展）`STEP_MS = 20` を `5`, `50`, `100` と変えて、
   どこからカクカクし始めるか調べよ

## まとめ

- **同期制御 = 全サーボに同じ時間割で位置を送り続けること**
- 線形補間: `pos(t) = start + (end - start) * t / duration`
- 学習用にはブロッキング版でOK、実機にはノンブロッキング版
- ノンブロッキングでは **現在位置 `current[]` の管理** がカギ
- イージング（smoothstep）で動きを滑らかにできる

これで「複数サーボを同期制御する」基礎は完成です。
次の Chapter 4 では、いよいよ **「足先を動かしたい座標」からサーボ角度を逆算する**
逆運動学（Inverse Kinematics, IK）に進みます。

---

[◀ Chapter 2 へ](02-multi-servo.md) | [▶ Chapter 4 へ](04-leg-kinematics.md)
