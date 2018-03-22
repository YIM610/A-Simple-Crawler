import math
from Bitmap import BitMap

class BloomFilter:
    def __init__(self, n):
        self.eleNum = n                                 #需要存储的元素个数
        self.m = int(n * 1.44 * math.log(n, 2))         #需要的位数
        self.k = int(math.log(2, math.e) * self.m / n)  #需要的hash个数
        self.seeds = []
        x = "131"
        for i in range(self.k):
            self.seeds.append(int(x))
            if(i % 2 == 0):
                x += "3"
            else:
                x += "1"
        self.bitmap = BitMap(max = self.m)
        self.count = 0

    def BKDRHash(self, str, seed):
        hash = 0
        for i in range(len(str)):
            hash = hash * seed + ord(str[i])
        return hash & (self.eleNum - 1)

    def hash(self, str, seeds):
        result = []
        for i in range(self.k):
            result.append(self.BKDRHash(str, seeds[i]))
        return result

    def set(self, string):
        calcmap = self.hash(string, self.seeds)
        for x in calcmap:
            self.bitmap.set(x)

    def test(self, string):
        calcmap = self.hash(string, self.seeds)
        for x in calcmap:
            if not self.bitmap.test(x):
                return False
        return True
