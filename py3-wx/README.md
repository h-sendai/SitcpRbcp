# SitcpRbcp GUI サンプル

python3でwxを使ったGUIのサンプル

## セットアップ

CentOS 7:
```
yum install epel-release; yum install python36-wxpython4
```

CentOS Stream 8:
```
yum install epel; yum install python3-wxpython4
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
