from direction import Direction


class MortarHandler:

    def __init__(self):
        self.direction = Direction.STOP

    def judgeLine(self, leftBlock, rightBlock):
        """線の状態を識別する
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
