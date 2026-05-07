---
title: ホーム
layout: home
nav_order: 1
---

# Adafruit PCA9685 で4脚ロボットを歩かせるチュートリアル

Arduino Uno と Adafruit 16-Channel PWM/Servo Driver（PCA9685）を使って、
**自作4脚ロボットの RC サーボを同期制御**できるようになるための実習教材です。

📖 **公開サイト: <https://jkoba0512.github.io/Adafruit-servo-driver-tutorial/>**

> ⚠ 実習を始める前に、必ず本ページ末尾の [免責事項](#免責事項) をお読みください。

## 対象者

- C 言語の基礎は学習済み
- Arduino / 組み込みは初学者
- これから4脚（または多脚）ロボットを設計・製作したい

## 学習のゴール

このチュートリアルを終えると、次のことができるようになります。

1. PCA9685 の基本的な使い方（配線・I²C・PWM）を説明できる
2. 1 個のサーボを目的の角度に動かせる
3. 複数サーボを **同じ時刻に目標角度へ到達させる**「同期制御」が書ける
4. 1 脚分の逆運動学（IK）で「足先座標 → サーボ角度」を計算できる
5. 4 脚ロボットを **クロール / トロット**で歩かせられる

## チュートリアルの進め方

| 章 | タイトル | 概要 |
|----|---------|------|
| [Ch 0](tutorial/00-pca9685-overview.md) | PCA9685 とは | サーボドライバの仕組みと役割 |
| [Ch 1](tutorial/01-single-servo.md) | 1 個のサーボを動かす | 配線・最小コード・キャリブレーション |
| [Ch 2](tutorial/02-multi-servo.md) | 複数サーボを同時に動かす | `setPWM` をループで呼ぶ／I²C 帯域 |
| [Ch 3](tutorial/03-synchronized-motion.md) | 同期制御 = 時間補間 | 全サーボを同じ時刻にゴールへ |
| [Ch 4](tutorial/04-leg-kinematics.md) | 1 脚の運動学入門 | 2-/3-DOF 脚の IK |
| [Ch 5](tutorial/05-walking-gaits.md) | 4 脚歩行ゲイト | クロール・トロットの位相設計 |
| [Ch 6](tutorial/06-gait-generator.md) | ゲイトジェネレータ実装 | IK + 位相生成で歩かせる |
| 付録 A | [電源設計](tutorial/appendix-a-power.md) | サーボ電源の選び方 |
| 付録 B | [デバッグ術](tutorial/appendix-b-debug.md) | 動かないときの切り分け |
| 付録 C | [トラブル集](tutorial/appendix-c-troubleshooting.md) | よくある症状と対処 |
| 付録 D | [VS Code + PlatformIO で進める](tutorial/appendix-d-platformio.md) | Arduino IDE 以外で進めたい人向け（外部資料リンク） |

## サンプルコード

`examples/` 以下に章ごとの `.ino` スケッチを置いています。
**Arduino IDE / PlatformIO の両方に対応** しています（各フォルダに `platformio.ini` 同梱）。

```
examples/
├── 01_single_servo/   ... Ch 1 用（基本動作）
├── 01b_calibration/   ... Ch 1 用（キャリブレーション）
├── 02_multi_servo/    ... Ch 2 用
├── 03_sync_motion/    ... Ch 3 用
├── 04_leg_ik/         ... Ch 4 用
└── 05_walk_trot/      ... Ch 5・6 用（最終版）
```

- **Arduino IDE**: `examples/0X_xxx/0X_xxx.ino` をダブルクリックで開く
- **PlatformIO**: VS Code で `examples/0X_xxx/` フォルダを開く（プロジェクトとして認識される）

## 必要なハードウェア

- Arduino Uno（R3 以降）
- Adafruit PCA9685 16-Channel Servo Driver
- RC サーボ（SG90 / MG90S / MG996R など）× 8〜12 個
- **サーボ用電源**（5V 3〜5A 程度のスイッチング電源、または 4×単3 電池ボックス）
- ジャンパワイヤ、ブレッドボード、必要に応じてはんだごて

> ⚠ サーボの電源は **必ず Arduino の 5V とは別系統**で用意してください。
> 詳細は [付録 A: 電源設計](tutorial/appendix-a-power.md) を参照。

## 必要なソフトウェア

開発環境は次のどちらかを選んでください（**両方に対応**しています）。

### A. Arduino IDE（はじめての人向け）

- Arduino IDE（1.8 系または 2.x 系）
- ライブラリ: **Adafruit PWM Servo Driver Library**
  - Arduino IDE のライブラリマネージャで `adafruit pwm` を検索してインストール

### B. Visual Studio Code + PlatformIO（補完・Git 派向け）

- Visual Studio Code
- 拡張機能: **PlatformIO IDE**
- ライブラリ: 各 example フォルダの `platformio.ini` に依存記述済み
  → 初回ビルド時に自動ダウンロード

セットアップ全般は別資料にまとまっています:
📖 **[VSCode + PlatformIO + Arduino セットアップ資料 (Notion)](https://tasty-eyeliner-3a3.notion.site/VSCode-PlatformIO-Arduino-333e1b8189ac800bb65cef402e3702c0)**

このリポジトリ固有の使い方（プロジェクト構成・例の開き方）は
**[付録 D: VS Code + PlatformIO で進める](tutorial/appendix-d-platformio.md)** を参照。

## GitHub Pages として公開する手順

このリポジトリは [Jekyll](https://jekyllrb.com/) + [just-the-docs](https://just-the-docs.com/) テーマで
そのまま **GitHub Pages** に公開できます。

1. GitHub にリポジトリを作成して push
2. リポジトリの **Settings → Pages** を開く
3. **Source** を `Deploy from a branch` に設定
4. **Branch** を `main` の `/ (root)` に設定して保存
5. 数分待つと `https://<ユーザー名>.github.io/<リポジトリ名>/` で公開される

ローカルプレビューしたい場合は `Gemfile` を使って:

```bash
bundle install
bundle exec jekyll serve
# → http://localhost:4000 で確認
```

## ライセンス

本教材（文書および Arduino サンプルコード）は **MIT License** の下で提供されています。
詳細は [LICENSE](LICENSE) を参照してください。

PBL 講義・自学習・改変・再配布のいずれの目的でも自由にご利用いただけます。

## 免責事項

本教材は教育目的で提供されています。記載内容は執筆時点での情報であり、
**正確性・完全性・最新性を保証するものではありません。**

本教材の内容を実践する際は、以下の点に十分ご注意ください。

- **電気的安全**: 電源・配線の取り扱いには細心の注意を払ってください。
  誤接続・容量不足・短絡は、機器の損傷・発火の原因となります。
- **機械的安全**: 動作するロボットには指の挟み込み・落下・転倒等の危険があります。
  動作確認は周囲の人や物に被害が出ない安全な環境で行ってください。
- **部品の損傷**: 誤った配線・パルス幅・パラメータ設定により、
  サーボモータ・PCA9685・Arduino 等の部品が損傷する可能性があります。
- **キャリブレーション**: サーボの可動範囲は機種・個体により異なります。
  必ず実機で測定した上で `SERVOMIN` / `SERVOMAX` を設定してください。

本教材の利用により生じたいかなる損害（機器の損傷・人的損害・データ損失・
逸失利益等を含むが、これらに限らない）についても、著者および提供者は
**一切の責任を負いません**。

**本教材は利用者ご自身の責任においてご利用ください。**
