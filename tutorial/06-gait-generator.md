---
title: "Ch 6: ゲイトジェネレータ実装"
parent: チュートリアル
nav_order: 6
---

# Chapter 6: ゲイトジェネレータ実装

> ⚠ 多数のサーボを高負荷で連続動作させます。電源容量・機構の安全確認を十分行い、
> [免責事項](../README.md#免責事項) を理解した上で実施してください。

## 学習目標

- これまでの Chapter（同期・IK・ゲイト）を **1 つのスケッチに統合**できる
- 12 個（4 脚 × 3 DOF）または 8 個（4 脚 × 2 DOF）のサーボを
  毎ループ更新するゲイトジェネレータの構造を理解する
- パラメータ（`cycle_time`, `stride`, `step_height`）の意味を体感的に把握する
- 自分のロボットの寸法・取り付けに合わせて調整できる

## 全体アーキテクチャ

```
┌─────────────────────────────────────────────────────────┐
│  loop()                                                 │
│                                                         │
│   1. dt = millis() - last_t                            │
│   2. phase_global += dt / cycle_time                   │
│   3. for each leg in [FR, FL, RR, RL]:                  │
│         phase_leg = (phase_global + offset[leg]) mod 1  │
│         (xf, ys, zd) = footTrajectory(phase_leg)        │
│         (yaw, hip, knee) = IK(xf, ys, zd)               │
│         setPWM(ch_yaw,  angleToPWM(yaw))                │
│         setPWM(ch_hip,  angleToPWM(hip))                │
│         setPWM(ch_knee, angleToPWM(knee))               │
│   4. last_t = millis()                                  │
└─────────────────────────────────────────────────────────┘
```

> 💡 ここでは Chapter 3 の `startMove()` 型の補間は **使いません**。
> 歩行軌道は時間の関数として連続的に定義されているので、
> **毎ループ最新の目標値を送る**だけで自然に滑らかな動きになります。
> （補間は「不連続な姿勢遷移（待機 → 歩き始め）」のときに使います）

## チャンネル割り当て例

12 サーボ（4脚 × 3DOF）の場合：

| 脚 | yaw | hip | knee |
|----|-----|-----|------|
| FR（前右）| ch 0 | ch 1 | ch 2 |
| FL（前左）| ch 3 | ch 4 | ch 5 |
| RR（後右）| ch 6 | ch 7 | ch 8 |
| RL（後左）| ch 9 | ch 10 | ch 11 |

> 学生作の機体は配線都合でチャンネル順がバラバラになりがちです。
> **ServoCal[] の `.channel` を書き換えるだけ**で対応できる構造にしておきます。

## データ構造

```cpp
enum LegId { FR = 0, FL, RR, RL, NUM_LEGS };

struct Leg {
  ServoCal yaw, hip, knee;   // 3つのサーボのキャリブレーション
  float    L1, L2;           // 大腿・脛のリンク長 [mm]
  float    offset;           // ゲイト位相オフセット
  float    side_sign;        // +1 (右) / -1 (左) でヨー方向反転
};

Leg legs[NUM_LEGS];
```

## メインループの心臓部

```cpp
void update(float dt_sec) {
  phase_global += dt_sec / cycle_time;
  if (phase_global >= 1.0f) phase_global -= 1.0f;

  for (int i = 0; i < NUM_LEGS; i++) {
    float p = phase_global + legs[i].offset;
    while (p >= 1.0f) p -= 1.0f;

    float xf, ys, zd;
    footTrajectory(p, &xf, &ys, &zd);

    // 旋回や左右補正を入れる場所
    ys *= legs[i].side_sign;

    float yaw, hip, knee;
    if (!ik3d(xf, ys, zd, legs[i].L1, legs[i].L2, &yaw, &hip, &knee)) {
      // 到達不能 → スキップ（前回値が残る）
      continue;
    }

    pwm.setPWM(legs[i].yaw.channel,  0, angleToPWM(legs[i].yaw,  yaw));
    pwm.setPWM(legs[i].hip.channel,  0, angleToPWM(legs[i].hip,  hip));
    pwm.setPWM(legs[i].knee.channel, 0, angleToPWM(legs[i].knee, knee));
  }
}
```

## 立ち上げ手順（動作確認）

ハードを組み終わったら、いきなり歩行サイクルに入れず **段階を踏みます**。

### Step 1: 全サーボを「中立姿勢」に置く

電源を入れたら、必ず安全な中立姿勢（脚を真下に伸ばした状態など）に
**ゆっくり** 移動させます（Ch 3 の `startMove()` を使う）。
この段階で脚が机に引っかかったり、ギアが鳴る場合はすぐ停止して再キャリブレーション。

### Step 2: 1脚だけスイング軌道を描かせる

`update()` を「1 脚だけ」呼ぶように改造して、足先の動きを目視確認。
→ 円弧（半円）状の軌跡を描いていれば OK。

### Step 3: 4脚同時、ただし機体は **手で持ち上げて** 動かす

地面に下ろすと突然走り出してしまうので、まずは空中で動作確認。
左右対称・対角対称になっていれば歩けます。

### Step 4: 接地して低速から

`cycle_time` を大きく（例: 4.0 秒）、`stride` を小さく（例: 30 mm）にして
**ゆっくり**から始めます。
クロール（duty=0.75）でスタートし、慣れたらトロット（duty=0.5）へ。

## 完成スケッチ

`examples/05_walk_trot/05_walk_trot.ino` に置いてあります。
要点を抜粋：

```cpp
const float cycle_time   = 2.0f;     // [sec/cycle]
const float duty         = 0.75f;    // クロール
const float stride       = 50.0f;    // [mm]
const float step_height  = 25.0f;    // [mm]
const float z_default    = 90.0f;    // [mm]

const float OFFSET_CRAWL[NUM_LEGS] = {0.00f, 0.50f, 0.75f, 0.25f};
const float OFFSET_TROT [NUM_LEGS] = {0.00f, 0.50f, 0.50f, 0.00f};

void loop() {
  unsigned long now = millis();
  float dt = (now - last_t) * 0.001f;
  last_t = now;

  update(dt);

  // CPU を食いすぎないよう少しだけ休ませる
  delay(20);
}
```

## チューニングのコツ

| パラメータ | 大きくすると | 小さくすると |
|-----------|-------------|-------------|
| `cycle_time` | ゆっくり歩く | 速くなるが追従できないと滑る |
| `stride` | 一歩が大きい・速い | 細かく刻む・力が出ない |
| `step_height` | 障害物を越えやすい | 滑らか・速いが引っかかる |
| `z_default` | 重心が低い・安定 | 重心が高い・速いが転びやすい |
| `duty` | 安定（クロール側） | 速いがバランスが要る |

「まず歩かせる」ためのオススメ初期値：

```
cycle_time = 3.0
stride     = 40
step_height= 20
z_default  = 90
duty       = 0.75 （クロール）
```

歩けたら徐々に `cycle_time` を縮め、`stride` を伸ばします。

## トラブル：歩かないとき

- 1歩進むけど次でこける → `stride` 大きすぎ、`step_height` 小さすぎ
- 足を上げる前にズリズリ動く → `step_height` 小さすぎ、または接地高さ `z_default` が足りない
- 後ろにしか進まない → スタンス期の x の符号が逆。`stride/2 - stride * p` を `-stride/2 + stride * p` に
- ガクガクして電源が落ちる → 電源容量不足（[付録 A](appendix-a-power.md)）
- 4本中1本だけ変な動き → そのサーボ単体のキャリブレーションが間違い

詳しくは [付録 C: トラブル集](appendix-c-troubleshooting.md) も参照。

## やってみよう（演習）

1. クロールで前進できることを確認したら、`OFFSET[]` を `OFFSET_TROT` に切り替えて違いを比較せよ
2. ボタン or シリアル入力で `OFFSET[]` と `duty` を切り替えられるようにせよ
3. 左右の `stride` を変えて、その場旋回を実装せよ
4. （発展）`stride`, `step_height` を **slowly に変化**させて加減速できるようにせよ
5. （発展）IMU を載せて、転倒検出 → 起き上がりルーチンを呼ぶ仕組みを追加せよ

## まとめ

- ゲイトジェネレータ = **時間の関数として全脚の足先座標を生成し、IK して PWM へ流す**
- `phase_global` という1つの「歩行時計」で 4脚が自然に同期する
- 段階を踏んで動作確認することで、サーボ・機構を壊さずに立ち上げられる
- パラメータ（`cycle_time`, `stride`, `step_height`, `duty`）の調整が歩きの良し悪しを決める

これでチュートリアル本編は完了です。
あとは付録で **電源・デバッグ・トラブル**周りを補完してください。

---

[◀ Chapter 5 へ](05-walking-gaits.md) | [▶ 付録 A へ](appendix-a-power.md)
