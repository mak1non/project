/*
 * 模型車両制御用プログラム
 * 
 * https://github.com/mak1non/project
 */

// ボタンのピン番号
const int stopBtn = 0;   // 停止スイッチ
const int fwdBtn = 1;    // 前進スイッチ
const int backBtn = 2;   // 後退スイッチ
const int leftBtn = 3;   // 左折スイッチ
const int rightBtn = 4;  // 右折スイッチ

// モーターのピン番号
const int leftOut = 9;    // 左モーター
const int rightOut = 11;  // 右モーター

// 走行状態
// 0: 停止, 1: 前進, 2: 後退, 3: 左折, 4: 右折
int carState = 0;

void setup() {
    // 入力ピンの準備
    pinMode(stopBtn, INPUT_PULLUP);
    pinMode(fwdBtn, INPUT_PULLUP);
    pinMode(backBtn, INPUT_PULLUP);
    pinMode(leftBtn, INPUT_PULLUP);
    pinMode(rightBtn, INPUT_PULLUP);
  
    // 出力ピンの準備
    pinMode(leftOut, OUTPUT);
    pinMode(rightOut, OUTPUT);

    // 初期化
    digitalWrite(leftOut, LOW);
    digitalWrite(rightOut, LOW);
}

void loop() {
    // ボタン状態の読み取り
    if (digitalRead(stopBtn) == LOW) {
        stopHere();
    } else if (digitalRead(fwdBtn) == LOW) {
        toForward();
    } else if (digitalRead(leftBtn) == LOW) {
        makeTurn(leftOut);
    } else if (digitalRead(rightBtn) == LOW) {
        makeTurn(rightOut);
    }
}

/*
 * 止まる
 */
void stopHere() {
    // 移動中のみ止まる
    if (carState == 1) {
        // じわじわ止めていく
        for (int i = 255; i > 0; i--) {
            delay(5);
            analogWrite(leftOut, i);
            analogWrite(rightOut, i);
        }
        carState = 0;
    }
}

/*
 * 前に進む
 */
void toForward() {
    if (carState == 0) {
        // じわじわ進めていく
        for (int i = 0; i < 255; i++) {
            delay(5);
            analogWrite(leftOut, i);
            analogWrite(rightOut, i);
        }
        carState = 1;
    }
}

/*
 * 曲がる
 */
void makeTurn(int pin) {
    if (carState == 1) {
        digitalWrite(pin, LOW);
        delay(1000);
        digitalWrite(pin, HIGH);
    }
}
