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
const int maxOut = 255;
const int minOut = -255;
int motorOut = 0;

// モータードライバー (TA7291P) のピン番号
// 左モーター
const int leftOut1 = 5;  // 入力1
const int leftOut2 = 6;  // 入力2

// 右モーター
const int rightOut1 = 9;   // 入力1
const int rightOut2 = 10;  // 入力2

// 走行状態
state carState = STOP;

void setup() {
    // シリアル通信の準備
    Serial.begin(115200);

    // 出力ピンの準備
    pinMode(leftOut1, OUTPUT);
    pinMode(leftOut2, OUTPUT);
    pinMode(rightOut1, OUTPUT);
    pinMode(rightOut2, OUTPUT);

    neutral();
}

void loop() {
    // 入力の読み取り
    if (Serial.available() > 0) {
        String input = Serial.readStringUntil('\n');

        if (input.substring(0, 1) == '\r') {
            input.remove(0, 1);
        }

        if (input.substring(0, 1) == "S") {
            carState = STOP;  // 停止
        } else if (input.substring(0, 1) == "A") {
            carState = FORWARD;  // 前進
        } else if (input.substring(0, 1) == "B") {
            carState = BACKWARD;  // 後退
        } else if (input.substring(0, 1) == "L") {
            makeTurn(LEFT);  // 左折
        } else if (input.substring(0, 1) == "R") {
            makeTurn(RIGHT);  // 右折
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
            delay(2000);
            analogWrite(leftOut1, motorOut);
        } else {
            analogWrite(rightOut1, 0);
            delay(2000);
            analogWrite(rightOut1, motorOut);
        }
    }
}
