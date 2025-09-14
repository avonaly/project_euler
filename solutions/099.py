import math

DEBUG = True


def solve(base_exp_pairs: list[tuple[int, int]], pos: int):
    def value(pair: tuple[int, int]):
        base, exp = pair
        return math.log2(base) * exp

    base_exp_pairs.sort(key=value)
    return base_exp_pairs[pos - 1]


def main():
    n = int(input())
    base_exp_pairs = [tuple(map(int, input().split())) for _ in range(n)]
    k = int(input())
    print(*solve(base_exp_pairs, k))  # type: ignore


main()
