# Firework Observer

English: [README.md](README.md)

Firework Observer は、Pyxel で作られた花火鑑賞用の小さな作品です。
直方体の観察空間の中に、ワイヤーフレームの街並み、星、UFO、そして複数種類の花火が現れます。
スコアやクリア条件はなく、カメラを回しながら静かに花火を眺めることを目的にしています。

## スクリーンショット

公開用スクリーンショットはまだ選定中です。

## 必要環境

- Python 3.12 以降
- Pyxel 2.0 以降
- 開発時は `uv` の利用を推奨

依存関係は `pyproject.toml` を参照してください。

## 起動方法

通常の起動:

```bash
python3 main.py
```

Pyxel の実行形式:

```bash
pyxel run main.py
```

開発環境でプロファイルを明示する場合:

```bash
.venv/bin/python main.py --profile iphone16_balanced
```

明示的な runtime launcher:

```bash
.venv/bin/python scripts/run_runtime_app.py --profile iphone16_balanced
```

`main.py` が公開用の標準入口です。
`scripts/run_runtime_app.py` は開発用の明示的な runtime launcher です。
`tools/preview_firework_box.py` は手動確認用の preview harness であり、公開用の入口ではありません。

## 操作方法

| キー | 操作 |
| --- | --- |
| `SPACE` | 花火の種類を切り替え |
| `Z` | 花火を1発打ち上げ |
| `R` | ランダム花火モード |
| `H` | 花火の高さ変化 ON/OFF |
| `1` | 1発ずつの継続サルボ |
| `2`-`5` | 固定数サルボ |
| `0` | ランダム数サルボ |
| `V` | 自動打ち上げ ON/OFF |
| `X` | 自動回転 ON/OFF |
| `Q` | 自動回転速度切り替え |
| `T` | 箱内の星 ON/OFF |
| `U` | UFO ambient ON/OFF |
| `M` | 音 ON/OFF |
| `B` | 街並み表示 ON/OFF |
| `G` | 背景/街並み切り替え |
| `D` | デバッグ HUD ON/OFF |
| `A` / `S` | ズーム |
| 矢印キー | カメラ回転 |
| `C` | カメラリセット |

## 主な機能

- 直方体の 3D 観察空間
- ワイヤーフレームの街並み
- 中央大通り、タワー、観覧車、看板、窓
- 箱の内側に貼り付いた星
- まれに通過する無音の 3D ワイヤーフレーム UFO
- オルゴール風 BGM
- 低めで控えめな花火爆発音
- 複数種類の花火
  - Kiku
  - Sphere Bloom
  - Smile
  - Ring
  - Spiral
  - Willow
  - Long Willow
  - Peony
  - Multi-ring
  - Senrin
  - Halo
- 花火ごとの 3 種類の deterministic color palette
- Kiku / Sphere Bloom / Peony / Multi-ring の delayed mini-burst garnish
- random / salvo show modes

`Sphere Bloom` は、素直な球状花火として読めることを目的にした花火です。
`Long Willow` は、通常の Willow より長く枝垂れる柳花火です。
`Smile` は、目と口の弧で構成された顔型の花火です。

## 開発・検証コマンド

```bash
python3 scripts/check_public_safety.py
python3 -m compileall src tests scripts tools main.py
.venv/bin/python -m pytest
.venv/bin/python -m ruff check .
python3 scripts/check_all.py
uv run python scripts/capture_smoke.py
```

`scripts/check_all.py` には public safety check が含まれています。
`scripts/check_public_safety.py` は、tracked files にローカル絶対パス、ローカル PC 名、ユーザー名などが混入していないかを確認します。

## 公開前チェック

公開前には少なくとも以下を確認します。

- `python3 main.py` で起動できる
- `pyxel run main.py` で起動できる
- `python3 scripts/check_public_safety.py` が通る
- `.venv/bin/python -m pytest` が通る
- `.venv/bin/python -m ruff check .` が通る
- `uv run python scripts/capture_smoke.py` が通る
- README と docs にローカル絶対パスを含めない

公開用のパス表記は、`docs/...`、`src/...`、`scripts/...` のような repository-relative path を使います。

## 公開方式メモ

現時点では GitHub 公開を想定しています。
Pyxel Web、`.pyxapp`、itch.io などの配布形式は今後整理します。

`reports/` の smoke report や開発用ログを公開対象に含めるかは、リリース前に確認してください。

## ライセンス / ステータス

- ステータス: prototype
- ライセンス: 未定

公開前に、利用するライセンスを決めて `LICENSE` を追加してください。
