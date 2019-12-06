import re
from collections import defaultdict
from generic_search import bfsAll
from typing import List
from pprint import pprint

distanceRegex = re.compile(r"(.+) to (.+) = (\d+)")


class Distance:
    def __init__(self, origin, destination, distance):
        self.origin = origin
        self.destination = destination
        self.distance = distance

    def __repr__(self):
        return f"Distance({self.origin}, {self.destination}, {self.distance}"

    def __str__(self):
        return f"{self.origin} to {self.destination} = {self.distance}"


class Path:
    def __init__(self, locations, distances):
        self.locations = locations
        self.distances = distances
        self.shortest = None

    def completePath(self, candidate: List[str]):
        return len(candidate) == len(self.locations)

    def successors(self, candidate: List[str]):
        return (candidate + (d.destination, )
                for d in self.distances[candidate[-1]]
                if d.destination not in candidate)

    def totalDistance(self, route):
        """
        Return the total distance in the given route
        """
        total = 0
        for i in range(len(route) - 1):
            total += self.distanceToLast(route[i:i+2], None)
        return total

    def distanceToLast(self,
                       candidate: List[str],
                       previousCandidate: List[str]):
        """
		Cost function for astar
		
		Keyword arguments
		candidate -- The current route. Return the distance from the penultimate to last location in this route.
		previousCandidate -- The previous route. This is just the current route without the last location so we don't really need it
		"""
        distance = [
            d.distance for d in self.distances[candidate[-2]]
            if d.destination == candidate[-1]
        ]
        if len(distance) != 1:
            raise ValueError(
                "DistanceToLast found something other than one distance.")
        return distance[0]

    def heurstic(self, candidate):
        return len(self.locations) - len(candidate)


def day9(fileName):
    distances = defaultdict(list)
    locations = set()

    with open(fileName) as infile:
        for line in infile:
            match = distanceRegex.match(line)
            if match:
                distances[match[1]].append(
                    Distance(match[1], match[2], int(match[3])))
                distances[match[2]].append(
                    Distance(match[2], match[1], int(match[3])))
                locations.add(match[1])
                locations.add(match[2])
            else:
                raise ValueError(f"Couldn't match line: {line}")

    path = Path(locations, distances)
    routes = bfsAll(((loc,) for loc in locations), path.completePath, path.successors)
    shortestDistance = 1e6
    longestDistance = 0
    routeCount = 0
    for route in routes:
        routeCount += 1
        routeDistance = path.totalDistance(route.state)
        shortestDistance = min(shortestDistance, routeDistance)
        longestDistance = max(longestDistance, routeDistance)
    print(f"{routeCount} routes found")
    return shortestDistance, longestDistance


shortest, longest = day9("9.txt")
print(shortest)
print(longest)
# 719 is too high
# 213 is too high
