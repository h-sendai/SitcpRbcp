# SitcpRbcp GUI サンプル

python3でwxを使ったGUIのサンプル

## セットアップ

CentOS 7:
```
yum install epel-release; yum install python36-wxpython4
```

CentOS Stream 8:
```
yum install epel-release; yum install python3-wxpython4
```

## サンプルの動作

SiTCP文書
https://www.sitcp.net/doc/SiTCP.pdf
29ページのレジスタマップにある「ユーザー領域」に書き込むように
作ってあります。

|     name    |  address   | length |
|-------------|------------|---|
| user_area_0 | 0xffffff3c | 1 |
| user_area_1 | 0xffffff3d | 1 |
| user_area_2 | 0xffffff3e | 1 |
| user_area_3 | 0xffffff3f | 1 |

## メモ

だいたいのものは別プログラムでバッチで設定してしまい
いろいろ変えたいものだけ自分で定義できるようになるという流れ
に対応する方法を考える。

レジスター情報はファイル先頭に
名前、アドレス、長さ、起動時に表示する数値
の配列としている。
これらを書いた設定ファイルを読んで``register_info``に
``append()``するように変更することで使いたいレジスタを
プログラムファイルを変更することなしにGUIを使うことが
できるようになる。
