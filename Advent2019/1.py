def fuel_for_mass(mass):
    this_fuel = mass // 3 - 2
    if this_fuel <= 0:
        return 0
    else:
        return this_fuel + fuel_for_mass(this_fuel)

if __name__ == "__main__":
    total_fuel = 0
    with open("1.txt", "r") as infile:
        for mass in infile:
            total_fuel += int(mass) // 3 - 2

    print(f"Total fuel required (part 1): {total_fuel}")

    total_fuel = 0
    with open("1.txt", "r") as infile:
        for mass in infile:
            total_fuel += fuel_for_mass(int(mass))

    print(f"Total fuel required (part 2): {total_fuel}")
