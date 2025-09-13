from collections.abc import Iterable
from collections import Counter
import math
import random


DEBUG = False
BENCH = False


N_UP_TO = 10**18
# bases valid for u64
MILLER_RABIN_BASES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
MILLER_RABIN_PRIMES = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)


def is_prime(
    n: int,
    bases: Iterable[int] = MILLER_RABIN_BASES,
    low_primes: Iterable[int] = MILLER_RABIN_PRIMES,
):
    """
    Uses fast primality testing per the spec described at https://t5k.org/prove/prove2_3.html
    With default bases & trial primes, the test is valid and fast up to u32 range.
    """
    if n < 2:
        return False
    elif n in bases:
        return True

    # opportunistically test common prime factors
    for prime in low_primes:
        if n % prime == 0:
            return n == prime

    # Write n-1 as 2^s * d
    d = n - 1
    s = (d & -d).bit_length() - 1
    d >>= s

    # test each base
    for a in bases:
        x = pow(a, d, n)

        if x == 1 or x == n - 1:
            continue  # probable prime for base a, move to the next base

        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break  # probable prime for base a, move to the next base
        else:
            return False  # both tests failed, x is composite

    # all bases pass, n is prime given the precomputed valid bound
    return True


def pollard_rho(n: int):
    if n % 2 == 0:
        return 2
    if n % 3 == 0:
        return 3
    while True:
        x = random.randrange(2, n - 1)
        y = x
        c = random.randrange(1, n - 1)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = math.gcd(abs(x - y), n)
        if d != n:
            return d


def factorize(n: int) -> Counter[int]:
    def factor(n: int, factors_of_n: Counter[int]):
        if n == 1:
            return
        if is_prime(n):
            factors_of_n[n] += 1
            return
        d = pollard_rho(n)
        factor(d, factors_of_n)
        factor(n // d, factors_of_n)

    factors = Counter()
    factor(n, factors)
    return factors


def solve(n: int):
    factors = factorize(n)
    square_div_count = 1
    for exp in factors.values():
        square_div_count *= 2 * exp + 1
    return (square_div_count + 1) // 2


def main():
    t = int(input())
    for _ in range(t):
        n = int(input())
        print(solve(n))


if BENCH:
    pass
else:
    main()
