from array import array
from timeit import timeit


DEBUG = False


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
        # gives the divisor count of n, by calculating the exponent of 2 and looking up the divisor count of the corresponding odd integer
        exp_of_2_plus_1 = (n & -n).bit_length()
        # finds how many 2's go into n
        return self._odd_div_counts[n >> exp_of_2_plus_1] * exp_of_2_plus_1
        # looks up num of divisors of (n without the 2's) and multiply by num of divisors of power of 2
        # a bit hacky here but makes sense


def main():
    MAX_DIVISORS = 1000
    UPPER_BOUND = 2**20
    # guess for up to what n we'll need to know divisor counts for

    divisor_count = DivisorCount(UPPER_BOUND)

    solutions = array("L", [0] * (MAX_DIVISORS + 1))
    # we intend for solutions[n] == m where the mth triangular number is the smallest triangular number to have more than n divisors
    working_max_divs = 1  # the divisor count we are currently working on
    n = 1  # the index of the triangular number we are up to

    while True:
        # sequentially test triangular numbers
        if n % 2 == 0:
            num_divs = divisor_count(n // 2) * divisor_count(n + 1)
        else:
            num_divs = divisor_count(n) * divisor_count((n + 1) // 2)
        # finds the number of divisors of the nth triangular number

        if num_divs > working_max_divs:
            # if the current divisor count is better than what we have so far
            if num_divs > MAX_DIVISORS:
                for i in range(working_max_divs, MAX_DIVISORS+1):
                    solutions[i] = n
                break
            # check if we've hit the upper bound and exit

            for i in range(working_max_divs, num_divs):
                solutions[i] = n
            working_max_divs = num_divs
            # update our solutions & the divisor count being worked

        n += 1

    num_test_cases = int(input().strip())
    for _ in range(num_test_cases):
        n = int(input().strip())
        m = solutions[n]
        print((m * (m + 1)) // 2)


if DEBUG:
    BENCH_UPPER_BOUND = 2**24
    TEST_DIVISOR_COUNT = 301592
    print(
        f"Building the divisor count up to {BENCH_UPPER_BOUND} took {timeit(lambda: DivisorCount(BENCH_UPPER_BOUND), number=1)} seconds."
    )
    print(f"The number of divisors of {TEST_DIVISOR_COUNT} is {DivisorCount(TEST_DIVISOR_COUNT+1)(TEST_DIVISOR_COUNT)}")
else:
    main()
