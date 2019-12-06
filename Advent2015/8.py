def day8(fileName):
    codeChars = 0
    memoryChars = 0
    encodedChars = 0
    with open(fileName) as infile:
        for line in infile:
            encodedString = line.strip().replace('\\', '\\\\').replace('"', '\\"')
            encodedChars += len(encodedString) + 2
            lineCodeChars = len(line.strip())
            codeChars += lineCodeChars
            lineString = eval(f"{line.strip()}")
            lineMemoryChars = len(lineString)
            memoryChars += lineMemoryChars
            
    return codeChars, memoryChars, encodedChars


codeChars, memoryChars, encodedChars = day8("8.txt")
print(f"{codeChars} - {memoryChars} = {codeChars - memoryChars}")
print(f"{encodedChars} - {codeChars} = {encodedChars - codeChars}")
