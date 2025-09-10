import math

DEBUG = False
BENCH = True

SOL_REDUCE = 10**9 + 7


def solve(num_digits: int):
    increasing = math.comb(num_digits + 9, 9) - 1
    decreasing = math.comb(num_digits + 10, 10) - num_digits - 1
    both = 9 * num_digits
    return increasing + decreasing - both


def main():
    t = int(input().strip())
    for _ in range(t):
        n = int(input())
        print(solve(n) % SOL_REDUCE)


if BENCH:
    import timeit
    import random

    def bench_solve():
        for _ in range(1000):
            solve(random.randint(10**4, 10**5))

    total_time = timeit.timeit(bench_solve, number=1)
    print(f"It took {total_time:.4f} seconds to run 1000 iterations of solve.")
else:
    main()
