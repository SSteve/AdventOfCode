def Day15(seed: str, limit: int = 2020) -> int:
    history = [int(num) for num in seed.split(",")]
    for _ in range(limit - len(history)):
        lastNumber = history[-1:][0]
        if lastNumber in history[:-1]:
            indexPos = len(history) - history[-2::-1].index(lastNumber) - 2
            sinceLast = len(history) - indexPos - 1
            history.append(sinceLast)
        else:
            history.append(0)
    return history[-1:][0]


assert Day15("0,3,6") == 436
assert Day15("1,3,2") == 1
assert Day15("2,1,3") == 10
assert Day15("1,2,3") == 27
assert Day15("2,3,1") == 78
assert Day15("3,2,1") == 438
assert Day15("3,1,2") == 1836

assert Day15("0,3,6") == 436

print(Day15("1,17,0,10,18,11,6"))
print(Day15("1,17,0,10,18,11,6", 30000000))
