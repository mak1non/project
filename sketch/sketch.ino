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
const int btn = 0;  // 停止スイッチ

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
    pinMode(btn, INPUT_PULLUP);

    // 出力ピンの準備
    pinMode(leftOut1, OUTPUT);
    pinMode(leftOut2, OUTPUT);
    pinMode(rightOut1, OUTPUT);
    pinMode(rightOut2, OUTPUT);

    // 初期化
    neutral();
}

void loop() {
    // ボタン状態の読み取り
    if (digitalRead(stopBtn) == LOW) {
        toForward();
    } else {
        stopHere();
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

        // ブレーキをかける
        digitalWrite(leftOut1, HIGH);
        digitalWrite(leftOut2, HIGH);
        digitalWrite(rightOut1, HIGH);
        digitalWrite(rightOut2, HIGH);
    }
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
 * 曲がる (TODO)
 *
 * dir: 曲がる方向
 */
void makeTurn(direction dir) {
    // 止めるピン番号
    int pin;

    // 左右の識別
    if (dir == LEFT) {
        pin = leftOut2;
    } else {
        pin = rightOut2;
    }

    // ブレーキ動作
    digitalWrite(pin, HIGH);
    delay(100);  // 要調整
    digitalWrite(pin, LOW);
}
