import sys
import imageio
def read_image(imagepath):
    """Reads an image from the given file path.

      Args:
        imagepath: The path to the image file.

      Returns:
        A 3D numpy array representing the image.
    """
    image = imageio.v2.imread(imagepath)
    height, width = image.shape[:2]

    return image, height, width
#print(read_image("./slike/Baboon.bmp"))
p = [[23,21,21,23,23], [24,22,22,20,24],[23,22,22,19,23],[26,25,21,19,22]]
x = len(p) #višina slike
y = len(p[0]) #širina slike

#p, x, y = read_image("./slike/Barb.bmp")

def predict(p, x , y ):
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
                elif p[i - 1][j - 1] <= min(p[i - 1][j],p[i][j - 1]):
                    e[k] = max(p[i - 1][j],p[i][j-1]) - p[i][j]
                else:
                    e[k] = p[i-1][j] + p[i][j - 1] - p[i - 1][j - 1] - p[i][j]
                    print(e[k])

            k += 1

    return e
#p, x, y = read_image("./slike/Barb.bmp")
print(predict(p, x, y))


def compress(p, x, y):
    e = predict(p, x, y)
    n = x*y
    return 0


def main():

    return 0


if __name__ == "__main__":
    main()