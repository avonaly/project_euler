from array import array
import sys


DEBUG = True


def build_solver():
    MAX_DIGIT_COUNT = 5000
    sys.set_int_max_str_digits(MAX_DIGIT_COUNT)

    digit_counts = array("H", [0]) * (MAX_DIGIT_COUNT + 1)
    latest_digit_count, fibo_term = 0, 1
    a, b = 0, 1

    while latest_digit_count < MAX_DIGIT_COUNT:
        num_digits = len(str(b))
        if num_digits > latest_digit_count:
            digit_counts[num_digits] = fibo_term
            latest_digit_count = num_digits

        a, b = b, a + b
        fibo_term += 1

    def solve(n: int):
        return digit_counts[n]

    return solve


def main():
    solve = build_solver()

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(solve(n))


main()
