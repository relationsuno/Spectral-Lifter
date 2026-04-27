# Spectral Lifter (v1.2)

[日本語](#日本語) | [English](#english)

---

## 日本語

Spectral Lifter は、Suno AIなどの生成AIによって作られた音源特有の「高域（12kHz〜16kHz以上）の欠落」を復元し、「人工的なシマーノイズ（シュワシュワ音）」を除去するためのオーディオ・プロセッサーです。

**⚠️ Note**: 自己責任でご利用ください。公式のサポート等はありません。

**⚠️ Note**: ニューラルアップスケーリングはうまくいってなかったので、処理を削除しました。ご了承ください。

### ✨ 特徴 (Features)
1. **Target Analysis**: 12k-16kHzの急激なロールオフ（カット）と、シマー成分・倍音を自動解析。
2. **Digital Denoising**: Spectral Gate（減算）により、ヒスノイズや砂嵐のような粒子感を除去。
3. **Dynamics Control**: 刺さる高音（5k-8kHz）、シマーノイズ（10k-14kHz）、不要なアーティファクト（18kHz以上）をマルチバンドで抑制。
4. **Final Mastering**: ストリーミング標準のラウドネス（-14 LUFS）およびTrue Peak（-1.0 dBTP）へ自動調整。

### 🚀 使い方

#### パターンA: Google Colaboratoryで実行する場合（推奨）
1. Google Driveの直下（MyDrive）に `Spectral Lifter` フォルダごとアップロードします。
2. Google Colabで新規ノートブックを作成し、以下のコードを順番に実行します。
   ```python
   # 1. Google Driveのマウント
   from google.colab import drive
   drive.mount('/content/drive')
   ```
   ```python
   # 2. ディレクトリ移動とパッケージのインストール
   %cd /content/drive/MyDrive/Spectral\ Lifter
   !pip install -r requirements.txt
   ```
   ```python
   # 3. アプリの起動（表示される Public URL にアクセスしてください）
   !GRADIO_SHARE=True python app.py
   ```

#### パターンB: ローカル環境で実行する場合
お使いのPCで実行する場合は、Python 3.9以上が必要です。
```bash
# パッケージのインストール
pip install -r requirements.txt

# アプリの起動
python app.py
```
起動後、ターミナルに表示される `http://127.0.0.1:7860` にブラウザでアクセスしてください。

### 💡 Tips (設定のカスタマイズ)
設定を変更したい場合は、テキストエディタで `utils/audio_io.py` を編集してください。
- **音量 (LUFS)**: デフォルトは `-14.0 LUFS` です。音が小さいと感じる場合は `-12.0` などに変更してください。
- **True Peak**: デフォルトは `-1.0 dBTP` です。
- **ビット深度**: デフォルトは `32-bit float` (`subtype='FLOAT'`) です。16bitや24bitにしたい場合は `'PCM_16'` や `'PCM_24'` に変更してください。

### 🔄 更新履歴
- **2026/4/27**: `HighFrequencyGenerator`を実装し、Neural Upscaling機能（失われた高域のニューラル予測）が動作するようになりました。

---

## English

Spectral Lifter is a audio processor designed to restore missing high-frequency content (above 12kHz–16kHz) and remove artificial "shimmer" artifacts (swishy/grainy noise) typically found in AI-generated audio.

**⚠️ Note**: Please use this tool at your own risk. No official support is provided.

### ✨ Features
1. **Target Analysis**: Detects 12k-16kHz rolloff and analyzes shimmer components and harmonics.
2. **Digital Denoising**: Removes hiss and graininess using Spectral Gate (subtraction).
3. **Dynamics Control**: Multi-band suppression of sibilance (5k-8kHz), shimmer (10k-14kHz), and artifacts above 18kHz.
4. **Final Mastering**: Automatic loudness normalization to -14 LUFS and True Peak limiting.

### 🚀 Usage

#### Option A: Google Colaboratory (Recommended)
1. Upload the entire `Spectral Lifter` folder to your Google Drive.
2. Create a Colab notebook and run the following in separate cells:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
   ```python
   %cd /content/drive/MyDrive/Spectral\ Lifter
   !pip install -r requirements.txt
   ```
   ```python
   !GRADIO_SHARE=True python app.py
   ```
3. Click the generated "Public URL" to access the web UI.

#### Option B: Local Environment
Requires Python 3.9+.
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:7860` in your browser.

### 💡 Tips
Adjust settings in `utils/audio_io.py` if needed:
- **LUFS**: Defaults to `-14.0 LUFS`. Change to `-12.0` if it sounds too quiet.
- **True Peak**: Defaults to `-1.0 dBTP`.
- **Bit Depth**: Defaults to 32-bit float (`subtype='FLOAT'`). Change to `'PCM_24'` or `'PCM_16'` as needed.

---

### License & Disclaimer
- **License**: MIT License. See [LICENSE](LICENSE) for details.
- **Disclaimer**: Provided "as is". The author is not responsible for any damages. Results may vary depending on the source material. Not affiliated with Suno AI, Google, or any other entities.

---

## 開発指示書 (Development Directives)

> プロジェクト構築時の仕様メモです。開発者向け。

### 1. プロジェクト概要
Suno AI等で生成された音源特有の「高域の欠落」および「AIシマー（シュワシュワ音）」を解決するためのニューラル・オーディオ・プロセッサー。物理的な音響特性に基づいた外科的な修復と再構築を自動化する。

### 2. ターゲット解析（ノイズ定義と物理特性）
* **遮断境界の検出:** 12kHz 〜 16kHz 付近に存在する急激なロールオフ（周波数カット）を特定。
* **アーティファクトの隔離:** 境界線周辺で発生する非調波的なデジタル歪み（AIシマー、さえずり音）を分離。
* **倍音構造の解析:** 300Hz 〜 800Hz 付近の中域および高域の倍音成分をスキャンし、予測生成の基礎データとする。

### 3. 主要処理パイプライン（Core Algorithm）

#### 3.1. デジタル・デノイジング（Antigravity Filter）
* **適応型ノイズ低減:** 背景のヒスノイズおよび「砂嵐のような粒子感」を動的に除去。
* **マルチパス処理:** 低い減少量設定（3dB 〜 6dB 程度）で複数回処理を行い、音楽的ディテールを保護。

#### 3.2. スペクトル復元（Spectral Upscaling）
* **高域予測生成:** 遮断された 16kHz 以上の帯域に対し、ニューラルモデルにより既存の倍音成分から高域情報を再構築。フルレンジ（20kHz 相当）へ拡張。
* **トランジェント取得:** 圧縮で丸くなったアタック音（ドラム等）の輪郭を再定義。

#### 3.3. ダイナミック・シビランス制御
* **マルチバンド・ディ・エッシング:**
    * **5kHz 〜 8kHz:** 歌声の核となるシビランス（歯擦音）の制御。
    * **10kHz 〜 14kHz:** Suno特有のシマー・ノイズ（金属的アーティファクト）の抑制。
    * **18kHz 以上:** デジタル・アーティファクトと偽りの「エア感」の除去。

### 4. 技術仕様と出力要件
| 項目 | 設定値 | 理由 |
| :--- | :--- | :--- |
| **Sampling Rate** | 48kHz | エイリアシングを防ぎ、広帯域を維持 |
| **Bit Depth** | 32-bit float | 量子化ノイズを最小限に抑える |
| **Loudness** | -14 LUFS | ストリーミング標準規格に準拠 |
| **True Peak** | -1.0 dBTP | デジタル変換時の歪みを防止 |
