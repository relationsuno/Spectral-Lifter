# Spectral Lifter (v1.0)

日本語の説明を下に書きました。

## English

Spectral Lifter is a neural audio processor designed to restore missing high-frequency content (above 12kHz–16kHz) and remove artificial "shimmer" artifacts (swishy/grainy noise) typically found in AI-generated audio, such as those from AI sound.

**Note**: Please use this tool at your own risk. No official support is provided.

### Architecture

- Web-based interface powered by `gradio`.
- Audio Digital Signal Processing (DSP) using PyTorch and Librosa.

### Usage: Running on Google Colaboratory (Recommended)

To leverage powerful TPU or GPU resources, it is recommended to upload the entire folder to Google Colab.

1. Upload the entire `Spectral Lifter` folder to your Google Drive (e.g., in the root "My Drive" directory).
2. Create a new Google Colab notebook and mount your Drive:
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. Navigate to the directory and install the required libraries:
   ```python
   %cd /content/drive/MyDrive/Spectral\ Lifter
   !pip install -r requirements.txt
   ```
4. Launch the Gradio app. Click the generated "Public URL" to access the interface:
   ```python
   !GRADIO_SHARE=True python app.py
   ```

### Usage: Running Locally

To run the tool on your local machine, ensure Python 3.9+ is installed, then execute the following:

```bash
# Install packages
pip install -r requirements.txt

# Launch the app
python app.py
```

Once started, open the link `http://127.0.0.1:7860` in your browser.

### Tips

If the audio sounds too quiet, try adjusting the LUFS value in `utils/audio_io.py` to -12.0.

- **LUFS**: Configured to -14.0 LUFS in `utils/audio_io.py`. Please adjust as needed.

- **True Peak**: Configured to -1.0 dBTP in `utils/audio_io.py`. Please adjust as needed.

- **Bit Depth**: Configured to 32-bit float in `utils/audio_io.py` (subtype='FLOAT'). To use 24-bit or 16-bit, change the subtype to 'PCM_24' or 'PCM_16', respectively.



### Audio Processing (Features)
1. **Target Analysis**: Detection of 12k-16kHz rolloff, analysis of shimmer components and harmonics
2. **Digital Denoising**: Removal of hiss and graininess using Spectral Gate (subtraction)
3. **Spectral Upscaling**: Reconstruction of frequencies above 16kHz using heuristics/neural foldover, transient acquisition
4. **Dynamics Control**: Multi-band suppression of sibilance (5k-8kHz), shimmer (10k-14kHz), and artifacts above 18kHz
5. **Final Mastering**: Loudness normalization to -14 LUFS, True Peak limiting control


### Disclaimer

- **Self-Responsibility**: This tool is provided "as is." The author is not responsible for any damages (data loss, audio degradation, system issues, etc.) arising from its use.
- **Quality Guarantee**: While designed for AI audio characteristics, results may vary depending on the source material and parameter settings.
- **Affiliation**: This is a personal research and development project. It is not affiliated with Suno AI, Google, or any other mentioned entities.
- **Intellectual Property**: The rights to the processed audio belong to the user, subject to the rights they hold over the original audio. The use of this tool does not alter intellectual property rights.


### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



## 日本語

AI等による人工的な音源に対して、高域（12k-16kHz以上）の欠落の復元と、人工的なシマーノイズ（シュワシュワ音）を除去するためのニューラル・オーディオ・プロセッサーです。

**Note**: 自己責任でご利用ください。サポートなどはありません。

### 構成
- WebベースのUI（`gradio`）
- PyTorch + Librosa をバックエンドとするオーディオDSP

### 使い方: Google Colaboratoryで実行する場合（推奨）
Google Colabにフォルダごとアップロードして実行することをお勧めします。

1. ご自身のGoogle Driveに `Spectral Lifter` フォルダ全体をアップロードします。今回はマイドライブの直下に「Spectral Lifter」というフォルダを作成し、その中にアップロードしました。
2. Google Colabのノートブックを新規作成し、MyDriveをマウントします。
   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```
3. ディレクトリを移動し、必要なライブラリをインストールします。
   ```python
   %cd /content/drive/MyDrive/Spectral\ Lifter
   !pip install -r requirements.txt
   ```
4. Gradioアプリを起動します。公開リンク（Public URL）が生成されるため、そちらをクリックしてUIにアクセスしてください。
   ```python
   !GRADIO_SHARE=True python app.py
   ```

### 使い方: ローカル環境で実行する場合
お手元のPC環境下で動作させる場合、Python 3.9+ がインストールされていることを確認の上、下記コマンドを実行してください。

```bash
# Install packages パッケージのインストール
pip install -r requirements.txt

#Launch the app アプリの起動
python app.py
```
起動後、ターミナルに表示される `http://127.0.0.1:7860` のリンクをブラウザで開いてご利用ください。


### 音源の処理（機能）
1. **Target Analysis**: 12k-16kHzのロールオフ検出、シマー成分と倍音の分析
2. **Digital Denoising**: Spectral Gate（減算）によるヒス・粒子感の除去
3. **Spectral Upscaling**: ヒューリスティック/Neuralフォールドオーバーを用いた16kHz以上の再構築、トランジェントの取得
4. **Dynamics Control**: 5k-8kHzのシビランス、10k-14kHzのシマー、18kHz以上のアーティファクトに対するマルチバンド抑制
5. **Final Mastering**: -14 LUFS へのラウドネスノーマライゼーション、True Peakリミッティング制御


### Tips

音量が小さいと感じる方は、テキストエディタを使って、utils/audio_io.py のLUFSを -12.0 に変更してみてください。

- **LUFS**: utils/audio_io.py に -14.0 LUFS と設定されています。必要に応じて変更してください。

- **True Peak**: utils/audio_io.py に -1.0 dBTP と設定されています。必要に応じて変更してください。

- **ビット数**: utils/audio_io.py にて 32 bit に設定してます。subtype='FLOAT' に設定しています。24ビットや16ビットへ変更したい方は、'PCM_24' や subtype='PCM_16'にしてください。


### ライセンス (License)
このプロジェクトは **MITライセンス** の下で公開されています。詳細は [LICENSE](LICENSE) ファイルをご覧ください。


### 免責事項 (Disclaimer)
- **自己責任の原則**: 本ツールは現状有姿で提供され、使用に伴ういかなる損害（データ損失、音質の劣化、システムトラブル等）についても作者は一切の責任を負いません。
- **出力品質の保証**: 本ツールはAI生成音源の特性に基づき設計されていますが、元の音源の状態やパラメーター設定により、期待される効果が得られない場合があります。
- **権利関係**: 本ツールは個人による研究・開発プロジェクトであり、Suno AI、Google、その他言及されている各企業・団体とは一切関係ありません。
- **知的財産権**: 処理後の音源の権利は、ユーザーが元の音源に対して保有している権利に準じます。本ツールの使用自体が権利関係を変更することはありません。


---


# 開発指示書：Project "Antigravity" - Spectral Lifter (v1.0)

## 1. プロジェクト概要
Suno AIによって生成された音源に含まれる、特有の「高域の欠落」および「AIシマー（シュワシュワ音）」を解決するためのニューラル・オーディオ・プロセッサーを構築する。物理的な音響特性に基づいた外科的な修復と再構築を自動化する。

## 2. ターゲット解析（ノイズ定義と物理特性）
* **遮断境界の検出:** 12kHz 〜 16kHz 付近に存在する急激なロールオフ（周波数カット）を特定する。
* **アーティファクトの隔離:** 境界線周辺で発生する非調波的なデジタル歪み（AIシマー、さえずり音）を、既存の音楽成分から分離する。
* **倍音構造の解析:** 300Hz 〜 800Hz 付近の中域および高域の倍音成分をスキャンし、予測生成の基礎データとする。

## 3. 主要処理パイプライン（Core Algorithm）

### 3.1. デジタル・デノイジング（Antigravity Filter）
* **適応型ノイズ低減:** 背景のヒスノイズおよび「砂嵐のような粒子感」を動的に除去するアルゴリズムを実装する。
* **マルチパス処理:** 低い減少量設定（3dB 〜 6dB 程度）で複数回処理を行うことで、音楽的ディテールを保護する。

### 3.2. スペクトル復元（Spectral Upscaling）
* **高域予測生成:** 遮断された 16kHz 以上の帯域に対し、既存の倍音成分から論理的な高域情報を再構築し、フルレンジ（20kHz 相当）へと拡張する。
* **トランジェント取得:** 圧縮で丸くなってしまったアタック音（ドラム等）の輪郭を再定義する。

### 3.3. ダイナミック・シビランス制御
* **マルチバンド・ディ・エッシング:** 下記の周波数設計に基づき、刺さるような高域を制御する。
    * **5kHz 〜 8kHz:** 歌声の核となるシビランス（歯擦音）の制御。
    * **10kHz 〜 14kHz:** Suno特有のシマー・ノイズ（金属的アーティファクト）の抑制。
    * **18kHz 以上:** デジタル・アーティファクトと偽りの「エア感」の除去。

## 4. 技術仕様と出力要件

| 項目 | 設定値 | 理由 |
| :--- | :--- | :--- |
| **Sampling Rate** | 48kHz | エイリアシングを防ぎ、広帯域を維持するため。 |
| **Bit Depth** | 24-bit または 32-bit float | 量子化ノイズを最小限に抑えるため。 |
| **Loudness** | -14 LUFS | ストリーミング配信の標準規格に準拠させるため。 |
| **True Peak** | -1.0 dBTP | デジタル変換時の歪みを防止するため。 |

## 5. 開発における重要事項
* **位相への配慮:** 外科的EQを適用する際は、定位の崩れを防ぐため、リニア位相モードまたは最小位相での緩やかな補正を選択可能にすること。
* **FFTサイズの動的調整:** 持続的なパッド音には大きなFFTサイズ、リズム楽器には時間解像度を優先した小さなFFTサイズを自動適用するロジックを検討すること。
* **リファレンス比較機能:** 高品質な商用録音データとリアルタイムで A/B 比較し、耳の慣れ（AI難聴）を防止するモニタリング機能を備えること。

