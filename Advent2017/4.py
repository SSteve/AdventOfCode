def a4(fileName):
    validCount = 0
    with open(fileName) as infile:
        for line in infile:
            rawWordList = line.strip().split(" ")
            wordList = []
            for word in rawWordList:
                word = sorted(word)
                wordList.append(''.join(word))
            wordSet = set(wordList)
            if len(wordList) == len(wordSet):
                validCount += 1
    return validCount                
                
if __name__ == "__main__":
    validCount = a4("4.txt")
    print(f"{validCount} valid passphrases.")
