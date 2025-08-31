import math

DEBUG = True


UPPER_BOUND = 3000


def build_solutions():
    MAX_LEN = UPPER_BOUND // 2
    solutions: tuple[list[int], ...] = tuple(list() for _ in range(UPPER_BOUND + 1))

    for a in range(1, MAX_LEN + 1):
        for b in range(a, MAX_LEN + 1):
            n = a**2 + b**2
            c = math.isqrt(n)
            if c**2 == n and a + b + c <= UPPER_BOUND:
                solutions[a + b + c].append(a * b * c)

    best_solutions = [max(triples, default=-1) for triples in solutions]

    return best_solutions


def main():
    sol = build_solutions()

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(sol[n])


main()
