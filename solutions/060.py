import math
from typing import Iterable

# debugging, comment out for final
""" import timeit
import sys """

Subgraph = tuple[int, ...]
CompleteSubgraphMap = dict[int, tuple[list[Subgraph], ...]]

DEBUG = True


def miller_rabin(
    n: int,
    bases: Iterable[int] = [2, 7, 61],
    low_primes: Iterable[int] = [3, 5, 7, 11, 13, 17, 19],
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
    max_prime, target_sg_size = map(int, input().split())
    SIEVE_UP_TO = 20000

    prime_sieve = create_prime_sieve(SIEVE_UP_TO)
    primes_str = tuple(str(n) for n in range(max_prime + 1) if prime_sieve(n))
    num_vertices = len(primes_str)
    # consider primes as vertices of a graph
    # we intend that two primes will be connected by an edge
    # if appending them to each other in either order results in a prime

    edges: tuple[set[int], ...] = tuple(set() for _ in range(num_vertices))
    # edges[i] stores the **lesser** indices of primes connected to vertices[i]
    for v1 in range(num_vertices):
        for v2 in range(v1):
            n1, n2 = (
                int(primes_str[v2] + primes_str[v1]),
                int(primes_str[v1] + primes_str[v2]),
            )
            if miller_rabin(n1) and miller_rabin(n2):
                edges[v1].add(v2)
    primes = tuple(map(int, primes_str))

    # complete_subgraphs[k][v] will store all complete subgraphs (cliques) of size k
    # where v is the vertex with the largest index in the subgraph.
    # The other vertices in the subgraph are stored as a tuple.
    complete_subgraphs: CompleteSubgraphMap = dict()

    # we will create the complete subgraphs iteratively
    # we build the p=3 case separately to initialise
    complete_subgraphs[3] = tuple(list() for _ in range(num_vertices))
    for v_greatest in range(num_vertices):
        for v2 in edges[v_greatest]:
            for v3 in edges[v2]:
                if v3 in edges[v_greatest]:
                    complete_subgraphs[3][v_greatest].append((v2, v3))

    for target_sg_size in range(4, target_sg_size + 1):
        complete_subgraphs[target_sg_size] = tuple(list() for _ in range(num_vertices))
        for v_greatest in range(num_vertices):
            for v2 in edges[v_greatest]:
                for sg in complete_subgraphs[target_sg_size - 1][v2]:
                    if all((v3 in edges[v_greatest]) for v3 in sg):
                        complete_subgraphs[target_sg_size][v_greatest].append((v2, *sg))

    subgraph_sums = [
        sum(primes[v] for v in (v1, *sg))
        for v1, list_of_sgs in enumerate(complete_subgraphs[target_sg_size])
        for sg in list_of_sgs
    ]
    subgraph_sums.sort()

    for s in subgraph_sums:
        print(s)


main()
