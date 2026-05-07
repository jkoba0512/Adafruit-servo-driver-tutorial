---
title: "付録 B: デバッグ術"
parent: チュートリアル
nav_order: 8
---

# 付録 B: デバッグ術

「動かない！」となったときの **切り分け順序**をまとめます。
**いきなり全部疑わない**で、上から順に確認していくのがコツです。

## デバッグの順序

```
[1] Arduino はそもそも生きているか？
        ↓ Yes
[2] I²C 通信は通っているか？（PCA9685 を Arduino が認識しているか）
        ↓ Yes
[3] PCA9685 から PWM が出ているか？（テスタや LED で確認）
        ↓ Yes
[4] サーボに正しい PWM パルス幅が届いているか？
        ↓ Yes
[5] サーボに十分な電源が来ているか？
        ↓ Yes
[6] アルゴリズム / IK / 角度変換が正しいか？
```

## [1] Arduino の生死確認：L チカ

最初に必ずやるべき確認。

```cpp
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  Serial.println("Hello");
}
void loop() {
  digitalWrite(LED_BUILTIN, HIGH); delay(500);
  digitalWrite(LED_BUILTIN, LOW);  delay(500);
}
```

シリアルモニタに `Hello` が出て、内蔵 LED が点滅すれば OK。

## [2] I²C スキャナで PCA9685 を確認

PCA9685 のデフォルトアドレスは `0x40`。
これが見えなければ配線・電源・I²C 自体に問題があります。

```cpp
// I2C scanner
#include <Wire.h>

void setup() {
  Wire.begin();
  Serial.begin(9600);
  Serial.println("\nI2C Scanner");
}

void loop() {
  byte found = 0;
  for (byte addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.print("Found 0x");
      if (addr < 16) Serial.print("0");
      Serial.println(addr, HEX);
      found++;
    }
  }
  if (found == 0) Serial.println("No devices found");
  delay(2000);
}
```

### 期待結果

```
I2C Scanner
Found 0x40    ← PCA9685
Found 0x70    ← All-Call address (PCA9685 のグローバル制御アドレス)
```

### 出ないとき

- SDA / SCL の配線間違い（A4=SDA, A5=SCL）
- VCC が来ていない
- ジャンパワイヤ断線
- I²C プルアップ抵抗が足りない（基板内蔵のはずだが、長配線なら追加検討）

## [3] PWM 出力の確認

サーボを外し、ch 0 の PWM 端子と GND の間に **LED + 抵抗** を入れて
明るさが変わるか確認。

```cpp
void setup() {
  pwm.begin();
  pwm.setPWMFreq(50);
}
void loop() {
  pwm.setPWM(0, 0, 0);    delay(500);   // 出力ゼロ → LED 消灯
  pwm.setPWM(0, 0, 2048); delay(500);   // 50% → LED 中明
  pwm.setPWM(0, 0, 4095); delay(500);   // フル → LED 明るい
}
```

オシロやテスタ（DC モード）があれば、ch 0 の電圧が変化するか確認できます。

## [4] サーボに届くパルスを目視・聴覚で確認

サーボを ch 0 に接続し、`SERVOMIN ↔ SERVOMAX` で往復スケッチ（Ch 1 のもの）を実行。

- **ジリジリと音だけして動かない** → パルス幅が範囲外、または電源不足
- **ガクッと一瞬動いて止まる** → 電源容量不足、リセット
- **連続で震える** → GND が共通になっていない / パルス幅が境界値
- **ゆっくり一方向に流れる** → 360° 連続回転サーボ（普通の RC サーボではない）が混入

## [5] 電源確認

サーボが動くタイミングで、**サーボ電源端子** の電圧をテスタで測ります。

- 通常時 5V → サーボ動作時に 3V まで落ちる → **電源容量不足**
- 通常時 5V → 動作時 4.5V くらいで安定 → OK
- 5V がそもそも来ていない → 配線・電源の故障

## [6] アルゴリズムの確認

ハード側がOKならソフトウェアを疑います。

### 役立つテクニック

1. **シリアル出力を入れる**
   ```cpp
   Serial.print("yaw="); Serial.print(yaw * 180/M_PI);
   Serial.print(" hip="); Serial.print(hip * 180/M_PI);
   Serial.print(" knee="); Serial.println(knee * 180/M_PI);
   ```
2. **動作を遅く**して目視追跡できるようにする（`cycle_time = 10.0` など）
3. **1脚だけ更新**にして他は固定 → 怪しい脚を絞り込む
4. **IK の入力をログ**して、想定範囲内か確認
   ```cpp
   Serial.print("foot=("); Serial.print(xf); Serial.print(",");
   Serial.print(ys); Serial.print(","); Serial.print(zd);
   Serial.println(")");
   ```
5. **PWM カウントを直接ログ**
   ```cpp
   Serial.print("pwm yaw="); Serial.print(angleToPWM(...));
   ```

### 数値が NaN になっているケース

`acosf(x)` に `|x| > 1.0` を渡すと NaN を返します。
余弦定理の前に `constrain` するのを忘れていないか確認してください。

## デバッグ用便利関数

ロボット動作中に Serial を読みやすくするためのテンプレ：

```cpp
void debugLeg(int legId) {
  Serial.print("[L"); Serial.print(legId); Serial.print("] ");
  Serial.print("phase="); Serial.print(phase_global, 2);
  // ... 他の情報も
  Serial.println();
}
```

`millis() % 200 == 0` のように **間引いて出力**しないと、シリアルが詰まって
歩行が遅くなることがあります。

## まとめ

- 上から順にレイヤを切り分ける（Arduino → I²C → PWM → サーボ → 電源 → SW）
- I²C scanner は **必ず手元に持っておく**
- 「ジリジリ音」は GND or 電源 or パルス範囲を疑う
- アルゴリズムは「動作を遅くする＋シリアル出力」で大半は解ける

---

[◀ 付録 A へ](appendix-a-power.md) | [▶ 付録 C へ](appendix-c-troubleshooting.md)
