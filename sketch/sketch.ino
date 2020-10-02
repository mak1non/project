/*
 * 模型車両制御用プログラム
 * 
 * https://github.com/mak1non/project
 * https://mak1non.github.io/project/mortar.html
 */

// ボタンのピン番号
const int stopBtn = 0;   // 停止スイッチ
const int fwdBtn = 1;    // 前進スイッチ
const int backBtn = 2;   // 後退スイッチ
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
// 0: 無, 1: 前進, 2: ブレーキ
const int carState = 0;

void setup() {
    // 入力ピンの準備
    pinMode(stopBtn, INPUT_PULLUP);
    pinMode(fwdBtn, INPUT_PULLUP);
    pinMode(backBtn, INPUT_PULLUP);
    pinMode(leftBtn, INPUT_PULLUP);
    pinMode(rightBtn, INPUT_PULLUP);
  
    // 出力ピンの準備
    pinMode(leftOut1, OUTPUT);
    pinMode(leftOut2, OUTPUT);
    pinMode(rightOut1, OUTPUT);
    pinMode(rightOut2, OUTPUT);

    // 初期化
    digitalWrite(leftOut1, LOW);
    digitalWrite(leftOut2, LOW);
    digitalWrite(rightOut1, LOW);
    digitalWrite(rightOut2, LOW);
}

void loop() {
    // ボタン状態の読み取り
    if (digitalRead(stopBtn) == LOW) {
        stopHere();
    } else if (digitalRead(fwdBtn) == LOW) {
        toForward();
    } else if (digitalRead(leftBtn) == LOW) {
        makeTurn();
    } else if (digitalRead(rightBtn) == LOW) {
        makeTurn();
    }
}

/*
 * 止まる
 */
void stopHere() {
}

/*
 * 前に進む
 */
void toForward() {
    // 前進状態以外でのみ実行
    if (carState != 1) {
        // 前進状態にする
        carState = 1;

        // 少しずつ強くする
        for (int i = 0; i < 255; i++) {
            delay(5);
            analogWrite(leftOut1, i);
            analogWrite(rightOut1, i);
        }
    }
}

/*
 * 曲がる
 */
void makeTurn() {
}