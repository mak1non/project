from direction import Direction


class Car:
    def __init__(self):
        self.direction = Direction.STOP

    def judgeLine(self, leftBlock, rightBlock):
        """線に合わせて進行方向を変える
        Args:
            leftBlock (int): 左ブロックエリア
            rightBlock (int): 右ブロックエリア
        """
        if leftBlock > 0 and rightBlock > 0:
            self.direction = Direction.STOP
        elif leftBlock > 0:
            self.direction = Direction.LEFT
        elif rightBlock > 0:
            self.direction = Direction.RIGHT
        else:
            self.direction = Direction.FORWARD

    # TODO
    def run(self):
        """実際にモーターを動作させる
        """
        print(self.direction)
