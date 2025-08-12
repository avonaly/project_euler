def first_digits_of_sum(addends):       # takes list of constant length addends and returns first 10 digits of sum
    return str(sum([int(str(x)[:11]) for x in addends]))[:10]


n = int(input())
numbers = [int(input()) for _ in range(n)]
print(first_digits_of_sum(numbers))