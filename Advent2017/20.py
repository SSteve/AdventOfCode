import math
import re
from collections import namedtuple

particleRegex = re.compile(r"p=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, v=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>, a=<\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)>")

Point3d = namedtuple('Point3d', ['x', 'y', 'z'])


def quadraticRoots(a, b, c):
    if a == 0:
        # When a is zero, this is a linear equation, not quadratic
        if b == 0:
            # This is a point
            return (c,)
        return (-c / b,)
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    if discriminant == 0:
        return (-b / (2 * a),)
    discriminantSqrt = math.sqrt(discriminant)
    return ((-b + discriminantSqrt) / (2 * a), (-b - discriminantSqrt) / (2 * a))


class Point(Point3d):
    def distance(self):
        return int(abs(self.x) + abs(self.y) + abs(self.z))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """
        Multiply a point by a scalar
        """
        return Point(self.x * other, self.y * other, self.z * other)


class Particle:
    def __init__(self, pX, pY, pZ, vX, vY, vZ, aX, aY, aZ):
        self.position = Point(pX, pY, pZ)
        self.velocity = Point(vX, vY, vZ)
        self.acceleration = Point(aX, aY, aZ)

    def distance(self):
        return self.position.distance()

    def atTime(self, t):
        """
        Calculate the particle's position at time t
        """
        return self.position + self.velocity * t + self.acceleration * t**2

    def willCollide(self, other):
        """
        Solve quadratic equation for each dimension and if the times match, the points will collide.
        """
        # Get differences. Use discreet versions from Reddit
        a = (other.acceleration - self.acceleration) * 0.5
        b = a + (other.velocity - self.velocity)
        c = other.position - self.position
        roots = []
        xStatic = a.x == 0 and b.x == 0 and c.x == 0
        if not xStatic:
            rootsX = [round(root, 3) for root in quadraticRoots(a.x, b.x, c.x) if root >= 0]
            if not rootsX:
                return False
            roots.append(rootsX)
        yStatic = a.y == 0 and b.y == 0 and c.y == 0
        if not yStatic:
            rootsY = [round(root, 3) for root in quadraticRoots(a.y, b.y, c.y) if root >= 0]
            if not rootsY:
                return False
            roots.append(rootsY)
        zStatic = a.z == 0 and b.z == 0 and c.z == 0
        if not zStatic:
            rootsZ = [round(root, 3) for root in quadraticRoots(a.z, b.z, c.z) if root >= 0]
            if not rootsZ:
                return False
            roots.append(rootsZ)
        if xStatic and yStatic and zStatic:
            return True
        commonRoots = set(roots.pop())
        while roots:
            commonRoots &= set(roots.pop())
        return len(commonRoots) > 0


def day20(fileName):
    particles = []
    with open(fileName) as infile:
        for line in infile:
            match = particleRegex.match(line)
            if match:
                args = []
                for groupNum in range(1, 10):
                    args.append(int(match.group(groupNum)))
                particles.append(Particle(*args))
    particleDistances = [p.atTime(1e6).distance() for p in particles]
    minParticleIndex = 0
    minParticleDistance = particleDistances[0]
    for inx, distance in enumerate(particleDistances):
        if distance < minParticleDistance:
            minParticleIndex = inx
            minParticleDistance = distance
    toRemove = set()
    for inx1, particle in enumerate(particles):
        for inx2 in range(inx1 + 1, len(particles)):
            particle2 = particles[inx2]
            if particle in toRemove and particle2 in toRemove:
                continue
            if particle.willCollide(particle2):
                toRemove.update([particle, particle2])
    remainingParticles = set(particles) - toRemove

    return minParticleIndex, len(remainingParticles)


if __name__ == "__main__":
    inx, particleCount = day20("20.txt")
    print(f"Particle {inx} will stay closest")
    print(f"{particleCount} particles remain")
    # 83 is wrong
