
DEBUG = True


def pwr_residue(base: int, exponent: int, modulus: int):
    """
    Returns the residue after exponentiation. Does not support negative bases or powers, or modulo 1.
    
    Implementation progressively exponentiates by two, adding one if required, until exponent reaches desired value.
    """

    base %= modulus
    residue = 1

    while exponent > 0:
        if exponent & 1:
            residue = residue * base % modulus
        base = base**2 % modulus
        exponent = exponent >> 1
    
    return residue


def build_series(upper_bound: int):
    NUM_OF_DIGITS = 10**10
    residue_sequence = [pwr_residue(n, n, NUM_OF_DIGITS) for n in range(1,upper_bound+1)]
    residue_series = [1] * upper_bound
    for i in range(1,upper_bound):
        residue_series[i] = (residue_series[i-1] + residue_sequence[i]) - NUM_OF_DIGITS * ((residue_series[i-1] + residue_sequence[i]) >= NUM_OF_DIGITS)
    if DEBUG: 
        print(f"The lengths of the lists are {len(residue_sequence),len(residue_series)}")
    return residue_series


def main():
    n = int(input().strip())
    print(build_series(n)[n-1])


if DEBUG: 
    main()
else: 
    main()
