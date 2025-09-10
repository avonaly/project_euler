from collections.abc import Sequence

DEBUG = False

type Matrix[T] = Sequence[Sequence[T]]


def matmul_mod(A: Matrix[int], B: Matrix[int], mod: int | None = None):
    B_transpose = tuple(zip(*B))
    result: Matrix[int] = []
    for row in A:
        new_row: list[int] = []
        for col in B_transpose:
            s = sum(x * y for x, y in zip(row, col))
            new_row.append(s % mod if mod is not None else s)
        result.append(new_row)
    return result


def matexp(
    A: Matrix[int],
    pwr: int,
    mod: int | None = None,
):
    dim = len(A)
    base = A
    # initialise result as identity matrix
    result: Matrix[int] = [[int(i == j) for j in range(dim)] for i in range(dim)]

    while pwr > 0:
        if pwr & 1:
            result = matmul_mod(result, base, mod)

        base = matmul_mod(base, base, mod)
        pwr >>= 1

    return result


def build_solver():
    RED = [[1, 1], [1, 0]]
    RED_INIT = [[2], [1]]
    GREEN = [[1, 0, 1], [1, 0, 0], [0, 1, 0]]
    GREEN_INIT = [[2], [1], [1]]
    BLUE = [[1, 0, 0, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    BLUE_INIT = [[2], [1], [1], [1]]

    SOL_REDUCE = 10**9 + 7

    def solve(n: int):
        red_state_vec = matmul_mod(
            matexp(RED, n - 1, SOL_REDUCE),
            RED_INIT,
        )
        green_state_vec = matmul_mod(
            matexp(GREEN, n - 1, SOL_REDUCE),
            GREEN_INIT,
        )
        blue_state_vec = matmul_mod(
            matexp(BLUE, n - 1, SOL_REDUCE),
            BLUE_INIT,
        )

        total_count = (
            red_state_vec[1][0] + green_state_vec[2][0] + blue_state_vec[3][0] - 3
        ) % SOL_REDUCE

        return total_count

    return solve


def main():
    solve = build_solver()

    t = int(input())
    for _ in range(t):
        n = int(input())
        print(solve(n))


if __name__ == "__main__":
    main()
