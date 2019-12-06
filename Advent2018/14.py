def printTenScores(scores, firstIndex):
    score = ""
    for i in range(firstIndex, firstIndex + 10):
        score += f"{scores[i]}"
    print(score)


def partBScore(scores, firstIndex, targetLength, numberOfScores):
    partBScores = []
    for indexOffset in range(numberOfScores):
        if firstIndex - indexOffset < 0:
            continue
        score = 0
        for i in range(firstIndex - indexOffset, firstIndex + targetLength - indexOffset):
            score = 10 * score + scores[i]
        partBScores.append(score)
    return partBScores


def createRecipies(recipe1, recipe2):
    """
    Return a list of the recipies created from the two given recipies
    """
    newRecipe = recipe1 + recipe2
    recipies = []
    if newRecipe > 9:
        recipies.append(newRecipe // 10)
    recipies.append(newRecipe % 10)
    return recipies


def printScores(scores, firstElfIndex, secondElfIndex):
    for index, score in enumerate(scores):
        if index == firstElfIndex:
            print(f"({score})", end='')
        elif index == secondElfIndex:
            print(f"[{score}]", end='')
        else:
            print(f" {score} ", end='')
    print()


def a14(numberOfRecipies, quiet):
    scores = [3, 7]
    firstElfIndex = 0
    secondElfIndex = 1
    for _ in range(numberOfRecipies + 10):
        scores.extend(createRecipies(scores[firstElfIndex], scores[secondElfIndex]))
        firstElfIndex = (firstElfIndex + scores[firstElfIndex] + 1) % len(scores)
        secondElfIndex = (secondElfIndex + scores[secondElfIndex] + 1) % len(scores)
        if not quiet:
            printScores(scores, firstElfIndex, secondElfIndex)
    printTenScores(scores, numberOfRecipies)


def b14(targetScore, targetScoreLength, quiet):
    scores = [3, 7]
    firstElfIndex = 0
    secondElfIndex = 1
    partBScores = []
    while targetScore not in partBScores:
        newScores = createRecipies(scores[firstElfIndex], scores[secondElfIndex])
        scores.extend(newScores)
        firstElfIndex = (firstElfIndex + scores[firstElfIndex] + 1) % len(scores)
        secondElfIndex = (secondElfIndex + scores[secondElfIndex] + 1) % len(scores)
        if not quiet:
            printScores(scores, firstElfIndex, secondElfIndex)
        if len(scores) >= targetScoreLength:
            partBScores = partBScore(scores, len(scores) - targetScoreLength, targetScoreLength, len(newScores))

    print(f"{len(scores) - targetScoreLength - (len(newScores) - 1)} recipes to the left")


if __name__ == "__main__":
    # a14(38, False)
    b14(110201, 6, True)
