# 開発・メンテナンスメモ

> このファイルは **このリポジトリを保守する人向け** のメモです。
> チュートリアル本編とは無関係なので、GitHub Pages のビルドからは除外されています。
> 学生・読者は読む必要はありません。

## 技術スタック

- **Jekyll**（GitHub Pages 標準ビルダ）
- **just-the-docs** テーマ（remote_theme で読み込み）
- 主要プラグイン: `jekyll-relative-links` / `jekyll-remote-theme` / `jekyll-seo-tag`

## GitHub Pages として公開する手順（初回セットアップ）

1. GitHub にリポジトリを作成して push
2. リポジトリの **Settings → Pages** を開く
3. **Source** を `Deploy from a branch` に設定
4. **Branch** を `main` の `/ (root)` に設定して保存
5. 1〜2 分でサイトが公開される: `https://<ユーザー名>.github.io/<リポジトリ名>/`

CLI（`gh` 経由）で一発設定:

```bash
gh api -X POST repos/<owner>/<repo>/pages \
  -f "source[branch]=main" -f "source[path]=/"
```

## ローカルプレビュー

```bash
bundle install
bundle exec jekyll serve
# → http://localhost:4000 で確認
```

## ハマりどころ

### サイトルートが 404 になる

`README.md` は Jekyll のデフォルトでは `README.html` として出力されるため、
そのままだとサイトルート (`/`) に `index.html` がなく 404 になる。

対処: `README.md` の front matter に `permalink: /` を追加する（このリポジトリでは設定済み）。

### ビルド状態の確認

```bash
gh run list --repo <owner>/<repo> --limit 5
gh api repos/<owner>/<repo>/pages/builds/latest --jq '{status, error}'
```

### 章を追加するとき

1. `tutorial/0X-xxx.md` を作成し、front matter に `parent: チュートリアル` と `nav_order: N` を入れる
2. `tutorial/index.md` の TOC テーブルに 1 行追加
3. `README.md` の TOC テーブルにも 1 行追加
4. 前後章の Prev/Next ナビリンクを更新
5. 対応する `examples/0X_xxx/` フォルダに `.ino` と `platformio.ini` を作成

## ファイル構成のルール

- `README.md` … サイトのトップページ（`permalink: /`、`layout: home`）
- `tutorial/index.md` … 章一覧（親ページ、`has_children: true`）
- `tutorial/*.md` … 各章（`parent: チュートリアル`、`nav_order: N`）
- `examples/0X_xxx/` … 章ごとの Arduino スケッチ + `platformio.ini`
  - 1 フォルダに 1 つの `.ino`（複数置くと両 IDE でビルドエラー）
- `assets/images/` … 図版の PNG（自動生成、コミット対象）
- `figures/` … 図を生成する Python スクリプト（uv 管理、Jekyll 除外）
- `DEVELOPMENT.md` … このファイル（Jekyll 除外）
- `Gemfile` … ローカルプレビュー用（Jekyll 除外）

## 図の更新方法

`figures/` で uv プロジェクト管理。matplotlib + numpy。

```bash
cd figures

# 依存関係（既に追加済み）
uv add matplotlib numpy

# 図を再生成
uv run 01_easing_curves.py        # → assets/images/ch3_easing.png
uv run 02_leg_ik.py               # → assets/images/ch4_leg_ik.png
uv run 03_foot_trajectory.py      # → assets/images/ch5_foot_trajectory.png
uv run 04_gait_timing.py          # → assets/images/ch5_gait_timing.png

# 全部一括
for f in 0*.py; do uv run "$f"; done
```

スタイルは `figures/_style.py` で一元管理（背景色・配色・フォント）。
just-the-docs ダークモードに合わせた配色になっている。
