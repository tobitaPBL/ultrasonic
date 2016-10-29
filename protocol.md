# プロトコル定義

## Network Layer

Physical Layer以下に対しての制御情報を設定する

### Header

#### version
- プロトコルバージョンを定義
- 4bit ?

#### データ長
- ヘッダ+データ部の長さ？
- データ部のみの長さ？
- 8 or 16 bit ?

#### フラグメント(パケット的な単位を作るなら必要)

##### ID

#####

### データ部

最小データ長は1byte

#### Network Byte Order

big endian

## Transport Layer

Network Layer以下に対しての制御情報を設定する.

### 構成

```
header_key=value
\n
body
\n
```

### Header

#### Content-type

text/plain;charset=ascii