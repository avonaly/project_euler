import math

DEBUG = False
BENCH = False


def create_prime_sieve(upper_bound: int):
    sieve = bytearray([True]) * ((upper_bound + 1) // 2)
    sieve[0] = False

    for p in range(1, math.isqrt(upper_bound) + 1, 2):
        if sieve[p // 2]:
            sieve[(p * p) // 2 :: p] = bytearray(
                len(range((p * p) // 2, (upper_bound + 1) // 2, p))
            )

    def is_prime(n: int):
        if n % 2 == 0:
            return n == 2
        else:
            return bool(sieve[n // 2])

    return is_prime


def build_solver():
    MAX_I = 80_000
    SIEVE_UP_TO = 10 ** 8

    is_prime = create_prime_sieve(SIEVE_UP_TO)

    solutions = [1, 2]  # handle base cases manually
    k = 2  # current ring
    while len(solutions) <= MAX_I:
        # first on ring
        if all(map(is_prime, (6 * k - 1, 6 * k + 1, 12 * k + 5))):
            solutions.append(3 * k * (k - 1) + 2)
        # last on ring
        if all(map(is_prime, (6 * k - 1, 6 * k + 5, 12 * k - 7))):
            solutions.append(3 * k * (k + 1) + 1)

        k += 1

    def solve(k: int):
        return solutions[k - 1]

    return solve


def main():
    solve = build_solver()

    t = int(input())
    for _ in range(t):
        k = int(input())
        print(solve(k))


if BENCH:
    from timeit import timeit

    def bench_build_solver():
        build_solver()

    def bench_sieve():
        SIEVE_TO = 10**8
        create_prime_sieve(SIEVE_TO)

    time = timeit(bench_sieve, number=1)
    print(f"It took {time:.4f} to build the sieve.")
else:
    main()
