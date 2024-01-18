import imageio
import math
from bitstring import BitArray
import time
import cProfile
def read_image(imagepath):

    image = imageio.v2.imread(imagepath)
    height, width = image.shape[:2]
    return image.tolist(), height, width

def predict(p, x, y):
    # p == image
    # x == height
    # y == width
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
    # h == višina slike
    # f == prvi element iz C
    # l == zadnji element iz C
    # no == število elementov v C
    h_bits = [int(bit) for bit in bin(h)[2:].zfill(16)]
    f_bits = [int(bit) for bit in bin(f)[2:].zfill(8)]
    l_bits = [int(bit) for bit in bin(l)[2:].zfill(32)]
    no_bits = [int(bit) for bit in bin(no)[2:].zfill(32)]
    header = h_bits + f_bits + l_bits + no_bits
    return header

def encode(g, c):
    # g == število bitov
    # c == vrednost
    binary_representation = bin(c)[2:]
    padded_binary = binary_representation.zfill(g)
    binary_list = [int(bit) for bit in padded_binary]
    return binary_list

def ic(B, C, L, H):
    if H - L > 1:
        if C[H] != C[L]:
            m = math.floor(0.5 * (H + L))
            g = math.ceil(math.log2((C[H] - C[L] + 1)))
            B.extend(encode(g, (C[m] - C[L])))
            if L < m:
                ic(B, C, L, m)
            if m < H:
                ic(B, C, m, H)
    return B

def compress(p, x, y):
    # p == slika
    # x == višina
    # y == širina
    e = predict(p, x, y)
    n = x * y
    N = [0] * n
    C = [0] * n
    N[0] = e[0]
    for i in range(1, n):
        N[i] = 2 * e[i] if e[i] >= 0 else 2 * abs(e[i]) - 1
    C[0] = N[0]
    for j in range(1, n):
        C[j] = C[j - 1] + N[j]
    B = setHeader(x, C[0], C[n - 1], n)
    B1 = []
    B.extend(ic(B1, C, 0, n - 1))
    return B


def writeFile(B, filepath):
    bitstream = BitArray(B)
    with open(filepath, 'wb') as file:
        file.write(bitstream.tobytes())

def main():
    image_files = [

        "Mosaic.bmp"
    ]
    with open("compression_times.txt", "w") as time_file:
        for image in image_files:
            image_path = f"./slike BMP2/{image}"

            start_time = time.time()

            p, x, y = read_image(image_path)
            B = compress(p, x, y)

            output_file = f"./output/{image[:-4]}.bin"
            writeFile(B, output_file)

            end_time = time.time()
            elapsed_time = end_time - start_time

            time_file.write(f"{image}: {elapsed_time:.4f} s\n")

if __name__ == "__main__":
    main()

