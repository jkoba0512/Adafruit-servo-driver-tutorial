---
title: チュートリアル
nav_order: 2
has_children: true
---

# チュートリアル

各章を順に進めてください。
左サイドバーの章リンクから個別に飛ぶこともできます。

> ⚠ **実習を始める前に必ず [免責事項](../README.md#免責事項) をご一読ください。**
> 電源・配線・機械動作にかかる安全は利用者ご自身の責任でご確認ください。

| 章 | タイトル | やること |
|----|---------|---------|
| Ch 0 | [PCA9685 とは](00-pca9685-overview.md) | サーボドライバの仕組みと基本仕様 |
| Ch 1 | [1個のサーボを動かす](01-single-servo.md) | 配線・ライブラリ・最小コード |
| Ch 2 | [複数サーボを同時に動かす](02-multi-servo.md) | 「バラバラに着いてしまう」問題を体験 |
| Ch 3 | [同期制御 = 時間補間](03-synchronized-motion.md) | 全部を同じ時刻にゴールへ |
| Ch 4 | [1脚の運動学入門](04-leg-kinematics.md) | 足先座標 → サーボ角度（IK） |
| Ch 5 | [4脚歩行ゲイト](05-walking-gaits.md) | クロール・トロットの設計 |
| Ch 6 | [ゲイトジェネレータ実装](06-gait-generator.md) | 完成版で歩かせる |
| 付録 A | [電源設計](appendix-a-power.md) | 電源の選び方・容量計算 |
| 付録 B | [デバッグ術](appendix-b-debug.md) | 動かないときの切り分け |
| 付録 C | [トラブル集](appendix-c-troubleshooting.md) | よくある症状と対処 |
| 付録 D | [VS Code + PlatformIO で進める](appendix-d-platformio.md) | Arduino IDE 以外で進めたい人向け（外部資料リンク） |
