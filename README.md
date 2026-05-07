---
title: ホーム
layout: home
nav_order: 1
---

# Adafruit PCA9685 で4脚ロボットを歩かせるチュートリアル

Arduino Uno と Adafruit 16-Channel PWM/Servo Driver（PCA9685）を使って、
**自作4脚ロボットの RC サーボを同期制御**できるようになるための実習教材です。

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

## サンプルコード

`examples/` 以下に章ごとの `.ino` スケッチを置いています。
そのまま Arduino IDE で開いてビルド・書き込みできます。

```
examples/
├── 01_single_servo/   ... Ch 1 用
├── 02_multi_servo/    ... Ch 2 用
├── 03_sync_motion/    ... Ch 3 用
├── 04_leg_ik/         ... Ch 4 用
└── 05_walk_trot/      ... Ch 5・6 用（最終版）
```

## 必要なハードウェア

- Arduino Uno（R3 以降）
- Adafruit PCA9685 16-Channel Servo Driver
- RC サーボ（SG90 / MG90S / MG996R など）× 8〜12 個
- **サーボ用電源**（5V 3〜5A 程度のスイッチング電源、または 4×単3 電池ボックス）
- ジャンパワイヤ、ブレッドボード、必要に応じてはんだごて

> ⚠ サーボの電源は **必ず Arduino の 5V とは別系統**で用意してください。
> 詳細は [付録 A: 電源設計](tutorial/appendix-a-power.md) を参照。

## 必要なソフトウェア

- Arduino IDE（1.8 系または 2.x 系）
- ライブラリ: **Adafruit PWM Servo Driver Library**
  - Arduino IDE のライブラリマネージャで `adafruit pwm` を検索してインストール

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

## ライセンス・利用について

本教材は PBL 講義での利用を想定して作成しています。
学生・教員の方は自由に複製・改変してご利用ください。
