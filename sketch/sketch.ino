/*
 * 模型車両制御用プログラム
 *
 * https://github.com/mak1non/project
 * https://mak1non.github.io/project/mortar.html
 */

enum state { BACKWARD, FORWARD, STOP };

enum direction { LEFT, RIGHT };

// 出力
const int count = 5;
const int maxOut = 240;
const int minOut = -220;
int motorOut = 0;

// モータードライバー (TA7291P) のピン番号
// 左モーター
const int leftOut1 = 10;  // 入力1
const int leftOut2 = 9;   // 入力2

// 右モーター
const int rightOut1 = 6;  // 入力1
const int rightOut2 = 5;  // 入力2

// 走行状態
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
                carState = STOP;  // 停止 (S)
            } else if (buf[0] == 65) {
                carState = FORWARD;  // 前進 (A)
            } else if (buf[0] == 66) {
                carState = BACKWARD;  // 後退 (B)
            } else if (buf[0] == 76) {
                makeTurn(LEFT);  // 左折 (L)
            } else if (buf[0] == 82) {
                makeTurn(RIGHT);  // 右折 (R)
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
            analogWrite(leftOut1, motorOut);
            analogWrite(rightOut1, motorOut);
        } else if (motorOut < 0) {
            int out = motorOut * -1;
            analogWrite(leftOut2, out);
            analogWrite(rightOut2, out);
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

/*
 * 曲がる (TODO)
 *
 * dir: 曲がる方向
 */
void makeTurn(direction dir) {
    // 前進中のみ実行
    if (carState == FORWARD) {
        if (dir == LEFT) {
            analogWrite(leftOut1, 0);
            delay(500);
            analogWrite(leftOut1, motorOut);
        } else {
            analogWrite(rightOut1, 0);
            delay(500);
            analogWrite(rightOut1, motorOut);
        }
    }
}
