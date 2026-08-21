# AI 迷路攻略ゲーム (Genetic Algorithm Maze Resolver)

遺伝的アルゴリズム（GA）を用いて、ドット状のコンピューターの個体たちが世代交代を繰り返しながら迷路の最短ルートを学習・攻略していくシミュレーションゲームです。

## 開発・配布
- **開発者**: 池﨑亮介 (with Gemini)
- **配布者**: taitai2661

---

## 起動方法

###  Windows ユーザー（簡単）
`Releases` から **`game.exe`** をダウンロードしてダブルクリックで起動できます。
※ Pythonのインストールは不要です。

###  Mac ユーザー（またはソースコードから実行したい方）
ターミナルを開き、以下のコマンドを実行して必要なライブラリをインストールした上で実行してください。

1. **HomebrewでPythonをインストール**（未導入の場合）
   ```bash
   /bin/bash -c "$(curl -fsSL [https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh](https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh))"
   brew install python

**依存ライブラリのインストールと実行**
pip3 install pygame-ce
python3 game.py

**遊び方 / 操作方法**
コンピューターの進化: 各世代の個体たちが壁を避けながら赤色のゴールを目指します。世代が進むほど効率的なルートを学習します。

[R] キー: 迷路を再生成して第1世代からやり直します。
