

class md5():
    def __init__(self):
        self.A = self.hex2bin('01234567')
        self.B = self.hex2bin('89abcdef')
        self.C = self.hex2bin('fedcba98')
        self.D = self.hex2bin('76543210')
        self.a = self.A
        self.b = self.B
        self.c = self.C
        self.d = self.D
        self.LAST_DATA = []
    def int2bin(self, x, base):
        res = []
        for i in range(base):
            res.append(x & 1)
            x >>= 1
        res.reverse()
        return res
    def bin2int(self, a, base):
        x = 0
        for i in range(base):
            x *= 2
            x += a[i]
        return x
    def hex2bin(self, s):
        x = 0
        for i in s:
            x *= 16
            if i == 'a':
                x += 10
            elif i == 'b':
                x += 11
            elif i == 'c':
                x += 12
            elif i == 'd':
                x += 13
            elif i == 'e':
                x += 14
            elif i == 'f':
                x += 15
            else:
                x += int(i)
        return self.int2bin(x, 32)
    def bin2hex(self, a):
        res = ''
        while len(a) != 0:
            x = a[0] * 8 + a[1] * 4 + a[2] * 2 + a[3]
            if x == 10:
                res += 'a'
            elif x == 11:
                res += 'b'
            elif x == 12:
                res += 'c'
            elif x == 13:
                res += 'd'
            elif x == 14:
                res += 'e'
            elif x == 15:
                res += 'f'
            else:
                res += str(x)
            a = a[4:]
        return res
    def Input(self, data):
        print data
        temp1 = []
        for i in data:
            temp1 += self.int2bin(ord(i), 8)
        c = len(temp1)
        while len(temp1) % 512 != 448:
            temp1.append(0)
        temp1 += self.int2bin(c ,64)
        self.DATA = []
        while len(temp1) != 0:
            t = []
            for i in range(16):
                t.append(temp1[:32])
                temp1 = temp1[32:]
            self.DATA.append(t)

    def AND(self, a, b):
        res = []
        for i in range(len(a)):
            res.append( (a[i] & b[i]) )
        return res
    def OR(self, a, b):
        res = []
        for i in range(len(a)):
            res.append( (a[i] | b[i]) )
        return res
    def XOR(self, a, b):
        res = []
        for i in range(len(a)):
            res.append( (a[i] ^ b[i]) )
        return res
    def OPP(self, a):
        res = []
        for i in a:
            if i == 0:
                res.append(1)
            else:
                res.append(0)
        return res
    def ADD(self, a, b):
        x = self.bin2int(a, 32)
        y = self.bin2int(b, 32)
        return self.int2bin(x + y, 32)
    def LeftMove(self, a, s):
        return a[s:] + a[:s]

    def F(self, X, Y, Z):
        return self.OR(self.AND(X, Y), self.AND(self.OPP(X), Z))
    def G(self, X, Y, Z):
        return self.OR(self.AND(X, Z), self.AND(Y, self.OPP(Z)))
    def H(self, X, Y, Z):
        return self.XOR(self.XOR(X, Y), Z)
    def I(self, X, Y, Z):
        return self.XOR(Y, self.OR(X, self.OPP(Z)))

    def FF(self, kind, M, s, t):
        if kind == 1:
            self.a = self.ADD(self.b, self.LeftMove(self.ADD(self.ADD(self.a, self.F(self.b, self.c, self.d)), self.ADD(M, t)), s))
        elif kind == 2:
            self.b = self.ADD(self.c, self.LeftMove(self.ADD(self.ADD(self.b, self.F(self.c, self.d, self.a)), self.ADD(M, t)), s))
        elif kind == 3:
            self.c = self.ADD(self.d, self.LeftMove(self.ADD(self.ADD(self.c, self.F(self.d, self.a, self.b)), self.ADD(M, t)), s))
        else:
            self.d = self.ADD(self.a, self.LeftMove(self.ADD(self.ADD(self.d, self.F(self.a, self.b, self.c)), self.ADD(M, t)), s))
    def GG(self, kind, M, s, t):
        if kind == 1:
            self.a = self.ADD(self.b, self.LeftMove(self.ADD(self.ADD(self.a, self.G(self.b, self.c, self.d)), self.ADD(M, t)), s))
        elif kind == 2:
            self.b = self.ADD(self.c, self.LeftMove(self.ADD(self.ADD(self.b, self.G(self.c, self.d, self.a)), self.ADD(M, t)), s))
        elif kind == 3:
            self.c = self.ADD(self.d, self.LeftMove(self.ADD(self.ADD(self.c, self.G(self.d, self.a, self.b)), self.ADD(M, t)), s))
        else:
            self.d = self.ADD(self.a, self.LeftMove(self.ADD(self.ADD(self.d, self.G(self.a, self.b, self.c)), self.ADD(M, t)), s))
    def HH(self, kind, M, s, t):
        if kind == 1:
            self.a = self.ADD(self.b, self.LeftMove(self.ADD(self.ADD(self.a, self.H(self.b, self.c, self.d)), self.ADD(M, t)), s))
        elif kind == 2:
            self.b = self.ADD(self.c, self.LeftMove(self.ADD(self.ADD(self.b, self.H(self.c, self.d, self.a)), self.ADD(M, t)), s))
        elif kind == 3:
            self.c = self.ADD(self.d, self.LeftMove(self.ADD(self.ADD(self.c, self.H(self.d, self.a, self.b)), self.ADD(M, t)), s))
        else:
            self.d = self.ADD(self.a, self.LeftMove(self.ADD(self.ADD(self.d, self.H(self.a, self.b, self.c)), self.ADD(M, t)), s))
    def II(self, kind, M, s, t):
        if kind == 1:
            self.a = self.ADD(self.b, self.LeftMove(self.ADD(self.ADD(self.a, self.I(self.b, self.c, self.d)), self.ADD(M, t)), s))
        elif kind == 2:
            self.b = self.ADD(self.c, self.LeftMove(self.ADD(self.ADD(self.b, self.I(self.c, self.d, self.a)), self.ADD(M, t)), s))
        elif kind == 3:
            self.c = self.ADD(self.d, self.LeftMove(self.ADD(self.ADD(self.c, self.I(self.d, self.a, self.b)), self.ADD(M, t)), s))
        else:
            self.d = self.ADD(self.a, self.LeftMove(self.ADD(self.ADD(self.d, self.I(self.a, self.b, self.c)), self.ADD(M, t)), s))

    def mainProcess(self):
        for i in self.DATA:
            self.FF(1, i[0], 7, self.hex2bin('d76aa478'))
            self.FF(4, i[1], 12, self.hex2bin('e8c7b756'))
            self.FF(3, i[2], 17, self.hex2bin('242070db'))
            self.FF(2, i[3], 22, self.hex2bin('c1bdceee'))
            self.FF(1, i[4], 7, self.hex2bin('f57c0faf'))
            self.FF(4, i[5], 12, self.hex2bin('4787c62a'))
            self.FF(3, i[6], 17, self.hex2bin('a8304613'))
            self.FF(2, i[7], 22, self.hex2bin('fd469501'))
            self.FF(1, i[8], 7, self.hex2bin('698098d8'))
            self.FF(4, i[9], 12, self.hex2bin('8b44f7af'))
            self.FF(3, i[10], 17, self.hex2bin('ffff5bb1'))
            self.FF(2, i[11], 22, self.hex2bin('895cd7be'))
            self.FF(1, i[12], 7, self.hex2bin('6b901122'))
            self.FF(4, i[13], 12, self.hex2bin('fd987193'))
            self.FF(3, i[14], 17, self.hex2bin('a679438e'))
            self.FF(2, i[15], 22, self.hex2bin('49b40821'))

            self.GG(1, i[1], 5, self.hex2bin('f61e2562'))
            self.GG(4, i[6], 9, self.hex2bin('c040b340'))
            self.GG(3, i[11], 14, self.hex2bin('265e5a51'))
            self.GG(2, i[0], 20, self.hex2bin('e9b6c7aa'))
            self.GG(1, i[5], 5, self.hex2bin('d62f105d'))
            self.GG(4, i[10], 9, self.hex2bin('02441453'))
            self.GG(3, i[15], 14, self.hex2bin('d8a1e681'))
            self.GG(2, i[4], 20, self.hex2bin('e7d3fbc8'))
            self.GG(1, i[9], 5, self.hex2bin('21e1cde6'))
            self.GG(4, i[14], 9, self.hex2bin('c33707d6'))
            self.GG(3, i[3], 14, self.hex2bin('f4d50d87'))
            self.GG(2, i[8], 20, self.hex2bin('455a14ed'))
            self.GG(1, i[12], 5, self.hex2bin('a9e3e905'))
            self.GG(4, i[2], 9, self.hex2bin('fcefa3f8'))
            self.GG(3, i[7], 14, self.hex2bin('676f02d9'))
            self.GG(2, i[12], 20, self.hex2bin('8d2a4c8a'))

            self.HH(1, i[5], 4, self.hex2bin('fffa3942'))
            self.HH(4, i[8], 11, self.hex2bin('8771f681'))
            self.HH(3, i[11], 16, self.hex2bin('6d9d6122'))
            self.HH(2, i[14], 23, self.hex2bin('fde5380c'))
            self.HH(1, i[1], 4, self.hex2bin('a4beea44'))
            self.HH(4, i[4], 11, self.hex2bin('4bdecfa9'))
            self.HH(3, i[7], 16, self.hex2bin('f6bb4b60'))
            self.HH(2, i[10], 23, self.hex2bin('bebfbc70'))
            self.HH(1, i[13], 4, self.hex2bin('289b7ec6'))
            self.HH(4, i[0], 11, self.hex2bin('eaa127fa'))
            self.HH(3, i[3], 16, self.hex2bin('d4ef3085'))
            self.HH(2, i[6], 23, self.hex2bin('04881d05'))
            self.HH(1, i[9], 4, self.hex2bin('d9d4d039'))
            self.HH(4, i[12], 11, self.hex2bin('e6db99e5'))
            self.HH(3, i[15], 16, self.hex2bin('1fa27cf8'))
            self.HH(2, i[2], 23, self.hex2bin('c4ac5665'))

            self.II(1, i[0], 6, self.hex2bin('f4292244'))
            self.II(4, i[7], 10, self.hex2bin('432aff97'))
            self.II(3, i[14], 15, self.hex2bin('ab9423a7'))
            self.II(2, i[5], 21, self.hex2bin('fc93a039'))
            self.II(1, i[12], 6, self.hex2bin('655b59c3'))
            self.II(4, i[3], 10, self.hex2bin('8f0ccc92'))
            self.II(3, i[10], 15, self.hex2bin('ffeff47d'))
            self.II(2, i[1], 21, self.hex2bin('85845dd1'))
            self.II(1, i[8], 6, self.hex2bin('6fa87e4f'))
            self.II(4, i[15], 10, self.hex2bin('fe2ce6e0'))
            self.II(3, i[6], 15, self.hex2bin('a3014214'))
            self.II(2, i[13], 21, self.hex2bin('4e0811a1'))
            self.II(1, i[14], 6, self.hex2bin('f7537e82'))
            self.II(4, i[11], 10, self.hex2bin('bd3af235'))
            self.II(3, i[2], 15, self.hex2bin('2ad7d2bb'))
            self.II(2, i[9], 21, self.hex2bin('eb86d391'))

            res = self.ADD(self.A, self.a)
            res += self.ADD(self.B, self.b)
            res += self.ADD(self.C, self.c)
            res += self.ADD(self.D, self.d)
            self.LAST_DATA.append(res)

    def Output(self):
        for i in self.LAST_DATA:
            print self.bin2hex(i)
test1 = md5()
test1.Input('HelloWorld')
test1.mainProcess()
test1.Output()