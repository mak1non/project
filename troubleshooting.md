# トラブルシューティング

## opencv-python のインストールが終わらない

画像解析などを行うために、`OpenCV`と呼ばれるパッケージが必要になる。そのため、`pip3 install opencv-python`を実行して必要なモジュールをインストールするのだが、インストール中に内部で OpenCV 関連のソースコードをコンパイルしているので、それを Raspberry Pi 上で実行すると非常に時間が掛かる。

### 解決方法

Raspberry Pi OS のソフトウェアリポジトリにコンパイル済みの`opencv-python`が用意されているので、それを利用する。

```
# apt install python3-opencv
```
