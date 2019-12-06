from dataclasses import dataclass
from collections import defaultdict
import re


@dataclass
class Reindeer:
    name: str
    speed: int
    flyTime: int
    restTime: int

    @property
    def cycleTime(self):
        return self.flyTime + self.restTime

    @property
    def distancePerCycle(self):
        return self.flyTime * self.speed

    def distanceAtTime(self, time):
        """
        Return the distance travelled at the given time
        """
        fullCycles, partialCycle = divmod(time, self.cycleTime)
        distance = fullCycles * self.distancePerCycle
        if partialCycle >= self.flyTime:
            distance += self.distancePerCycle
        else:
            distance += partialCycle * self.speed
        return distance


def buildPack(fileName):
    reindeerRegex = re.compile(r"(.+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds\.")
    pack = []
    with open(fileName) as infile:
        for line in infile:
            match = reindeerRegex.match(line)
            if match:
                pack.append(Reindeer(match[1], int(match[2]), int(match[3]), int(match[4])))
    return pack

def day14(fileName, seconds):
    pack = buildPack(fileName)
    furthest = (pack[0].name, pack[0].distanceAtTime(seconds))
    for reindeer in pack[1:]:
        distance = reindeer.distanceAtTime(seconds)
        if distance > furthest[1]:
            furthest = (reindeer.name, distance)
    return furthest


def day14b(fileName, seconds):
    pack = buildPack(fileName)
    scores = defaultdict(int)
    for i in range(seconds):
        distances = defaultdict(list)
        for reindeer in pack:
            distance = reindeer.distanceAtTime(i + 1)
            distances[distance].append(reindeer)
        for reindeer in distances[max(distances)]:
            scores[reindeer.name] += 1
    highScore = max(scores.values())
    winners = [reindeer for reindeer in scores if scores[reindeer] == highScore]
    return (winners[0], highScore)


name, distance = day14("14test.txt", 1000)
print(f"{name} went {distance} km")
name, distance = day14("14.txt", 2503)
print(f"{name} went {distance} km")

name, score = day14b("14test.txt", 1000)
print(f"{name} scored {score}")
name, score = day14b("14.txt", 2503)
print(f"{name} scored {score}")
