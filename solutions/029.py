import math
from array import array

DEBUG = True


def main():
    upper_bound = int(input().strip())
    MAX_N = 10**5

    power_sieve = array("B", [1]) * (upper_bound + 1)
    power_sieve[0] = power_sieve[1] = 0
    # initialise power sieve as True, less 0 and 1
    # we intend eventually for there to be no two True indices i and j such that there exists integer i^a == j^b
    duplicate_count = array("B", [1]) * (upper_bound + 1)
    # we intend duplicate_count[n] == number of powers of n <= upper_bound

    for n in range(math.isqrt(upper_bound) + 1):
        if power_sieve[n]:
            # for each unique base in power sieve
            working_power_of_n = n * n
            # incrementally remove all of its powers
            while working_power_of_n <= upper_bound:
                power_sieve[working_power_of_n] = 0
                duplicate_count[n] += 1  # tally the number of duplicate powers
                working_power_of_n *= n

    if DEBUG:
        print(
            f"""List of unique bases is {
                [
                    (b, count)
                    for b, (is_unique, count) in enumerate(
                        zip(power_sieve, duplicate_count)
                    )
                    if is_unique
                ]
            }"""
        )

    # we have all the unique bases and the duplication factor for each
    # each unique base contributes independently to the final sequence
    # the number of contributions per base is determined by the duplication factor
    # we now find the relationship for up to the highest dup factor possible given MAX_N

    MAX_DUP_FACTOR = int(math.log(MAX_N, 2))
    contribution = array("L", [0]) * (MAX_DUP_FACTOR + 1)
    # we intend contribution[d] == contribution of a base with dup factor d
    multiples_sieve = array("B", [0]) * (upper_bound * MAX_DUP_FACTOR + 1)
    # incrementally build boolean sieve of multiples of the power
    # after each duplication factor is multiplied through the sieve, we count the num of entries

    for duped in range(1, MAX_DUP_FACTOR + 1):
        for n in range(2, upper_bound + 1):
            multiples_sieve[duped * n] = 1
        contribution[duped] = sum(multiples_sieve)

    if DEBUG:
        print(f"The contributions array looks like {contribution}")

    print(
        sum(
            is_unique * contribution[d]
            for is_unique, d in zip(power_sieve, duplicate_count)
        )
    )


if DEBUG:
    main()
else:
    main()
