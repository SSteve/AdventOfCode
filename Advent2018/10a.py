import re


class PointOfLight:
    def __init__(self, px, py, vx, vy):
        self.positionX = px
        self.positionY = py
        self.velocityX = vx
        self.velocityY = vy

    def __repr__(self):
        return f"PointOfLight({self.positionX}, {self.positionY}, " \
            f"{self.velocityX}, {self.velocityY})"

    def afterSeconds(self, seconds):
        return (self.positionX + self.velocityX * seconds,
                self.positionY + self.velocityY * seconds)


compiled = re.compile(
    r"position=<\s*([-\d]+),\s*([-\d]+)> velocity=<\s*([-\d]+),\s*([-\d]+)>")

pointsOfLight = []


def showPoints(points):
    minimumX = 1e12
    minimumY = 1e12
    maximumX = -1e12
    maximumY = -1e12
    for point in points:
        minimumX = min(minimumX, point[0])
        maximumX = max(maximumX, point[0])
        minimumY = min(minimumY, point[1])
        maximumY = max(maximumY, point[1])
    if (maximumX - minimumX) > 200 or (maximumY - minimumY) > 15:
        # print(f"{maximumX - minimumX}, {maximumY - minimumY}")
        return False
    row = ['.'] * (maximumX - minimumX + 1)
    pointArray = []
    for i in range(maximumY - minimumY + 1):
        pointArray.append(row.copy())
    for point in points:
        pointArray[point[1] - minimumY][point[0] - minimumX] = '#'
    for pointRow in pointArray:
        print(''.join(pointRow))
    return True


with open("10.txt", "r") as infile:
    for line in infile:
        result = compiled.match(line)
        if result:
            positionX = int(result[1])
            positionY = int(result[2])
            velocityX = int(result[3])
            velocityY = int(result[4])
            pointsOfLight.append(PointOfLight(
                positionX, positionY, velocityX, velocityY))

currentSecond = 1
showedPoints = True
while True:
    if showedPoints:
        choice = input("(n)ext or (q)uit: ")
    else:
        choice = "n"

    if choice == "q":
        print(f"{currentSecond - 1} seconds")
        break
    if choice == "n":
        currentPoints = [pol.afterSeconds(currentSecond)
                         for pol in pointsOfLight]
        showedPoints = showPoints(currentPoints)
        currentSecond += 1
