import math
from timeit import timeit
from array import array


DEBUG = True


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


def main():
    if DEBUG:
        up_to, digit_count = UP_TO, DIGIT_COUNT
    else:
        up_to, digit_count = (int(input().strip()) for _ in range(2))

    total = 0 # running total
    for n in range(1, up_to + 1): # for all numbers up to n
        if math.isqrt(n)**2 == n:
            continue
        # skip perfect squares

        digits_of_sqrt_n = array("B", digits_of(math.isqrt(n * 10 ** (2 * digit_count))))
        # store the base-10 digits of sqrt(n) in default reverse order
        total += sum(digits_of_sqrt_n[-digit_count:])
        # add the first digit_count digits of sqrt(n) to the running total

    print(total)


if DEBUG:
    UP_TO = 1000
    DIGIT_COUNT = 1000
    print(
        f"The time it takes to calculate up to N={UP_TO} with {DIGIT_COUNT} digits is {timeit(lambda: main(), number=1)} seconds"
    )
else:
    main()
