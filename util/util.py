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
    primes: typing.Iterable[int] = [3, 5, 7, 11, 13, 17, 19],
):
    """
    Uses fast primality testing per the spec described at https://t5k.org/prove/prove2_3.html
    With default bases, the test is valid up to u32 range.
    """
    if n < 2:
        return False
    elif n in bases or n in primes:
        return True

    # opportunistically test low primes
    if any(n % prime == 0 for prime in primes):
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


def digits_of(n: int):  # obsolete
    """
    yields base-10 digits of n from least sig fig up
    """
    if n == 0:
        yield 0

    n_rem = abs(n)  # remaining digits
    while n_rem > 0:
        a, b = divmod(n_rem, 10)
        n_rem = a
        yield b
    # return the next digit per call


def index_of_greatest_element_less_than(
    sorted_seq: typing.Sequence[int], upper_bound: int
):  # obsolete
    """
    Returns the index of the maximum value in sorted_seq less than upper_bound.

    Implements naive search
    """

    a, b = -1, len(sorted_seq)
    while a + 1 < b:
        m = (a + b) // 2
        if sorted_seq[m] < upper_bound:
            a = m
        else:
            b = m

    return a


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


def pwr_residue(base: int, exponent: int, modulus: int):  # obsolete
    """
    Returns the residue after exponentiation. Does not support negative bases or powers, or modulo 1.

    Implementation progressively exponentiates by two, increasing exponent by one if required, until exponent reaches desired value.
    """

    base %= modulus
    residue = 1

    while exponent > 0:
        if exponent & 1:
            residue = residue * base % modulus
        base = base**2 % modulus
        exponent = exponent >> 1

    return residue
