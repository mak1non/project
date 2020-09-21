class MortarHandler:

    def __init__(self):
        self.direction = 'Stop'

    def judgeLine(self, leftBlock, rightBlock):
        """線の状態を識別する
        Args:
            leftBlock (int): 左ブロックエリア
            rightBlock (int): 右ブロックエリア
        """
        if leftBlock > 0 and rightBlock > 0:
            self.direction = 'Stop'
        elif leftBlock > 0:
            self.direction = 'Left'
        elif rightBlock > 0:
            self.direction = 'Right'
        else:
            self.direction = 'Forward'
