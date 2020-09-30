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
const int leftOut = 10;   // 左モーター
const int rightOut = 11;  // 右モーター

// 走行状態
// true: 移動中, false: 停止
bool carState = false;

void setup() {
    // 入力ピンの準備
    pinMode(stopBtn, INPUT);
    pinMode(fwdBtn, INPUT);
    pinMode(backBtn, INPUT);
    pinMode(leftBtn, INPUT);
    pinMode(rightBtn, INPUT);
  
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
        // 停止ボタン
        stopHere();
    } else if (digitalRead(fwdBtn) == LOW) {
        carState = true;
    }

    if (carState) {
        toForward();
    }
}

/*
 * 前に進む
 */
void toForward() {
    digitalWrite(leftOut, HIGH);
    digitalWrite(rightOut, HIGH);
}

/*
 * 止まる
 */
void stopHere() {
    // 移動中のみ止まる
    if (carState) {
        carState = false;

        // じわじわ止めていく
        for (int i = 255; i > 0; --i) {
            analogWrite(leftOut, i);
            analogWrite(rightOut, i);
            delay(5);
        }
    }
}
