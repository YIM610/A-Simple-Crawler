class BitMap(object):
    def __init__(self, max):
        self.size = int((max + 31) / 32)               #向上取整获得整型数的个数
        self.array = [0 for i in range(self.size)]    #初始为0

    def getIndex(self, num, up = False):
        if up:
            return int((num + 31) / 32)
        return int(num / 32)

    def getBitIndex(self, num):
        return num % 32

    def set(self, num):
        index = self.getIndex(num)
        bitIndex = self.getBitIndex(num)
        ele = self.array[index]
        self.array[index] = ele | (1 << (31 - bitIndex))

    def test(self, i):
        index = self.getIndex(i)
        bitIndex = self.getBitIndex(i)
        if self.array[index] & (1 <<(31 - bitIndex)):
            return True
        return False
