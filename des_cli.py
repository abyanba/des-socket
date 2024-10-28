import binascii
import random

class BinString(str):
    def __new__(cls, *args, **kwargs):
        instance = super(BinString, cls).__new__(cls, *args, **kwargs)
        for char in instance:
            if char not in ('0', '1'):
                raise ValueError('Invalid input string for BinString')
        return instance

    def __xor__(self, other):
        result = bin(int(self, 2) ^ int(other, 2))[2:]
        result = result.zfill(max(len(self), len(other)))
        return BinString(result)

    def __lshift__(self, n):
        result = self[:]
        for _ in range(n):
            result = result[1:] + result[0]
        return BinString(result)

class StringConverter(object):
    @classmethod
    def to_bin(cls, s, hexstring=False):
        string = cls.to_hex(s) if not hexstring else s
        bits = ''
        for char in string:
            bits += bin(int(char, 16))[2:].zfill(4)
        while len(bits) % 64 != 0:
            bits += '0'
        return BinString(bits)

    @classmethod
    def from_bin(cls, s):
        hex_str = ''
        for i in range(0, len(s), 4):
            hex_str += hex(int(s[i:i+4], 2))[2:].zfill(1)
        return hex_str

    @staticmethod
    def from_hex(input_):
        # Do not decode to UTF-8, just return the hex representation
        return input_  # Return as is without decoding

class BinasciiConverter(StringConverter):
    @staticmethod
    def to_hex(input_):
        return binascii.hexlify(str(input_).encode('utf-8')).decode('utf-8')

    @staticmethod
    def from_hex(input_):
        return binascii.unhexlify(input_).decode('utf-8')

class DES:
    PC_1 = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]

    PC_2 = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]

    PI = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9, 1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]

    E = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]

    # S boxes
    S = [
        #S1
        [
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
        ],

        #S2
        [
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
        ],

        #S3
        [
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
        ],

        #S4
        [
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
        ],

        #S5
        [
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
        ],

        #S6
        [
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
        ],

        #S7
        [
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
        ],

        #S8
        [
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
        ]
    ]

    P = [
        16, 7, 20, 21,
        29, 12, 28, 17,
        1, 15, 23, 26,
        5, 18, 31, 10,
        2, 8, 24, 14,
        32, 27, 3, 9,
        19, 13, 30, 6,
        22, 11, 4, 25,
    ]

    PI_1 = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9, 49, 17, 57, 25,
    ]

    @staticmethod
    def generate_des_key():
        key = []
        for i in range(8):
            byte = random.getrandbits(7)
            parity_bit = 1 if bin(byte).count('1') % 2 == 0 else 0
            key.append((byte << 1) | parity_bit)
        return ''.join(f'{byte:02X}' for byte in key)

    def __init__(self, converter=BinasciiConverter, **kwargs):
        self.converter = converter
        if kwargs.get('key'):
            self._set_key(kwargs['key'], kwargs.get('hexkey', False))
    
    def _set_key(self, key, hexkey=False):
        self.key = self.converter.to_bin(key, hexkey)

    def _permute_with(self, string, permutation):
        return ''.join([string[i-1] for i in permutation])
    
    def _group_by(self, string, by):
        return [string[i:i+by] for i in range(0, len(string), by)]
    
    def f(self, r, k):
        e = BinString(self._permute_with(r, self.E))
        k_xor_e = BinString(k) ^ e
        S = ''
        blocks = self._group_by(k_xor_e, 6)
        for n in range(8):
            i = int(blocks[n][0] + blocks[n][-1], 2)
            j = int(blocks[n][1:-1], 2)
            S += bin(self.S[n][i][j])[2:].zfill(4)
        return BinString(self._permute_with(S, self.P))

    def encrypt(self, string, **kwargs):
        self._set_key(kwargs['key'], kwargs.get('hexkey', False))
        self.message = self.converter.to_bin(string, kwargs.get('hexstring', False))

        # Pad message
        while len(self.message) % 64 != 0:
            self.message += '0'

        pc1_key = self._permute_with(self.key, self.PC_1)
        C = [BinString(pc1_key[:28])]
        D = [BinString(pc1_key[28:])]

        for i in range(16):
            shift = 1 if i in (0, 1, 8, 15) else 2
            C.append(C[-1] << shift)
            D.append(D[-1] << shift)

        K = []
        for i in range(16):
            CD = C[i+1] + D[i+1]
            K.append(self._permute_with(CD, self.PC_2))
        
        result = ''
        for block in self._group_by(self.message, 64):
            PI = self._permute_with(block, self.PI)
            L = [BinString(PI[:32])]
            R = [BinString(PI[32:])]
            for i in range(16):
                Ln = R[-1]
                Rn = L[-1] ^ self.f(R[-1], K[i])
                L.append(Ln)
                R.append(Rn)
            RL = R[-1] + L[-1]
            result += self._permute_with(RL, self.PI_1)

        return self.converter.from_bin(result)

    def decrypt(self, string, key, hexkey=False):
        # Menggunakan fungsi encrypt dengan argumen yang diperlukan
        return self.encrypt(string, key=key, hexkey=hexkey, decrypt=True)