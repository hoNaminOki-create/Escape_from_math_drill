# Escape from Math Drill

Pygame で作成された弾幕回避ゲームです。`pygbag` を使って WebAssembly 化し、ブラウザ上でもプレイできるように対応しています。

## 操作方法

- `↑` / `↓`: ステージ選択（タイトル画面）・上下移動（プレイ中）
- `←` / `→`: 左右移動（プレイ中）
- `Shift`: 低速移動（精密回避）
- `Space`: ゲーム開始 / タイトルに戻る

## ローカルでの実行方法

### デスクトップ版 (Pygame)

```bash
pip install pygame
python3 main.py
```

### Web版 (pygbag)

```bash
pip install pygbag
python3 -m pygbag .
```

ブラウザで `http://localhost:8000` を開くとプレイできます。
