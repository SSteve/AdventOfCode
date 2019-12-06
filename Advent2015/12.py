import json


def valueOf(obj, ignoreString = None):
    if isinstance(obj, str):
        return 0
    if isinstance(obj, int):
        return obj
    if isinstance(obj, dict):
        if ignoreString and ignoreString in obj.values():
            return 0
        total = 0
        for val in obj.values():
            total += valueOf(val, ignoreString)
        return total
    if isinstance(obj, list):
        total = 0
        for val in obj:
            total += valueOf(val, ignoreString)
        return total
    return 0




def day12(fileName, ignoreString = None):
    with open(fileName) as infile:
        jsonObj = json.load(infile)
    total = 0
    for x in jsonObj:
        total += valueOf(x, ignoreString)
    return total


print(day12("12.txt"))
print(day12("12.txt", "red"))
