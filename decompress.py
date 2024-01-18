import math
from bitstring import BitArray
from PIL import Image
import os
import time
import cProfile

def read_compressed_file(filepath):
    with open(filepath, 'rb') as file:
        return BitArray(file.read()).bin

def string_bits_to_int_list(binary_str):
    return [int(bit) for bit in binary_str]
def decode_header(header_bits):
    h_bits = ''.join(map(str, header_bits[:16]))
    f_bits = ''.join(map(str, header_bits[16:24]))
    l_bits = ''.join(map(str, header_bits[24:56]))
    no_bits = ''.join(map(str, header_bits[56:88]))
    h = int(h_bits, 2)
    f = int(f_bits, 2)
    l = int(l_bits, 2)
    no = int(no_bits, 2)

    return h, f, l, no
def decompress(filepath):
    B = read_compressed_file(filepath)
    B = string_bits_to_int_list(B)
    header_bits = B[:88]
    x, c_first, c_last, n = decode_header(header_bits)
    B = B[88:]
    y = n // x
    C = initialise_c(n, c_first, c_last)
    C = de_ic(B, C, 0, n - 1)
    N = [0] * n
    N[0] = C[0]
    for i in range(1, n):
        N[i] = C[i] - C[i - 1]
    e = [0] * n
    e[0] = N[0]
    for j in range(1, n):
        if N[j] % 2 == 0:
            e[j] = N[j] / 2
        else:
            e[j] = -((N[j] + 1) / 2)
    P = predict_inverse(e, x, y)
    return P
def de_ic(B, C, L, H):
    if H - L > 1:
        if C[L] == C[H]:
            for i in range(L + 1, H):
                C[i] = C[L]
        else:
            m = math.floor(0.5 * (H + L))
            g = math.ceil(math.log2(C[H] - C[L] + 1))
            extracted_bits = get_bits(B, g)
            C[m] = C[L] + decode(extracted_bits)
            if L < m:
                de_ic(B, C, L, m)
            if m < H:
                de_ic(B, C, m, H)
    return C

def decode(bits_list):
    binary_str = ''.join(map(str, bits_list))
    return int(binary_str, 2)

def get_bits(B, g):
    extracted_bits = B[:g]
    del B[:g]
    return extracted_bits

def predict_inverse(e, x, y):
    k = 0
    p = [[0 for i in range(y)] for j in range(x)]
    p[0][0] = e[0]
    for j in range(y):
        for i in range(x):
            if j == 0 and i != 0:
                p[i][j] = int(p[i - 1][j] - e[k])
            elif i == 0 and j != 0:
                p[i][j] = int(p[i][j - 1] - e[k])
            elif i != 0 and j != 0:
                if p[i - 1][j - 1] >= max(p[i - 1][j], p[i][j - 1]):
                    p[i][j] = int(min(p[i - 1][j], p[i][j - 1]) - e[k])
                elif p[i - 1][j - 1] <= min(p[i - 1][j], p[i][j - 1]):
                    p[i][j] = int(max(p[i - 1][j], p[i][j - 1]) - e[k])
                else:
                    p[i][j] = int(p[i - 1][j] + p[i][j - 1] - p[i - 1][j - 1] - e[k])
            k += 1
    return p
def initialise_c(n, c_first, c_last):
    C = [0] * n
    C[0] = c_first
    C[n-1] = c_last
    return C
def write_file(P, filepath):
    width = len(P[0])
    height = len(P)
    image = Image.new('L', (width, height)) # L - grayscale
    newPixels = image.load()

    for y in range(height):
        for x in range(width):
            newPixels[x, y] = P[y][x] # P[y][x] ker je P[y] vrstica, P[y][x] pa element v vrstici
    image.save(filepath)
def decompress_and_measure_time(filepath):

    start_time = time.time()
    image = decompress(filepath)
    end_time = time.time()
    elapsed_time = end_time - start_time
    output_path = os.path.join("output_decompressed", os.path.basename(filepath)[:-4] + "_decompressed.bmp")
    write_file(image, output_path)
    return elapsed_time

def main():
    output_folder = "output"
    bin_files = [f for f in os.listdir(output_folder) if f.endswith("Mosaic.bin")]
    with open("decompression_times.txt", "w") as time_file:
        for bin_file in bin_files:
            bin_filepath = os.path.join(output_folder, bin_file)
            elapsed_time = decompress_and_measure_time(bin_filepath)
            time_file.write(f"{bin_file}: {elapsed_time:.4f} s\n")

if __name__ == "__main__":
    main()
