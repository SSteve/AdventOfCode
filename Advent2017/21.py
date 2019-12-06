import re
import numpy as np

rule2Regex = re.compile(r"([.#]{2})/([.#]{2}) => ([.#]{3})/([.#]{3})/([.#]{3})")
rule3Regex = re.compile(r"([.#]{3})/([.#]{3})/([.#]{3}) => ([.#]{4})/([.#]{4})/([.#]{4})/([.#]{4})")


def addArrayToPatternDict(arr, outputPattern, patternList):
    patternList[arr.tostring()] = outputPattern
    rot = np.rot90(arr).tostring()
    if rot not in patternList:
        patternList[rot] = outputPattern
    rot = np.rot90(np.rot90(arr)).tostring()
    if rot not in patternList:
        patternList[rot] = outputPattern
    rot = np.rot90(np.rot90(np.rot90(arr))).tostring()
    if rot not in patternList:
        patternList[rot] = outputPattern


def day21(fileName, iterations):
    pattern2 = {}
    pattern3 = {}
    with open(fileName) as infile:
        for line in infile:
            match = rule2Regex.match(line)
            if match:
                arr = np.array([[*match[1]], [*match[2]]])
                outputPattern = np.array([[*match[3]], [*match[4]], [*match[5]]])
                addArrayToPatternDict(arr, outputPattern, pattern2)
                addArrayToPatternDict(np.fliplr(arr), outputPattern, pattern2)
                addArrayToPatternDict(np.flipud(arr), outputPattern, pattern2)
                continue
            match = rule3Regex.match(line)
            if match:
                arr = np.array([[*match[1]], [*match[2]], [*match[3]]])
                outputPattern = np.array([[*match[4]], [*match[5]], [*match[6]], [*match[7]]])
                addArrayToPatternDict(arr, outputPattern, pattern3)
                addArrayToPatternDict(np.fliplr(arr), outputPattern, pattern3)
                addArrayToPatternDict(np.flipud(arr), outputPattern, pattern3)

    artArray = np.array([[".", "#", "."], [".", ".", "#"], ["#", "#", "#"]])
    for _ in range(iterations):
        if artArray.shape[0] & 1:
            # divisible by 3
            newSize = int(artArray.shape[0] * 4 / 3)
            newArray = np.full((newSize, newSize), " ", dtype='<U1')
            for row in range(int(artArray.shape[0] / 3)):
                for col in range(int(artArray.shape[0] / 3)):
                    inputArray = artArray[row * 3:row * 3 + 3, col * 3:col * 3 + 3]
                    outputArray = pattern3[inputArray.tostring()]
                    newArray[row * 4:row * 4 + 4, col * 4:col * 4 + 4] = outputArray
            artArray = newArray
        else:
            # divisible by 2
            newSize = int(artArray.shape[0] * 3 / 2)
            newArray = np.full((newSize, newSize), " ", dtype='<U1')
            for row in range(int(artArray.shape[0] / 2)):
                for col in range(int(artArray.shape[0] / 2)):
                    inputArray = artArray[row * 2:row * 2 + 2, col * 2:col * 2 + 2]
                    outputArray = pattern2[inputArray.tostring()]
                    newArray[row * 3:row * 3 + 3, col * 3:col * 3 + 3] = outputArray
            artArray = newArray
    # Have to do sum once for each dimension
    return sum(sum(np.char.count(artArray, "#")))


if __name__ == "__main__":
    litPixels = day21("21.txt", 5)
    print(litPixels)
    litPixels = day21("21.txt", 18)
    print(litPixels)
