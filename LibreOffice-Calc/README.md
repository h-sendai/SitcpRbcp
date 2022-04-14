# LibreOffice Calc マクロ (Python)

LibreOffice Calc (Excelのような表計算ソフト)のpythonマクロを使って
SiTCP RBCPでレジスタの値をセットするプログラム。

SiTCP RBCP用プログラムはこのディレクトリにあるCalcファイルに埋め込んで
いるのでpython実行ファイル, LibreOffice Calc以外はセットアップは必要ない。
pythonは普通にインストールすると入っていると思うのでセットアップ方法は省略する。

## LibreOfficeのインストール

CentOS 7:
```
root# yum -y install libreoffice
```

CentOS Stream 8:
```
yum -y install libreoffice-calc
```

## LibreOffice Calcの起動

デスクトップ環境のメニューバーからLibreOffice Calcを起動することも
可能だが、pythonマクロ内からprint()関数でデバッグ風文字列を出力
しているのでターミナルエミュレータからCalcを起動する。

```
user% libreoffice --calc
```

起動後に
Tools -> Options -> LibreOffice -> Security -> [Macro Security ...] ボタン
でSecurity LevelをMediumにセットしてください。次回からマクロを含んだ
ファイルを開くとマクロを有効にするかどうかのダイアログがでるので有効に
するを選んでください。

## ファイル名を指定してCalcを起動

サンプルとして
アドレス0xffffff3c - 0xffffff3fに値をセットするファイルを
このディレクトリにおいてあるのでこれをコピーして使ってください。
CentOS 7ではsitcp-rbcp-python2.ods、CentOS Stream 8ではsitcp-rbcp-python3.ods
を使ってください。
LibreOffice CalcのpythonマクロはCentOS 7付属のものはpython2を、
CentOS Stream 8のものはpython3を使うようなのでこのようにわけてあります。

起動例:

```
user% cp somewhere/SitcpRbcp/LibreOffice-Calc/sitcp-rbcp-python2.ods .
user% libreoffice --calc sitcp-rbpc-python2.ods
```

(注)アドレス0xffffff3c - 0xffffff3fはSiTCPライブラリで「ユーザー領域」
として読み書きが自由にできるレジスタとなっています。
「SiTCP説明書」https://www.sitcp.net/doc/SiTCP.pdf 29ページ
を参照。(注おわり)

## 使い方

ボタンをおせば192.168.10.16にむけてSiTCP RBCP UDPパケットが飛びます。

Calcを起動したターミナルエミュレータには次のようにでます:

```
2022-04-13 15:35:58.324588 start
192.168.10.16 1 user_area_0 0xffffff3c 1 10
192.168.10.16 2 user_area_1 0xffffff3d 1 7
192.168.10.16 3 user_area_2 0xffffff3e 1 48
192.168.10.16 4 user_area_3 0xffffff3f 1 64
2022-04-13 15:35:58.329004 done
```

(注)上にも書きましたが、アドレス0xffffff3c - 0xffffff3fはSiTCPライブラリで「ユーザー領域」
として読み書きが自由にできるレジスタとなっています。
「SiTCP説明書」https://www.sitcp.net/doc/SiTCP.pdf 29ページ
を参照。(注おわり)

各コラムの意味は次のように定義されています。

- Column A: レジスタ名
- Column B: レジスタアドレス
- Column C: レジスタ長（単位: バイト）
- Column D: 書き込む値
- Column E以降: 無視するので自由にコメントなどを書いてください

数値は0xが先頭にあれば16進数、0bがあれば2進数（たとえば0b11110000 == 0xf0）、それ以外は
10進数として解釈します。

- Column Aが空白ならその行は無視します。
- Column Aの名前が``#``で始まっていればその行は無視します（コメント）。
- デフォルトでは192.168.10.16にSiTCP RBCP UDPを送信しますが、Column Aが``ip_address``という文字列なら
その次の行から送信先IPアドレスはColumn Bで指定したIPアドレスに変更になります。

### 例

| Column A    | Column B   | Column C | Column D | Column E |
--------------|------------|----------|----------|----------|
| user_area_0 | 0xffffff3c |        1 | 0x10     | 192.168.10.16 0xffffff3c に1バイト 0x10を書く |
| user_area_1 | 0xffffff3d |        1 | 0x20     | 192.168.10.16 0xffffff3d に1バイト 0x20を書く |
| ip_address  | 192.168.10.17 |        |          |
| user_area_0 | 0xffffff3c |1         | 0b11110000 | 192.168.10.17 0xffffff3c に1バイト 0xf0を書く |
| user_area_1 | 0xffffff3d |        1 | 100    | 192.168.10.17 0xffffff3d に1バイト 100(10進数)を書く |

## 保存

ファイルを保存するにはふつうにメニューバーから保存してください。

## 値の変更

値を変更したらエンターキーを押して値が変更されたことをCalcに通知してください。
編集だけしてエンターキーをおさないで``set registers``ボタンを押すと編集前の
値が送信されることがあります。

## マクロファイルのとりだし

マクロファイルをみたい場合はunzipコマンドで取り出せます。
なかにあるファイルはこのディレクトリにある
python_set_reg.py
と
[../py2/SitcpRbcp.py](../py2/SitcpRbcp.py)あるいは
[../py3/SitcpRbcp.py](../py3/SitcpRbcp.py)です。

## LibreOffice Calcにpythonマクロを埋め込む方法

Calcファイルにpythonマクロを埋め込むには拡張機能
Alternative Script Organizer for Python (APSO)
https://extensions.libreoffice.org/en/extensions/show/apso-alternative-script-organizer-for-python
が必要になります。

(注)
なぜ
Alternative Script Organizer for PythonをAPSOと略称するのか不明です。（注おわり）

APSOをセットするにはCalcで

Tools -> Extensions Manager -> Get more extension online ... -> 
Firefox起動 -> pythonで検索 -> APSOがでるのでダウンロード ->
Extensions Managerで追加 -> Calcリスタートが必要とでるのでリスタート

でセットします。

マクロの編集に使用するエディタを指定したい場合は

Tools -> Extensions Manager -> APSOをクリック -> Optionsボタン

でEditor欄に記入します。

埋め込みマクロをみるには
Tools -> Macros -> Organaize python scripts
から行います（Organize python scrirptsはAPSOをセットアップ後に出現するメニューです）。
