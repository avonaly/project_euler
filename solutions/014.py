from array import array
from typing import Sequence
import bisect


DEBUG = True


def rolling_max(seq: Sequence[int]) -> list[int]:
    max_indices = list()
    latest_max = 0

    for idx, value in enumerate(seq):
        if value >= latest_max:
            max_indices.append(idx)
            latest_max = value

    return max_indices


def build_collatz_sequence_lengths(upper_bound: int):
    seq_lens: array[int] = array("H", [0]) * (40 * upper_bound)
    # seq_lens[n] will store the Collatz length of n
    cache_size: int = len(seq_lens)
    seq_lens[1] = 1

    # build seq_lens up to upper bound, relying opportunistically on known results
    for starting_term in range(2, upper_bound + 1):
        seq = [starting_term]
        latest_term = starting_term
        # follow the sequence until we find a known Collatz length
        while latest_term >= cache_size or seq_lens[latest_term] == 0:
            if latest_term % 2 == 0:
                latest_term //= 2
            else:
                latest_term = 3 * latest_term + 1
            seq.append(latest_term)

        # add all discovered lengths to the cache
        known_len = seq_lens[latest_term]
        for path_len, n in enumerate(reversed(seq)):
            if n < cache_size:
                seq_lens[n] = known_len + path_len

    return seq_lens[: upper_bound + 1]


def build_solver():
    UPPER_BOUND = 5 * 10**6
    seq_lens = build_collatz_sequence_lengths(UPPER_BOUND)
    max_len_starting_terms = rolling_max(seq_lens)

    def solve(n: int):
        idx = bisect.bisect_right(max_len_starting_terms, n)
        return max_len_starting_terms[idx - 1]

    return solve


def main():
    solve = build_solver()

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(solve(n))


main()
