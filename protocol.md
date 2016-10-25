# プロトコル定義

## Network Layer

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

#### Network Byte Order

big endian

## Transport Layer

### Header

#### Content-type

text/plain;charset=ascii