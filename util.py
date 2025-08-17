
import typing


def primes_less_than(upper_bound: int):
    """
    Returns a tuple with prime numbers exclusive less than upper_bound

    Uses naive elimination method
    """

    candidates = [True for _ in range(upper_bound)]
    for p in range(2,upper_bound):
        if candidates[p]:
            for n in range(2*p,upper_bound, p):
                candidates[n] = False

    return tuple(i for i,n in enumerate(candidates) if n and i>=2)


def index_of_greatest_element_less_than(sorted_seq: typing.Sequence[int], upper_bound: int):
    """
    Returns the index of the maximum value in sorted_seq less than upper_bound.

    Implements naive search
    """

    a, b = -1, len(sorted_seq)
    while a+1 < b:
        m = (a+b) // 2
        if sorted_seq[m] < upper_bound:
            a=m
        else:
            b=m

    return a


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
