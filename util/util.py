import typing
from array import array
import math
import timeit


DEBUG = True


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


def miller_rabin(
    n: int,
    bases: typing.Iterable[int] = [2, 7, 61],
    low_primes: typing.Iterable[int] = [3, 5, 7, 11, 13, 17, 19],
):
    """
    Uses fast primality testing per the spec described at https://t5k.org/prove/prove2_3.html
    With default bases, the test is valid up to u32 range.
    With default primes this test is unnecessarily slow for even numbers.
    """
    if n < 2:
        return False
    elif n in bases:
        return True

    # opportunistically test common prime factors
    if any(n % prime == 0 for prime in low_primes):
        return False

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


def create_divisor_counter(upper_bound: int):
    size = upper_bound // 2

    odd_div_counts = array("H", [1] * size)
    # build an array of the divisor counts of odd integers on initialisation
    # we eventually want _odd_div_counts[k] == the divisor count of 2k+1
    for k in range(1, size):
        # for all integers 2k+1
        for m in range(k, size, 2 * k + 1):
            odd_div_counts[m] += 1
        # increment the divisor counter for all (odd) multiples of 2k+1

    def divisor_count(n: int):
        # gives the divisor count of n, by calculating the exponent of 2 in constant time and looking up the divisor count of the corresponding odd integer
        exp_of_2_plus_1 = (n & -n).bit_length()
        # finds how many 2's go into n
        return odd_div_counts[n >> exp_of_2_plus_1] * exp_of_2_plus_1
        # looks up num of divisors of (n without the 2's) and multiply by num of divisors of power of 2
        # a bit hacky here but makes sense

    return divisor_count
