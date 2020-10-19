/*
 * 模型車両制御用プログラム
 *
 * https://github.com/mak1non/project
 * https://mak1non.github.io/project/mortar.html
 */

enum state { BACKWARD, FORWARD, NEUTRAL, STOP };

enum direction { LEFT, RIGHT };

// 最高出力
const int maxOut = 255;

// ボタンのピン番号
const int stopBtn = 0;   // 停止スイッチ
const int fwdBtn = 1;    // 前進スイッチ
const int invBtn = 2;    // 後進スイッチ
const int leftBtn = 3;   // 左折スイッチ
const int rightBtn = 4;  // 右折スイッチ

// モータードライバー (TA7291P) のピン番号
// 左モーター
const int leftOut1 = 5;  // 入力1
const int leftOut2 = 6;  // 入力2

// 右モーター
const int rightOut1 = 9;   // 入力1
const int rightOut2 = 10;  // 入力2

// 走行状態
state carState;

void setup() {
    // 入力ピンの準備
    pinMode(stopBtn, INPUT_PULLUP);
    pinMode(fwdBtn, INPUT_PULLUP);
    pinMode(invBtn, INPUT_PULLUP);
    pinMode(leftBtn, INPUT_PULLUP);
    pinMode(rightBtn, INPUT_PULLUP);
    
    // 出力ピンの準備
    pinMode(leftOut1, OUTPUT);
    pinMode(leftOut2, OUTPUT);
    pinMode(rightOut1, OUTPUT);
    pinMode(rightOut2, OUTPUT);

    // 初期化
    neutral();
    delay(1000);
}

void loop() {
    // ボタン状態の読み取り
    if (digitalRead(stopBtn) == LOW) {
        stopHere();
    }
    if (digitalRead(fwdBtn) == LOW) {
        toForward();
    }
    if (digitalRead(invBtn) == LOW) {
        toBackward();
    }
    if (digitalRead(leftBtn) == LOW) {
        makeTurn(LEFT);
    }
    if (digitalRead(rightBtn) == LOW) {
        makeTurn(RIGHT);
    }
}

/*
 * ニュートラル
 */
void neutral() {
    carState = NEUTRAL;
    digitalWrite(leftOut1, LOW);
    digitalWrite(leftOut2, LOW);
    digitalWrite(rightOut1, LOW);
    digitalWrite(rightOut2, LOW);
}

/*
 * 止まる (TODO)
 */
void stopHere() {
    if (carState == FORWARD) {
        // 状態の更新
        carState = STOP;

        // 少しずつ弱くする
        for (int i = maxOut; i > 0; i--) {
            delay(5);
            analogWrite(leftOut1, i);
            analogWrite(rightOut1, i);
        }
    } else if (carState == BACKWARD) {
        // 状態の更新
        carState = STOP;

        // 少しずつ弱くする
        for (int i = maxOut; i > 0; i--) {
            delay(5);
            analogWrite(leftOut2, i);
            analogWrite(rightOut2, i);
        }
    }

    // 止める
    digitalWrite(leftOut1, LOW);
    digitalWrite(leftOut2, LOW);
    digitalWrite(rightOut1, LOW);
    digitalWrite(rightOut2, LOW);
}

/*
 * 前に進む
 */
void toForward() {
    // 前進状態以外でのみ実行
    if (carState != FORWARD) {
        neutral();

        // 前進状態にする
        carState = FORWARD;

        // 少しずつ強くする
        for (int i = 0; i < maxOut; i++) {
            delay(5);
            analogWrite(leftOut1, i);
            analogWrite(rightOut1, i);
        }
    }
}

/*
 * 後退する
 */
void toBackward() {
    // 後進状態以外でのみ実行
    if (carState != BACKWARD) {
        neutral();

        // 前進状態にする
        carState = BACKWARD;

        // 少しずつ強くする
        for (int i = 0; i < maxOut; i++) {
            delay(5);
            analogWrite(leftOut2, i);
            analogWrite(rightOut2, i);
        }
    }
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
            analogWrite(leftOut1, maxOut);
        } else {
            analogWrite(rightOut1, 0);
            delay(2000);
            analogWrite(rightOut1, maxOut);
        }
    }
}
