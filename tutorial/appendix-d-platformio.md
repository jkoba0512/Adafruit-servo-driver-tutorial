---
title: "付録 D: VS Code + PlatformIO 環境"
parent: チュートリアル
nav_order: 10
---

# 付録 D: VS Code + PlatformIO 環境

Arduino IDE の代わりに **Visual Studio Code + PlatformIO** で
このチュートリアルを進める方向けのセットアップ手順です。

## なぜ PlatformIO？

| 項目 | Arduino IDE | PlatformIO (VS Code) |
|------|------------|----------------------|
| インストール | 簡単 | やや手順あり |
| コード補完 | △ 弱い | ◎ 強力（IntelliSense） |
| ライブラリ管理 | GUI からポチポチ | `platformio.ini` で版数固定 |
| ビルド速度 | 遅め | 速い（並列・キャッシュ） |
| Git との相性 | △（プロジェクト単位がない） | ◎ プロジェクト構成が明確 |
| デバッグ機能 | ほぼ無し | ステップ実行・ブレークポイント |

**慣れた人には PlatformIO の方が圧倒的に快適**です。
ただし最初の壁が少し高いので、無理に乗り換える必要はありません。

## インストール

### 1. VS Code をインストール

公式サイト <https://code.visualstudio.com/> から入手してインストール。

### 2. PlatformIO IDE 拡張機能をインストール

1. VS Code の左サイドバー **拡張機能（Extensions）** をクリック
2. 検索欄に `platformio` と入力
3. **PlatformIO IDE**（提供元: PlatformIO）を [Install]
4. インストール後、**コアのダウンロード**が自動で始まる（初回 5〜10 分）
5. 完了するとサイドバーに 🐝 のような **PlatformIO アイコン**が出現

> ⚠ ネット接続必須・Python が必要（拡張機能側で自動インストールされます）

## チュートリアルの例を開く

このリポジトリには各章ごとに **独立した PlatformIO プロジェクト**が用意されています。

```
examples/
├── 01_single_servo/
│   ├── 01_single_servo.ino
│   └── platformio.ini       ← これがあるフォルダがプロジェクトの単位
├── 01b_calibration/
│   ├── 01b_calibration.ino
│   └── platformio.ini
├── 02_multi_servo/
│   ├── 02_multi_servo.ino
│   └── platformio.ini
└── ...
```

### 開き方

1. VS Code で **「フォルダーを開く」**
2. 例: `examples/01_single_servo/` を選んで開く
3. PlatformIO が `platformio.ini` を検出し、自動的にプロジェクトとして認識
4. 初回はライブラリ（Adafruit_PWMServoDriver）が自動ダウンロードされる

> 💡 リポジトリのルート（`Adafruit-servo-driver-tutorial/` 全体）を開くと、
> PlatformIO はプロジェクトを認識しません。
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

### 各項目の意味

| キー | 意味 |
|------|------|
| `[platformio] src_dir = .` | このフォルダ自身を「ソースフォルダ」にする（デフォルトは `src/`） |
| `[env:uno]` | `uno` という名前の環境定義 |
| `platform = atmelavr` | Atmel AVR 系 MCU 用ツールチェイン |
| `board = uno` | ボード = Arduino Uno |
| `framework = arduino` | Arduino フレームワークを使う（`Wire.h` 等が使える） |
| `monitor_speed = 9600` | シリアルモニタのボーレート |
| `lib_deps = ...` | 依存ライブラリ。指定するだけで自動ダウンロード |

## ビルド・書き込み・モニタ

### GUI から

PlatformIO サイドバー（または下部ステータスバー）の各アイコン:

| アイコン | 機能 | CLI 相当 |
|---------|------|---------|
| ✓ Build | ビルド（コンパイル） | `pio run` |
| → Upload | ボードへ書き込み | `pio run -t upload` |
| 🔌 Monitor | シリアルモニタを開く | `pio device monitor` |
| 🗑 Clean | ビルド成果物を削除 | `pio run -t clean` |

### CLI から

ターミナルを開いて、プロジェクトフォルダに移動:

```bash
cd examples/01_single_servo

pio run                # ビルド
pio run -t upload      # 書き込み
pio device monitor     # シリアルモニタ
```

`Ctrl+C` でシリアルモニタを終了。

## 章を切り替えるには

1. VS Code で **「フォルダーを閉じる」** → 別の `examples/0X_xxx/` を開く
2. または **マルチルートワークスペース**を使う:
   - **File → Add Folder to Workspace…** で複数の例フォルダを追加
   - 各章のプロジェクトをサイドバーから切り替え可能

## .ino と main.cpp の違い

PlatformIO は `.ino` ファイルを直接サポートしますが、**.cpp に書き換える派**もいます。

| | .ino | .cpp |
|---|------|------|
| Arduino IDE 互換 | ◎ | × |
| 関数の前方宣言 | 自動挿入 | 自分で書く必要あり |
| 補完の精度 | △ | ◎ |
| Lint との相性 | △ | ◎ |

このチュートリアルは **Arduino IDE と PlatformIO の両方で動くこと**を優先し、
すべて `.ino` のまま提供しています。
PlatformIO に慣れて来たら `.ino` を `src/main.cpp` に変えてもOKです。

## トラブルシューティング

### ライブラリが見つからない

```
Library Manager: Installing adafruit/Adafruit PWM Servo Driver Library
Error: Could not find the package
```

- ネット接続を確認
- `platformio.ini` の `lib_deps` のスペルを確認
- PlatformIO サイドバーの **Libraries → Search** から手動インストールも可

### `pio` コマンドが見つからない

```
zsh: command not found: pio
```

- VS Code の PlatformIO サイドバーから **Quick Access → Miscellaneous → New Terminal**
  を開く（パスが通った状態で起動される）
- または `~/.platformio/penv/bin` を PATH に追加

### Upload エラー（ポート権限）

macOS / Linux:
```
sudo usermod -a -G dialout $USER       # Linux
# その後ログアウト・ログインし直す
```

macOS で USB シリアルが見えないときは、Arduino IDE 用の CH340 / FTDI ドライバが必要な場合あり。

### ビルドが遅い

初回ビルドは **コアフレームワークのコンパイル**が走るため数分かかることがあります。
2回目以降はキャッシュが効いて速くなります。

## やってみよう（演習）

1. VS Code に PlatformIO IDE をインストールせよ
2. `examples/01_single_servo/` を開いてビルド・書き込みを成功させよ
3. シリアルモニタで `Single servo test start` の表示を確認せよ
4. `examples/01b_calibration/` も同様に動かしてキャリブレーションを実施せよ
5. （発展）`platformio.ini` の `monitor_speed` を `115200` に変えて、
   スケッチの `Serial.begin(9600)` も合わせて変更し、動作することを確認せよ

## まとめ

- **VS Code + PlatformIO** は Arduino IDE の代替として強力
- 各 `examples/0X_xxx/` フォルダが独立した PlatformIO プロジェクト
- `platformio.ini` で **ボード・依存ライブラリを宣言**するだけで動く
- `.ino` のままでビルドできるので、**Arduino IDE と相互運用**が可能

---

[◀ 付録 C へ](appendix-c-troubleshooting.md) | [🏠 README に戻る](../README.md)
