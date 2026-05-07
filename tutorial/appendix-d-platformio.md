---
title: "付録 D: VS Code + PlatformIO で進める"
parent: チュートリアル
nav_order: 10
---

# 付録 D: VS Code + PlatformIO で進める

VS Code + PlatformIO のインストール手順や基本的な使い方は、別資料にまとめてあります。
未セットアップの方はこちらを先にご参照ください。

📖 **[VSCode + PlatformIO + Arduino セットアップ資料 (Notion)](https://tasty-eyeliner-3a3.notion.site/VSCode-PlatformIO-Arduino-333e1b8189ac800bb65cef402e3702c0)**

ここでは **本チュートリアル固有の事項**だけまとめます。

## このリポジトリのプロジェクト構成

各 `examples/0X_xxx/` フォルダが **独立した PlatformIO プロジェクト**として
動くように `platformio.ini` を同梱しています。

```
examples/
├── 01_single_servo/
│   ├── 01_single_servo.ino
│   └── platformio.ini       ← このフォルダを VS Code で「開く」
├── 01b_calibration/
│   ├── 01b_calibration.ino
│   └── platformio.ini
├── 02_multi_servo/
│   ├── 02_multi_servo.ino
│   └── platformio.ini
└── ...
```

> 💡 リポジトリのルート（`Adafruit-servo-driver-tutorial/` 全体）を開いても
> PlatformIO はプロジェクトとして認識しません。
> **必ず `examples/0X_xxx/` フォルダ単体を開く**こと。

## platformio.ini の中身

```ini
[platformio]
src_dir = .

[env:uno]
platform = atmelavr
board = uno
framework = arduino
monitor_speed = 9600
lib_deps =
    adafruit/Adafruit PWM Servo Driver Library
```

このうち本チュートリアル固有なのは `lib_deps` の行だけです。
PlatformIO が **初回ビルド時に Adafruit_PWMServoDriver を自動ダウンロード**するので、
ライブラリの手動インストールは不要です。

## やってみよう

1. 上記の Notion 資料に従って VS Code + PlatformIO のセットアップを完了させる
2. `examples/01_single_servo/` フォルダを VS Code で開く
3. ビルド（✓）→ 書き込み（→）→ シリアルモニタ（🔌）の順に実行
4. シリアルモニタに `Single servo test start` が出れば成功

---

[◀ 付録 C へ](appendix-c-troubleshooting.md) | [🏠 README に戻る](../README.md)
