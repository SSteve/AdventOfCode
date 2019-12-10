import re
from dataclasses import dataclass


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int

    def __getitem__(self, key):
        return eval(f"self.{key}")


def buildIngredients(fileName):
    ingredients = {}
    ingredientRegex = re.compile(r"(.+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)")
    with open(fileName) as infile:
        for line in infile:
            match = ingredientRegex.match(line)
            if match:
                ingredients[match[1]] = Ingredient(match[1], int(match[2]), int(match[3]), int(match[4]), int(match[5]), int(match[6]))
    return ingredients


def totalScore(ingredientAmounts, ingredients):
    props = ["capacity", "durability", "flavor", "texture"]
    total = 1
    for prop in props:
        propTotal = 0
        for ingredient in ingredientAmounts:
            propTotal += ingredients[ingredient][prop] * ingredientAmounts[ingredient]
        total *= max(0, propTotal)
    return total


def calories(ingredientAmounts, ingredients):
    caloriesTotal = 0
    for ingredient in ingredientAmounts:
        caloriesTotal += ingredients[ingredient]["calories"] * ingredientAmounts[ingredient]
    return caloriesTotal


def teaspoons(ingredientNumber, totalIngredients, inx):
    if ingredientNumber == 1:
        return 60 - inx
    if ingredientNumber == 2:
        return inx
    return 20


def day15(fileName, countCalories=False):
    ingredients = buildIngredients(fileName)
    highScore = 0
    for i in range(101):
        for j in range(0, 101 - i):
            for k in range(0, 101 - (i + j)):
                l = 100 - (i + j + k)
                recipe = {}
                tsps = [i, j, k, l]
                for ingredientNumber, ingredient in enumerate(ingredients):
                    recipe[ingredient] = tsps[ingredientNumber]
                if countCalories and calories(recipe, ingredients) != 500:
                    continue
                score = totalScore(recipe, ingredients)
                highScore = max(score, highScore)
    print(highScore)


day15("15.txt")
day15("15.txt", True)
