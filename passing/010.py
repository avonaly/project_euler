
def prime_sieve(upper_bound: int):
    """
    Returns a tuple with prime numbers exclusive less than upper_bound

    Uses naive sieve method
    """
    candidates = [True for _ in range(upper_bound)]
    for p in range(2,upper_bound):
        if candidates[p]:
            for n in range(2*p,upper_bound, p):
                candidates[n] = False

    return tuple(i for i,n in enumerate(candidates) if n and i>=2)


def greatest_element_less_than(sorted_seq, upper_bound: int):
    """
    Returns the index of the maximum value in sorted_sequence less than upper_bound.

    Implements naive search
    """

    a, b = -1, len(sorted_seq)
    while a+1 < b:
        m = (a+b) // 2
        if sorted_seq[m] < upper_bound: a=m
        else: b=m

    return a


def main():
    primes = prime_sieve(1000001)
    primes_acc = [0]
    for p in primes: primes_acc.append(primes_acc[-1] + p)

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())

        a = greatest_element_less_than(primes, n+1)
        print(primes_acc[a+1])


main()
