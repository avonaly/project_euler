import typing
from array import array
import math


DEBUG = True


def primes_less_than(upper_bound: int):
    """
    Returns an array with prime numbers less than upper_bound

    Uses naive elimination method
    """
    if upper_bound < 3:
        return array("L")

    candidates = bytearray([1]) * upper_bound
    candidates[0] = candidates[1] = False

    for p in range(math.isqrt(upper_bound) + 1):
        if candidates[p]:
            candidates[p * p :: p] = bytearray(len(range(p * p, upper_bound, p)))

    return array("L", (i for i, is_prime in enumerate(candidates) if is_prime))


def digits_of(n: int):
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
):
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


class DivisorCount:
    def __init__(self, upper_bound: int):
        size = upper_bound // 2

        self._odd_div_counts = array("H", [1] * size)
        # build an array of the divisor counts of odd integers on initialisation
        # we eventually want _odd_div_counts[k] == the divisor count of 2k+1
        for k in range(1, size):
            # for all integers 2k+1
            for m in range(k, size, 2 * k + 1):
                self._odd_div_counts[m] += 1
            # increment the divisor counter for all (odd) multiples of 2k+1

    def __call__(self, n: int):
        # gives the divisor count of n, by calculating the exponent of 2 in constant time and looking up the divisor count of the corresponding odd integer
        exp_of_2_plus_1 = (n & -n).bit_length()
        # finds how many 2's go into n
        return self._odd_div_counts[n >> exp_of_2_plus_1] * exp_of_2_plus_1
        # looks up num of divisors of (n without the 2's) and multiply by num of divisors of power of 2
        # a bit hacky here but makes sense


def pwr_residue(base: int, exponent: int, modulus: int):
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
