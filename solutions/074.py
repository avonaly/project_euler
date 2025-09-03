import math
from array import array
from itertools import islice


DEBUG = True


def build_chain_lengths(upper_bound: int):
    SAFE_CACHE_SIZE = 2200000

    # a number is either inside or outside a loop
    # so a chain starting from a number n always has unique nums until it enters a loop
    # at which point it does exactly one cycle
    # this means we can efficiently build a cache of the chain lengths starting from each n
    # so long as we make sure to detect and correctly fill out loops on each iteration

    chain_len = array("B", [0]) * (SAFE_CACHE_SIZE + 1)
    # chain_len[n] stores chain length of sequence starting from n

    for n in range(0, upper_bound + 1):
        chain_from_n: list[int] = [n]
        chain_index: set[int] = set(chain_from_n)
        working_num = n

        # work through the chain until either we find a cached length or we detect a loop
        while chain_len[chain_from_n[-1]] == 0:
            # find the next_term with the sum of factorials of digits calculation
            working_num = sum(math.factorial(int(digit)) for digit in str(working_num))

            # check if we've found a loop
            if working_num in chain_index:
                loop_start = chain_from_n.index(working_num)
                loop_len = len(chain_from_n) - loop_start
                # label the chain_len for all the nums inside the loop
                for k in islice(chain_from_n, loop_start, None):
                    chain_len[k] = loop_len
                # drop the loop from the chain (keeping the entry point)
                del chain_from_n[loop_start + 1 :]
                break

            # add the validated term to the chain
            chain_from_n.append(working_num)
            chain_index.add(working_num)

        cached_len = chain_len[chain_from_n[-1]]
        for k, a_k in enumerate(reversed(chain_from_n)):
            chain_len[a_k] = k + cached_len

    return chain_len[: upper_bound + 1]


def build_solver():
    MAX_N = 10**6
    chain_len_array = build_chain_lengths(MAX_N)

    def solve(chain_len: int, upper_bound: int):
        solutions = [n for n, len in enumerate(islice(chain_len_array, upper_bound + 1)) if len == chain_len]
        return solutions or [-1]

    return solve


def main():
    solve = build_solver()

    t = int(input().strip())
    for _ in range(t):
        n, len = map(int, input().split())
        print(*solve(len, n))


if DEBUG:
    main()
else:
    main()
