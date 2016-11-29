# プロトコル定義

## Network Layer

Physical Layer以下に対しての制御情報を設定する

### Header

|0|1|2|3|4|5|6|7|
|:-|:-|:-|:-|:-|:-|:-|:-|
|version|-|-|>|payload length|-|-|-|
|-|-|-|-|-|-|-|>|
|payload checksum|-|-|-|-|-|-|>|
|header checksum|-|-|-|-|-|-|>|

#### version
- プロトコルバージョンを定義(4bit)

#### データ長
- データ部の長さ
- 12 bit (最大 4kbyte)

#### checksum

##### payload
- ペイロードデータの8bit毎のデータの1の補数の和を求める

##### header
- header checksumは自身を0埋め、8bit毎にデータの1の補数の和を求める

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