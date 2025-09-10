import timeit
import random
from typing import Iterable

DEBUG = False
BENCH = True

MOD = 10**12


def solve(cases: Iterable[Iterable[int]]):
    sum_of_cases = sum(a * pow(b, c, MOD) + d for a, b, c, d in cases)
    return str(sum_of_cases + MOD)[-12:]


def main():
    t = int(input().strip())
    n = (map(int, input().split()) for _ in range(t))
    print(solve(n))


if BENCH:

    def bench_solve():
        solve((random.randint(1, 10**9) for _ in range(4)) for _ in range(500_000))

    total_time = timeit.timeit(bench_solve, number=1)
    print(f"Total time for 500,000 iterations: {total_time:.4f} seconds")
else:
    main()
