# グリッパー用近接覚センサ

## 使用機器
- Raspberry Pi zero
- VL618X x 3

## 配線
| Raspbery Pi | sensor1 | sensor2 | sensor3 |
| ----------- | ------- | ------- | ------- | 
| GPIO21(40番ピン) | VIN  |      |      | 
| GPIO20(38番ピン) |      | VIN  |      | 
| GPIO16(36番ピン) |      |      |  VIN | 
| SCL(5番ピン)     | SCL  | SCL  | SCL  | 
| SDA(3番ピン)     | SDA  | SDA  | SDA  | 
| GND(6番ピン)     | GND  | GND  | GND  | 

- GPIO21, 20, 16は各センサーへの電力共有および，個別にON/OFFするためのスイッチとして利用
- Strethへの取り付けは，[これ](mounter_stretch)を使う


## setup
- raspberry piをwifiに接続できるようにする
- ssh, i2cを有効化する
- 依存モジュールインストール：`pip install rospkg catkin_pkg`
- このリポジトリをクローン：`https://github.com/naka-lab/ros_proximity_sensor_pi.git`
- 実行するためのシェルスクリプトを作成
   ```
   cp ros_proximity_sensor_pi/start_sensor.sh ./　
   chmod +x start_sensor.sh
   nano start_sensor.sh  # シェル内のROS_MASTER_URIとROS_IPを自身の環境に合わせて変更する
   ```
- この時点で`./start_sensor.sh`で実行できることが確認できたらRaspberry Piをリードオンリー化する[[参考]](https://astherier.com/blog/2020/05/change-raspi-to-read-only/#])
  - リードオンリー化後は，Raspberry Piの電源を直接切れるようになります
  - ただしリードオンリー化すると，Rasberry Piへの変更はすべて保存されなため，設定を変えたいときはもとに戻す

## 実行方法
- 正常にセットアップできていれば，sshでRaspberry Piに接続し，シェルクリプト`./start_sensor.sh`を実行するとノードが立ち上がる
- 情報はFloat32MultiArray型のroximity_sensor_valueという名前でpublishされる
