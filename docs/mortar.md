# モータードライバーの挙動

使用予定: TA7291P

| IN1     | IN2     | 動作     |
| ------- | ------- | -------- |
| LOW(0)  | LOW(0)  | ストップ |
| HIGH(1) | LOW(0)  | 回転     |
| LOW(0)  | HIGH(1) | 逆回転   |
| HIGH(1) | HIGH(1) | ブレーキ |

- 出典: [モータードライバー(TA7291P)の使い方 [Arduino]](https://www.petitmonte.com/robot/motor_driver_ta7291p.html)