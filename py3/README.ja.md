# RBCP Libaray/command for python3

さらに別のRBCPプログラム(python3用)。

ライブラリ: SitcpRbcp.py

コマンドラインツール: cmdrbcp.py3

## cmdrbcp.py3 セットアップ

```
% git clone https://github.com/h-sendai/SitcpRbcp.git
```

を実行後、PATH環境変数がとっているディレクトリから
cmdrbcp.py3へシンボリックリンクをはるのが簡単です。
たとえばPATH環境変数に``$HOME/bin``が入っているなら
(ログインシェルがbashなら入っています)次のようにします。

```
% cd $HOME/bin
% ln -s path/to/SitcpRbcp/py3/cmdrbcp.py3
% ls -l cmdrbcp.py3
```

### コマンドラインオプション

```
% cmdrbcp.py3 -h
usage: cmdrbcp.py3 [-h] [-d] [-q] [-t TIMEOUT] [-n BYTES_PER_LINE]
                   [-l FILENAME] [-i]
                   [ip_address] [port]

Yet another RBCP program using python3

positional arguments:
  ip_address            IP Address
  port                  Port Number

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           some debug printing
  -q, --quiet           do not print intro
  -t TIMEOUT, --timeout TIMEOUT
                        set timeout sec (default: 0.5 sec)
  -n BYTES_PER_LINE, --bytes-per-line BYTES_PER_LINE
                        print bytes per line in rd command (default: 8)
  -l FILENAME, --load FILENAME
                        non-interactive. Load this file and excute the
                        commands in that file
  -i, --interactive     After load and execute via -l option, switch to
                        interactive mode

Example:
% cmdrbcp.py3 -h
    display command usage, options and exit.
% cmdrbcp.py3
    interactive command.  Use 192.168.10.16 and port 4660.
% cmdrbcp.py3 192.168.10.10
    interactive command.  Use 192.168.10.10 and port 4660.
% cmdrbcp.py3 192.168.10.10 4559
    interactive command.  Use 192.168.10.10 and port 4559.
% cmdrbcp.py3 -l cmd.txt
    non-interactive command.  Read cmd.txt and execute it,
    then exit.
% cmdrbcp.py3 -l cmd.txt -i
    Read cmd.txt and execute it, then switch to interactive mode.

Use help or help <topic> command to get commands under interactive mode.
```

### インタラクティブモードでのコマンド

```
% ./cmdrbcp.py3
Trying IP address: 192.168.10.16, Port: 4660
Type help to get available commands.  Type q to quit
help <command> displays each <command> help.  Example: help rd
command/filename completion by TAB key, history and command line editing available
Good luck!
RBCP> help

Documented commands (type help <topic>):
========================================
EOF  help  load  q  quit  rd  setip  setport  showipport  wr  wrb  wrs  wrw

RBCP> help wrb
Usage: wrb address data
       write one byte data to address
RBCP> help rd
Read a register and print its value in HEX.
Usage: rd address [length]
       default length is 1 bytes
RBCP> rd 0xffffff10 1
0x 01
RBCP> wrb 0xffffff10 0
RBCP> rd 0xffffff10 1
0x 00
RBCP> q
%
```

### コマンド行編集、コマンド名・ファイル名の補完およびヒストリーの保存

インタラクティブモードの場合、bashのようにコマンドライン編集、
ctrl-pでの以前使ったコマンドの呼び出し、ctrl-sでのインクリメンタルサーチ
ができます。
タブキーでコマンド名およびloadコマンドで使うファイル名の補完が可能です。
インタラクティブモードで入力されたコマンドは``~/.cmdrbcp_history``に
保存されます。次回起動時にはこのファイルが読まれてヒストリーに入ります。
