import math

DEBUG = True


SIEVE_UP_TO = 120000


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


def main():
    is_prime = create_prime_sieve(SIEVE_UP_TO)
    primes = [n for n in range(120000) if is_prime(n)]

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(primes[n-1])


main()
