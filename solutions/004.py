def prime_sieve(upper_bound: int):
    candidates = [True for _ in range(upper_bound)]
    for p in range(2, upper_bound):
        if candidates[p]:
            for n in range(2 * p, upper_bound, p):
                candidates[n] = False

    return tuple(i for i, n in enumerate(candidates) if n and i >= 2)


def find_valid_palindromes():
    valid_palindromes: list[int] = []
    for j in range(100, 1000):
        for k in range(j, 1000):
            s = str(j * k)
            if s == s[::-1]:
                valid_palindromes.append(int(s))
    valid_palindromes.sort()
    return valid_palindromes


def main():
    valid_palindromes = find_valid_palindromes()

    t = int(input().strip())
    for _ in range(t):
        n = int(input().strip())

        high_palindrome = 0
        for m in valid_palindromes:
            if m >= n:
                break
            high_palindrome = m

        print(high_palindrome)


main()
