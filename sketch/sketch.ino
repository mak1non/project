/*
 * 模型車両制御用プログラム
 *
 * https://github.com/mak1non/project
 * https://mak1non.github.io/project/mortar.html
 */

enum direction { CENTER, LEFT, RIGHT };

enum state { BACKWARD, FORWARD, STOP };

// 出力
const int count = 5;
const int maxOut = 240;
const int minOut = -220;
const int diff = 10;
int motorOut = 0;

// モータードライバー (TA7291P) のピン番号
// 左モーター
const int leftOut1 = 10;  // 入力1
const int leftOut2 = 9;   // 入力2

// 右モーター
const int rightOut1 = 6;  // 入力1
const int rightOut2 = 5;  // 入力2

// 走行状態
direction carDir = CENTER;
state carState = STOP;

// バッファ
byte buf[3];

void setup() {
    // タイマーの無効化
    TIMSK0 = 0;
    
    // シリアル通信の準備
    Serial.begin(115200);

    // 出力ピンの準備
    pinMode(leftOut1, OUTPUT);
    pinMode(leftOut2, OUTPUT);
    pinMode(rightOut1, OUTPUT);
    pinMode(rightOut2, OUTPUT);

    neutral();
    Serial.println("Ready.");
}

void loop() {
    while (true) {
        if (Serial.available() > 0) {
            Serial.readBytesUntil('\n', buf, 1);
            Serial.println(buf[0]);
    
            if (buf[0] == 83) {
                // 停止 (S)
                carState = STOP;
                carDir = CENTER;
            } else if (buf[0] == 65) {
                // 前進 (A)
                carState = FORWARD;
                carDir = CENTER;
            } else if (buf[0] == 66) {
                // 後退 (B)
                carState = BACKWARD;
                carDir = CENTER;
            } else if (buf[0] == 76) {
                // 左折 (L)
                carState = FORWARD;
                carDir = LEFT;
            } else if (buf[0] == 82) {
                // 右折 (R)
                carState = FORWARD;
                carDir = RIGHT;
            }
        }

        // 現在速度
        if (carState == STOP && motorOut > 0) {
            motorOut -= count;
        } else if (carState == STOP && motorOut < 0) {
            motorOut += count;
        } else if (carState == FORWARD && motorOut < maxOut) {
            motorOut += count;
        } else if (carState == BACKWARD && motorOut > minOut) {
            motorOut -= count;
        }

        // 速度の反映
        if (motorOut == 0) {
            neutral();
        } else if (motorOut > 0) {
            if (carDir == LEFT) {
                analogWrite(leftOut1, 0);
                analogWrite(rightOut1, motorOut + diff);
                delay(200);
            } else if (carDir == RIGHT) {
                analogWrite(leftOut1, motorOut);
                analogWrite(rightOut1, 0);
                delay(200);
            } else {
                analogWrite(leftOut1, motorOut);
                analogWrite(rightOut1, motorOut + diff);
            }
        } else if (motorOut < 0) {
            int out = motorOut * -1;
            analogWrite(leftOut2, out);
            analogWrite(rightOut2, out + diff);
        }
    }
}

/*
 * 初期化
 */
void neutral() {
    digitalWrite(leftOut1, LOW);
    digitalWrite(leftOut2, LOW);
    digitalWrite(rightOut1, LOW);
    digitalWrite(rightOut2, LOW);
    delay(1000);
}
