# 透過電子顕微鏡データ標準テンプレート

## 概要
透過電子顕微鏡データを登録したい方に適したテンプレートです。２つの入力モードがあり、１つはGatan社 Digital Micrographのdm3フォーマットから計測手法を自動的に判別して、適切な可視化を行うTEM_DM3モードで、対応する計測手法は、TEM、STEM、TED、EELSです。もう１つは、dm3やTiffやpng、bmpなどの画像ファイルを入力し、必要に応じて可視化・可読化を行うEMモードです。なお、すべての入力ファイルの解析にHyperSpyを用います。

* DT0008: TEM_DM3モード
* DT0010: EMモード

### 構造化処理
TEM_DM3モードではTEMの専門家によって監修されたメタ情報を上記ファイルから自動的にRDEが抽出します。画像データはtiff化、png化、またコントラスト調整後png化します。EMモードでは上記ファイルから抽出したメタデータすべてをcsvとして登録します。なお、複数入力には対応していません。

## 基本情報

### コンテナ情報（構造化処理）

- 【コンテナ名】nims_electron_microscope_standard

### データセットテンプレート情報
- DT0008:
  - 【データセットテンプレートID】NIMS_DT0008_ELECTRON_MICROSCOPE_STANDARD_TEM_DM3_v1.0
  - 【データセットテンプレート名日本語】電子顕微鏡データ標準テンプレート (TEM_DM3)
  - 【データセットテンプレート名英語】NIMS Erectron Microscope Standard dataset-template (TEM_DM3)
  - 【データセットテンプレートの説明】電子顕微鏡データを登録したい方に適したテンプレートです。Gatan社 Digital Micrographのdm3フォーマットから計測手法（TEM、STEM、TED、EELS）を自動的に判別して、適切な可視化・可読化を行います。
  - 【バージョン】：1.0
  - 【データセット種別】：加工・計測レシピ型
  - 【データ構造化】：あり (システム上「あり」を選択)
  - 【取り扱い事業】NIMS研究および共同研究プロジェクト (PROGRAM)
  - 【装置名】(なし)
- DT0010:
  - 【データセットテンプレートID】NIMS_DT0010_ELECTRON_MICROSCOPE_STANDARD_v1.0
  - 【データセットテンプレート名日本語】電子顕微鏡データ標準テンプレート
  - 【データセットテンプレート名英語】NIMS Erectron Microscope Standard dataset-template
  - 【データセットテンプレートの説明】Gatan社 Digital Micrographのdm3ファイルや、tiff、png、bmpなどの画像ファイルを入力し、必要に応じて可視化・可読化を行います。
  - 【バージョン】：1.0
  - 【データセット種別】：加工・計測レシピ型
  - 【データ構造化】：あり (システム上「あり」を選択)
  - 【取り扱い事業】NIMS研究および共同研究プロジェクト (PROGRAM)
  - 【装置名】(なし)

### データ登録方法

- DT0008:
  - 送り状画面をひらいて入力ファイルに関する情報を入力する
  - 「登録ファイル」欄に登録したいファイルをドラッグアンドドロップする
    - 登録できるファイルのフォーマットは、*.dm3で、１ファイルずつ登録します。
  - 「登録開始」ボタンを押して（確認画面経由で）登録を開始する
- DT0010:
  - 送り状画面をひらいて入力ファイルに関する情報を入力する
  - 「登録ファイル」欄に登録したいファイルをドラッグアンドドロップする
    - 登録できるファイルのフォーマットは以下のいずれかで、１ファイルずつ登録します。
      - Gatan社 Digital Micrographが出力するdm3形式のファイル: .dm3
      - Tiff形式のファイル: .tif、.tiff
      - 画像ファイル: .bmp、.png、.jpg、.gif
  - 「登録開始」ボタンを押して（確認画面経由で）登録を開始する

## 構成

### レポジトリ構成
```
em_standard_dataset_template
├── LICENSE
├── README.md
├── container
│    ├── Dockerfile
│    ├── Dockerfile_nims (NIMSイントラ用)
│    ├── data (入出力(下記参照))
│    ├── main.py
│    ├── modules (ソースコード)
│    │    ├── datasets_process.py (構造化処理の大元)
│    │    ├── interfaces.py
│    │    ├── meta_handler.py (メタデータ解析(共通部))
│    │    ├── models.py
│    │    ├── modules_em (EMモード構造化処理)
│    │    │    ├── DigitalMicrograph (DigitalMicrographフォーマット用)
│    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    ├── ImageFormats (画像フォーマット用)
│    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    ├── Tiff (Tiffフォーマット用)
│    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    ├── factory.py (使用クラス取得)
│    │    │    ├── meta_handler.py (メタデータ解析)
│    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化(EMモード共通部))
│    │    ├── modules_temdm3 (TEM_DM3モード構造化処理)
│    │    │    ├── factory.py (使用クラス取得)
│    │    │    ├── inputfile_handler.py (入力ファイル整合性チェック)
│    │    │    ├── invoice_handler.py (送り状上書き)
│    │    │    ├── meta_handler.py (メタデータ解析(TEM_DM3モード共通部))
│    │    │    ├── methods
│    │    │    │    ├── eels (EELS測定)
│    │    │    │    │    ├── meta_handler.py (メタデータ解析)
│    │    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    │    ├── stem (STEM測定)
│    │    │    │    │    ├── meta_handler.py (メタデータ解析)
│    │    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    │    ├── ted (TED測定)
│    │    │    │    │    ├── meta_handler.py (メタデータ解析)
│    │    │    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    │    └── tem (TEM測定)
│    │    │    │        ├── meta_handler.py (メタデータ解析)
│    │    │    │        └── spectral_analyzer.py (入力ファイル解析、可視化)
│    │    │    └── spectral_analyzer.py (入力ファイル解析、可視化(TEM_DM3モード共通部))
│    │    ├── spectral_analyzer.py (入力ファイル解析、可視化(共通部))
│    │    └── structured_handler.py (構造化データ解析)
│    ├── pip.conf
│    ├── pyproject.toml
│    ├── requirements-test.txt
│    ├── requirements.txt
│    └── tox.ini
├── docs (ドキュメント)
│    ├── manual (マニュアル)
│    └── requirement_analysis
│        ├── 要件定義_EM.xlsx (要件定義(EMモード用))
│        └── 要件定義_TEM_DM3.xlsx (要件定義(TEM_DM3モード用))
└── templates (テンプレート群)
    ├── template_Em (EMモード向け)
    │    ├── batch.yaml
    │    ├── catalog.schema.json (カタログ項目定義)
    │    ├── invoice.schema.json (送り状項目定義)
    │    ├── jobs.template.yaml
    │    ├── metadata-def.json (メタデータ定義)
    │    └── tasksupport
    │        ├── invoice.schema.json (送り状項目定義)
    │        ├── metadata-def.json (メタデータ定義)
    │        ├── metadata-def_DigitalMicrograph.json (メタデータ定義(DigitalMicrographフォーマット用))
    │        ├── metadata-def_Image.json (メタデータ定義(画像フォーマット用))
    │        ├── metadata-def_Tiff.json (メタデータ定義(Tiffフォーマット用))
    │        └── rdeconfig.yaml (設定ファイル)
    └── template_TemDm3
        ├── batch.yaml
        ├── catalog.schema.json (カタログ項目定義)
        ├── invoice.schema.json (送り状項目定義)
        ├── jobs.template.yaml
        ├── metadata-def.json (メタデータ定義)
        └── tasksupport
            ├── default_value_EELS.csv (送り状上書き値(EELS用))
            ├── default_value_STEM.csv (送り状上書き値(STEM用))
            ├── default_value_TED.csv (送り状上書き値(TED用))
            ├── default_value_TEM.csv (送り状上書き値(TEM用))
            ├── invoice.schema.json (送り状項目定義)
            ├── metadata-def.json (メタデータ定義)
            ├── metadata-def_EELS.json (メタデータ定義(EELS測定用))
            ├── metadata-def_STEM.json (メタデータ定義(STEM測定用))
            ├── metadata-def_TED.json (メタデータ定義(TED測定用))
            ├── metadata-def_TEM.json (メタデータ定義(TEM測定用))
            └── rdeconfig.yaml (設定ファイル)
```

### 動作環境

- Python: 3.12
- RDEToolKit: 1.1.0

### 動作環境ファイル入出力

- DT0008:
```
│   ├── container/data
│   │   ├── attachment
│   │   ├── inputdata
│   │   │   └── 登録ファイル欄にドラッグアンドドロップした任意のファイル
│   │   ├── invoice
│   │   │   └── invoice.json (送り状ファイル)
│   │   ├── main_image
│   │   │   └── コントラスト調整後のpng画像、またはスペクトラムプロット画像
│   │   ├── meta
│   │   │   └── metadata.json (主要パラメータメタ情報ファイル)
│   │   ├── nonshared_raw
│   │   │   └── inputdataからコピーした入力ファイル
│   │   ├── other_image
│   │   │   └── コントラスト調整前のpng画像
│   │   ├── structured
│   │   │   └── *_metadata.csv (メタデータ)
│   │   ├── tasksupport (テンプレート群)
│   │   │   ├── default_value_EELS.csv
│   │   │   ├── default_value_STEM.csv
│   │   │   ├── default_value_TED.csv
│   │   │   ├── default_value_TEM.csv
│   │   │   ├── invoice.schema.json
│   │   │   ├── metadata-def.json
│   │   │   ├── metadata-def_EELS.json
│   │   │   ├── metadata-def_STEM.json
│   │   │   ├── metadata-def_TED.json
│   │   │   ├── metadata-def_TEM.json
│   │   │   └── rdeconfig.yaml
│   │   └── thumbnail
│   │       └── (サムネイル用)コントラスト調整後のpng画像、またはスペクトラムプロット画像
```
- DT0010:
```
│   ├── container/data
│   │   ├── attachment
│   │   ├── inputdata
│   │   │   └── 登録ファイル欄にドラッグアンドドロップした任意のファイル
│   │   ├── invoice
│   │   │   └── invoice.json (送り状ファイル)
│   │   ├── main_image
│   │   │   ├── (DigitalMicrographフォーマット) コントラスト調整後のpng画像、またはスペクトラムプロット画像
│   │   │   ├── (Tiffフォーマット) コントラスト調整後のpng画像
│   │   │   └── (画像フォーマット) 入力ファイルをpng化した画像
│   │   ├── meta
│   │   │   └── metadata.json (主要パラメータメタ情報ファイル)
│   │   ├── nonshared_raw
│   │   │   └── inputdataからコピーした入力ファイル
│   │   ├── other_image
│   │   │   ├── (DigitalMicrographフォーマット) コントラスト調整前のpng画像
│   │   │   └── (Tiffフォーマット) コントラスト調整前のpng画像
│   │   ├── structured
│   │   │   ├──  (DigitalMicrographフォーマット) コントラスト調整前のtif画像
│   │   │   └── *_metadata.csv (メタデータ)
│   │   ├── tasksupport (テンプレート群)
│   │   │   ├── invoice.schema.json
│   │   │   ├── metadata-def.json
│   │   │   ├── metadata-def_DigitalMicrograph.json
│   │   │   ├── metadata-def_ImageFormats.json
│   │   │   ├── metadata-def_Tiff.json
│   │   │   └── rdeconfig.yaml
│   │   └── thumbnail
│   │       └── (サムネイル用) main_imageと同じもの
```

## データ閲覧
- データ一覧画面を開く。
- ギャラリー表示タブでは１データがタイル状に並べられている。データ名をクリックして詳細を閲覧する。
- ツリー表示タブではタクソノミーにしたがってデータを階層表示する。データ名をクリックして詳細を閲覧する。
