import random
import math


def prime_test(N, k):
    # This is the main function connected to the Test button. You don't need to touch it.
    return run_fermat(N,k), run_miller_rabin(N,k)


def mod_exp(x, y, N):
    # You will need to implement this function and change the return value.
    if y == 0:
        return 1, False, False

    z, negative_one, first_non_one = mod_exp(x,math.floor(y/2), N)

    if not first_non_one:
        if z % N != -1:
            if z % N == 1:
                if y % 2 == 0:return (math.pow(z, 2) % N), negative_one, first_non_one
                else: return (x * math.pow(z, 2) % N), negative_one, first_non_one
            else:
                first_non_one = True
                if y % 2 == 0:return (math.pow(z, 2) % N), negative_one, first_non_one
                else: return (x * math.pow(z, 2) % N), negative_one, first_non_one


        first_non_one = True
        negative_one = True
        if y % 2 == 0: return (math.pow(z, 2) % N), negative_one, first_non_one
        else: return (x * math.pow(z, 2) % N), negative_one, first_non_one

    if y % 2 == 0: return (math.pow(z, 2) % N), negative_one, first_non_one
    else: return (x * math.pow(z, 2) % N), negative_one, first_non_one

def fprobability(k):
    return math.pow((1/2), k)


def mprobability(k):
    return math.pow((1/2), k)


def run_fermat(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.

    numbers = []
    for i in range(k):
        num = random.randint(1,N-1)
        if num not in numbers:
            numbers.append(num)
        else:
            # Prevents testing the same numbers
            while True:
                num = random.randint(1, N - 1)
                if num not in numbers:
                    numbers.append(num)
                    break
        total, _, __ = mod_exp(num, N-1, N)
        if total % N == 1:
            continue

        return 'composite'

    return 'prime'


def run_miller_rabin(N,k):
    # You will need to implement this function and change the return value, which should be
    # either 'prime' or 'composite'.
    #
    # To generate random values for a, you will most likley want to use
    # random.randint(low,hi) which gives a random integer between low and
    #  hi, inclusive.

    numbers = []
    for i in range(k):
        num = random.randint(1,N-1)
        if num not in numbers:
            numbers.append(num)
        else:
            # Prevents testing the same numbers
            while True:
                num = random.randint(1, N - 1)
                if num not in numbers:
                    numbers.append(num)
                    break

        total, negative_one, first_non_one = mod_exp(num, N - 1, N)

        if total % N == 1:
            continue

        # Checks if there was a non-1 value and if it was -1 % N
        if first_non_one and negative_one:
            continue

        return 'composite'


    return 'prime'
