import itertools


DEBUG = False

MAX_SUM_SQUARE_DIG = 200 * 9**2
SOL_REDUCE = 10**9 + 7


def build_ending_state_array():
    # returns an array where array[n] stores the ending num of the chain starting from n
    end_states: list[int] = [0] * (MAX_SUM_SQUARE_DIG + 1)
    # end_states[n] == end state of chain from n
    end_states[1], end_states[89] = 1, 89
    # initialise with known exhaustive end states

    # build the end states iteratively for each n
    for n in range(1, MAX_SUM_SQUARE_DIG + 1):
        chain_from_n: list[int] = list()
        cur_num = n

        # search through sequence until we hit cached result
        while end_states[cur_num] == 0:
            # while we don't know the end state of the current number
            chain_from_n.append(cur_num)
            # add it to the chain
            cur_num = sum(int(d) ** 2 for d in str(cur_num))
            # find the next number in sequence

        # update end states of all nums in the chain
        end_state = end_states[cur_num]
        for k in chain_from_n:
            end_states[k] = end_state

    return end_states


def build_sums_tally(max_num_len: int):
    # build array up to max possible digit square sum
    max_sum_square_dig = max_num_len * 9**2

    # store the tally of numbers with a dig sq sum of n at dig_sq_sum_tally[n]
    dig_sq_sum_tally = [0] * (max_sum_square_dig + 1)
    # initialise with 0 and 1 digit cases
    for k in range(10):
        dig_sq_sum_tally[k**2] += 1
    tally_update = [0] * (max_sum_square_dig + 1)

    # for each length of number (in base 10)
    for _ in range(2, max_num_len + 1):
        # for each possible digit added in front of an existing number
        for new_first_dig in range(1, 10):
            # for each existing tally of numbers with sum n
            for n, count in enumerate(dig_sq_sum_tally):
                # if the count is nonzero
                if count:
                    # increment the corresponding tally of the sum after adding the new digit
                    tally_update[n + new_first_dig**2] += count

        # update the tally with the aggregate counts of the new number length
        dig_sq_sum_tally[:] = map(sum, zip(dig_sq_sum_tally, tally_update))
        # clear the update cache
        tally_update[:] = itertools.repeat(0, max_sum_square_dig + 1)

    return dig_sq_sum_tally


def solve(digit_count: int):
    digit_sq_sum_tally = build_sums_tally(digit_count)
    end_states = build_ending_state_array()

    sol_count = sum(
        tally
        for tally, end_state in zip(digit_sq_sum_tally, end_states)
        if end_state == 89
    )
    if DEBUG:
        print(f"Total tally is {sum(digit_sq_sum_tally)}")
    return sol_count % SOL_REDUCE


def main():
    k = int(input().strip())
    print(solve(k))


if DEBUG:
    main()
else:
    main()
