"""
For this one I decided not to implement the VM but instead translate it
to the equivalent Python program.
"""

from re import A


if __name__ == '__main__':
    a = 1
    b = 1
    for _ in range(26):
        # This is the Fibonacci sequence.
        c = a
        a += b
        b = c
    a += 19 * 11
    print(f"Part 1: {a}")

    a = 1
    b = 1
    for _ in range(33):
        c = a
        a += b
        b = c
    a += 19 * 11
    print(f"Part 2: {a}")
