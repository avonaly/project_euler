

def acc_multiples(upper_bound):
    accumulate = 0

    a0 = (upper_bound-1) // 3
    accumulate += 3 * (a0 * (a0+1) // 2)

    a1 = (upper_bound-1) // 5
    accumulate += 5 * (a1 * (a1+1) // 2)

    a2 = (upper_bound-1) // 15
    accumulate -= 15 * (a2 * (a2+1) // 2)

    return accumulate


def main():
    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())
        print(acc_multiples(n))


main()
