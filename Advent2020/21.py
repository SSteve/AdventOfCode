class Food:
    def __init__(self, ingredients: set[str], allergens: set[str]) -> None:
        self.ingredients = ingredients
        self.allergens = allergens


def ReadFood(food: str) -> Food:
    ingredientString, allergenString = food.split('(')
    ingredients = ingredientString.strip().split(" ")
    allergenString = allergenString.strip().removeprefix("contains ").removesuffix(')')
    allergens = allergenString.split(", ")
    food = Food(ingredients, allergens)
    return food


TEST = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""


def Part1(foods: list[Food]) -> tuple[int, dict[str, set[str]]]:
    allAllergens = set()
    allIngredients = set()
    for food in foods:
        allAllergens.update(food.allergens)
        allIngredients.update(food.ingredients)

    # Build a map of each allergen and all of the possible
    # ingredients that might contain it.
    allergenIngredients: dict[str, set[str]] = {}
    for allergen in allAllergens:
        for food in foods:
            if allergen in food.allergens:
                if allergen in allergenIngredients:
                    allergenIngredients[allergen].intersection_update(food.ingredients)
                else:
                    allergenIngredients[allergen] = set(food.ingredients)

    # Find the ingredients that aren't contained in any of the
    # lists of allergen-containing ingredients.
    safeIngredients = set()
    for ingredient in allIngredients:
        if not any(ingredient in allergenIngredients[allergen] for allergen in allergenIngredients):
            safeIngredients.add(ingredient)

    # Count the occurances of safe ingredients for part 1.
    safeIngredientCount = 0
    for safeIngredient in safeIngredients:
        safeIngredientCount += sum(safeIngredient in food.ingredients for food in foods)

    return safeIngredientCount, allergenIngredients


def Part2(allergenIngredients: dict[str, set[str]]) -> str:
    translations: dict[str, str] = {}
    allergen = ''
    while any(len(allergenIngredients[al]) for al in allergenIngredients):
        for allergen in allergenIngredients:
            if len(allergenIngredients[allergen]) == 1:
                break
        # This allergen is in only one possible ingredient so we've
        # found a match.
        ingredient = allergenIngredients[allergen].pop()
        translations[allergen] = ingredient
        # Remove this ingredients from all the other possibilities.
        for allergen in allergenIngredients:
            allergenIngredients[allergen].discard(ingredient)

    # Build the list of dangerous ingredients sorted by their allergen
    # for Part 2
    dangerousIngredients = ''
    for allergen in sorted(translations):
        dangerousIngredients += translations[allergen] + ","

    return dangerousIngredients.removesuffix(",")


if __name__ == "__main__":
    testFoods = []
    for line in TEST.splitlines():
        testFoods.append(ReadFood(line.strip()))
    testPart1, allergenIngredients1 = Part1(testFoods)
    assert testPart1 == 5
    testPart2 = Part2(allergenIngredients1)
    assert testPart2 == 'mxmxvkd,sqjhc,fvjkl'

    foods = []
    with open("21.txt", "r") as infile:
        for line in infile.readlines():
            foods.append(ReadFood(line.strip()))
    part1, allergenIngredients = Part1(foods)
    print(f"Part 1: {part1}")
    part2 = Part2(allergenIngredients)
    print(f"Part 2: {part2}")
    assert part2 == 'cljf,frtfg,vvfjj,qmrps,hvnkk,qnvx,cpxmpc,qsjszn'