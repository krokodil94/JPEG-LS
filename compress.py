import sys
import imageio
import numpy as np
import math
from bitstring import BitArray
#Preberemo sliko
def read_image(imagepath):
    image = imageio.v2.imread(imagepath)
    height, width = image.shape[:2]
    return image.tolist(), height, width

def predict(p, x, y):
    k = 0
    e = [0] * x * y
    for j in range(y):
        for i in range(x):
            if i == 0 and j == 0:
                e[k] = p[i][j]
            elif i == 0:
                e[k] = p[i][j - 1] - p[i][j]
            elif j == 0:
                e[k] = p[i - 1][j] - p[i][j]
            else:
                if p[i - 1][j - 1] >= max(p[i - 1][j], p[i][j - 1]):
                    e[k] = min(p[i - 1][j], p[i][j - 1]) - p[i][j]
                elif p[i - 1][j - 1] <= min(p[i - 1][j], p[i][j - 1]):
                    e[k] = max(p[i - 1][j], p[i][j - 1]) - p[i][j]
                else:
                    e[k] = p[i - 1][j] + p[i][j - 1] - p[i - 1][j - 1] - p[i][j]
            k += 1
    return e


def setHeader(h, f, l, no):
    h_bits = [int(bit) for bit in bin(h)[2:].zfill(16)]
    f_bits = [int(bit) for bit in bin(f)[2:].zfill(8)]
    l_bits = [int(bit) for bit in bin(l)[2:].zfill(32)]
    no_bits = [int(bit) for bit in bin(no)[2:].zfill(32)]
    header = h_bits + f_bits + l_bits + no_bits
    return header

def encode(g, c):
    binary_representation = bin(c)[2:]  # Convert to binary and remove the '0b' prefix
    padded_binary = binary_representation.zfill(g)  # Pad with zeros to the specified length
    binary_list = [int(bit) for bit in padded_binary]  # Convert to a list of integers
    return binary_list



def ic(B,C,L,H):
    if H - L > 1:
        if C[H] != C[L]:
            m = math.floor(0.5 * (H + L))
            g = math.ceil(math.log((C[H]-C[L] + 1),2))
            B.extend(encode(g,(C[m]- C[L])))
            if L < m:
                ic(B,C,L,m)
            if m < H:
                ic(B,C,m,H)
    return B
def compress(p, x, y):
    e = predict(p, x, y)
    n = x * y
    N = [0] * n
    C = [0] * n
    B = []
    N[0] = e[0]
    for i in range(1, n):
        if e[i] >= 0:
            N[i] = 2 * e[i]
        else:
            N[i] = 2 * abs(e[i]) - 1
    C[0] = N[0]
    for j in range(1, n):
        C[j] = C[j - 1] + N[j]
    B.extend(setHeader(x, C[0], C[n-1], n))
    B_1 = []
    B.extend(ic(B_1,C,0,n-1))
    return B


def encode(g, c):
    binary_representation = bin(c)[2:]  # Convert to binary and remove the '0b' prefix
    padded_binary = binary_representation.zfill(g)  # Pad with zeros to the specified length
    binary_list = [int(bit) for bit in padded_binary]  # Convert to a list of integers
    return binary_list


p, x, y = read_image("./slike BMP2/Baboon.bmp")

B = compress(p,x,y)



def writeFile(B, filepath):
    # Convert the list of bits to a bitstring
    bitstream = BitArray(B)

    # Open the file in binary write mode ('wb')
    with open(filepath, 'wb') as file:
        # Write the bitstream to the file
        file.write(bitstream.tobytes())
writeFile(B, "./outPut1.bin")


"""p = [[23, 21, 21, 23, 23], [24, 22, 22, 20, 24], [23, 22, 22, 19, 23], [26, 25, 21, 19, 22]]
x = len(p)  # višina slike
y = len(p[0])  # širina slike
B = compress(p, x, y)
e = [23, -1, 1, -3, 2, 0, 0, 0, 0, 0, 0, 4, -2, 3, 1, 0, 0, -4, 0, 1]
n = [23, 1, 2, 5, 4, 0, 0, 0, 0, 0, 0, 8, 3, 6, 2, 0, 0, 7, 0, 2]
c = [23, 24, 26, 31, 35, 35, 35, 35, 35, 35, 35, 43, 46, 52, 54, 54, 54, 61, 61, 63]"""
print(len(B))
def main():
    return 0


if __name__ == "__main__":
    main()




