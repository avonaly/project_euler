from collections.abc import Sequence

DEBUG = True

type Matrix[T] = Sequence[Sequence[T]]


def matmul_mod(A: Matrix[int], B: Matrix[int], mod: int | None = None) -> Matrix[int]:
    B_transpose = tuple(zip(*B))
    result: Matrix[int] = []
    for row in A:
        new_row: list[int] = []
        for col in B_transpose:
            s = sum(x * y for x, y in zip(row, col))
            new_row.append(s % mod if mod is not None else s)
        result.append(new_row)
    return result


def matexp(A: Matrix[int], pwr: int, mod: int | None = None) -> Matrix[int]:
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
    EVOLVE = [[1, 1, 1, 1], [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
    INIT = [[8], [4], [2], [1]]

    MOD = 10**9 + 7

    def solve(n: int):
        count = matmul_mod(matexp(EVOLVE, n - 1, MOD), INIT, MOD)[-1][0]
        return count

    return solve


def main():
    solve = build_solver()

    t = int(input())
    for _ in range(t):
        n = int(input())

        print(solve(n))


if __name__ == "__main__":
    main()
