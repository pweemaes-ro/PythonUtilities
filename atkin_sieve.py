"""Implementation of atkin_sieve for calculating primes

   A basic version accepting only an upperbound was taken from github and used as a basis for

        atkin_sieve2(*, min_prime=0, max_prime=1)

   accepting a lower- and upper limit.
   """

import math
""" Some theoretical notes about the atkin_sieve:

    THE MATH
    
    Let n be a positive integer > 3.

    Define: 
    - an integer x is a square if x == y^2 for some integer y > 1. 
    - an integer x is squarefree if x is not divisible by any square (so 54 is NOT squarefree, but 35 is).   

    Theorems:
    
    1. Let n be a squarefree positive integer of the form n = 1 + 4Z for some (positive) integer Z. 
       Then n is prime if and only if n = 4x^2 + y^2 has an odd number of solutions (x, y) for x, y positive integers.

    2. IF n is a squarefree positive integer of the form n = 7 + 12Z for some (positive) integer Z. 
       Then n is prime if and only if n = 3x^2 + y^2 has an odd number of solutions (x, y) for x, y positive integers.

    3. IF n is a squarefree positive integer of the form n = 11 + 12Z for some (positive) integer Z.
       Then n is prime if and only if n = 3x^2 - y^2 has an odd number of solutions (x, y) for x, y, positive integers
       and x > y.

    Theorems 1, 2, 3 are proved by Atkin c.s. in their article "Prime Sieves Using Binary Quadratic Forms"
    
    Let integer Z >= 0.

    Consider the following equations: 
    (1) n = 1 + 4Z,
    (2) n = 7 + 12Z,
    (3) n = 11 + 12Z
    (4) n = 12 + 3Z

    4. Any odd positive integer > 3 can be written in one of these four forms.
    
    5. (From 4 follows) Any n that cannot be expressed as (1), (2) or (3) can be expressed as (4).
    
    6. (Obvious) Any n of forms (1), (2), (3) is odd.
    
    7. Equations (1), (2), (3) are 'mutually exclusive', that is, if there exists Z s.t. one of them holds for a given 
       n, then there does not exist any Z for which the other two hold.

    8. n % 12 == 1 => there exists Z s.t. n = 1 + 4Z.
    
    9. n % 12 == 5 => there exists Z s.t. n = 1 + 4Z.
    
    10. n % 12 == 7 => there exists Z s.t. n = 7 + 12Z.

    11. n % 12 == 11 => there exists Z s.t. n = 11 + 12Z.

    12. n % 12 == 9 => there exists Z s.t. n = 12 + 3Z, and n is a multiple of 3 (and therefore not a prime).

    Theorem 4 (and therefore consequential theorem 5) are not proved... 
    Theorems 5-12 are easy to prove (try it!) 
    
    THE ALGORITHM
    
    - The algorithm leaves all even n untouched, since it mutates is_prime[n] only if n is of the forms (1), (2) or (3),
      which is only possible if n is odd.
    - The algorithm leaves n == 3 untouched, since 3 cannot be written in forms (1), (2) or (3).
    - Therefore for n==2 and n == 3 (both primes!), is_prime[n] is set to True initially, and never changes. 
    - For all n > 3, is_prime[n] is initially set to false, to reflect that initially we have an even number of zero 
      solutions (x, y).
    - In the first loop: 
      a) For all (x, y) the value of n = 4x^2 + y^2 (that is, (x, y) is a solution of n = 4x^2 + y^2). Then it checks 
         if n is relevant (min_prime <= n <= max_prime) and if n % 12 in [1,5]. If so, n can be written as n = 1 + 4Z 
         (see theorems 8 and 9 above). Each time this occurs, is_prime[n] is 'flipped' between False and True. NOTICE 
         that n % 12 == 9 is not considered, since then n is a multiple of 3 and therefore not prime (see theorem 11).
      b) The procedure described in a) is also done for n = 3x^2 + y^2 and n % 12 == 7. If so, n can be written as 
         n = 7 + 12Z (see theorem 10 above).
      c) The procedure described in a) is also done for n = 3x^2 - y^2 and n % 12 == 11. If so, n can be written as 
         n = 11 + 12 Z (see theorem 11 above). 
    - After all (x, y) have been checked, we have is_prime[n] == True if there were an odd number of solutions and 
      is_prime[n] == False if there were an even number of solutions.
    - All n for which is_prime[n] == False are NOT primes. This includes all even numbers (that were initialized to 
      False and never touched, and all n that could not be expressed as (1), (2) or (3). All n for which is_prime[n] 
      == True ARE prime if and only if they are also squarefree! This is checked in the next loop. If n is not 
      squarefree, is_prime[n] is set to False.
    - After the final check, all n for which is_prime[n] == True are prime, so they are collected in a list and returned
      to the caller.  
"""


# def smallest_multiple(factor: int, lower_bound: int) -> int:
#     """Returns the smallest multiple of factor that is larger than or equal to lower_bound.
#        Both parameters MUST be integers!"""
#     # Both params MUST be integers
#     assert factor % 1 == 0
#     assert lower_bound % 1 == 0
#     if (remainder:= lower_bound % factor):
#         return lower_bound + (factor - remainder)
#     return lower_bound


def atkin_sieve(max_prime):
    """returns a list of all primes <= max_prime"""
    # D.R.Y. ;-)
    return atkin_sieve2(min_prime=min(max_prime, 0), max_prime=max_prime)

# optimized_overall = 0


def atkin_sieve2(min_prime=0, max_prime=-1):
    """returns a list of all primes >= min_prime and <= max_prime """

    if min_prime > max_prime:
        raise ValueError(f'min_prime must be < max_prime (min_prime = {min_prime}, max_prime = {max_prime})')

    if max_prime < 2:
        return []

    min_prime = max(2, min_prime)

    is_prime = [False] * (max_prime - min_prime + 1)
    # Since the main loop only touches numbers > 3, we must set is_prime to True for 2 and/or 3 if these are in the
    # range of the primes the caller wants.
    if min_prime == 2:
        is_prime[0] = True
    if min_prime <= 3 <= max_prime:
        is_prime[3 - min_prime] = True

    factor = int(math.sqrt(max_prime)) + 1
    _range = range(1, factor)
    for x in _range:
        x_squared = x * x

        for y in _range:
            y_squared = y * y

            # n = 3x^2 + y^2
            n = 3 * x_squared + y_squared
            if min_prime <= n <= max_prime and n % 12 == 7:
                is_prime[n - min_prime] = not is_prime[n - min_prime]

            # n = 3x^2 - y^2 = 3x^2 + y^2 - (2y^2), multiplying by 2 is fast!
            n -= 2 * y_squared
            if x > y and min_prime <= n <= max_prime and n % 12 == 11:
                is_prime[n - min_prime] = not is_prime[n - min_prime]

            # n = 4x^2 + y^2 = 3x^2 - y^2 + (2y^2), multiplying by 2 is fast!
            n += x_squared + 2 * y_squared
            if min_prime <= n <= max_prime and (n % 12 in [1, 5]):
                is_prime[n - min_prime] = not is_prime[n - min_prime]

    # is_prime may not hold information for all x in range(5, factor). If so, get 'missing' primes!
    missing_primes = []
    if 0 < min_prime <= factor:
        missing_primes = atkin_sieve((min_prime - 1))
    elif min_prime > factor:
        missing_primes = atkin_sieve(factor)

    for x in range(5, factor):
        x_is_prime = False
        if missing_primes and x <= missing_primes[-1]:
            x_is_prime = x in missing_primes
        elif 0 <= x - min_prime < len(is_prime):
            x_is_prime = is_prime[x - min_prime]

        if x_is_prime:
            x_squared = x * x
            # Optimization: set the start value of the for loop to the smallest multiple of x_squared >= min_prime
            loop_start = x_squared
            if min_prime > x_squared:
                remainder = min_prime % x_squared
                if remainder:
                    loop_start = min_prime + (x_squared - remainder)
                else:
                    loop_start = min_prime

            for n in range(loop_start, max_prime + 1, x_squared):
                is_prime[n - min_prime] = False

    return [index + min_prime for (index, prime_flag) in enumerate(is_prime) if prime_flag]


if __name__ == '__main__':
    def test_atkin_sieve():
        """tests for the atkin sieve implementation"""

        def is_prime(n: int) -> bool:
            """Returns True if n is a prima, else False"""
            if n < 2 or n % 1 > 0:
                return False
            for divisor in range(2, n // 2):
                if n % divisor == 0:
                    return False
            return True

        def get_prime_gt(p: int) -> int:
            """Returns the first prime greater than p."""
            assert p % 1 == 0, f'parameter p (value: {p!r}) not an integer.'

            # Special cases (p <= 2):
            if p < 2:
                return 2
            if p == 2:
                return 3

            # Here? Then p > 2. All primes > 2 are odd, so make sure next try the next odd number
            if p % 2 == 0:
                p += 1
            else:
                p += 2
            while not is_prime(p):
                p += 2
            return p

        def test_prime_assertions(primes: list, min_prime, max_prime) -> None:
            assert all(is_prime(p) for p in primes)
            assert all(p >= min_prime for p in primes)
            assert all(p <= max_prime for p in primes)
            if len(primes):
                assert primes[0] == min_prime or primes[0] == get_prime_gt(min_prime), \
                    f'Expected {primes[0]} == {min_prime} or {primes[0]} == {get_prime_gt(min_prime)}'
                assert primes[-1] == max_prime or get_prime_gt(primes[-1]) > max_prime

        def test_for_range(min_p, max_p, expected_sum, expected_nr):
            print(f'\ttesting primes from {min_p} to {max_p}...', end='')
            l1 = atkin_sieve2(min_prime=min_p, max_prime=max_p)
            assert len(l1) == expected_nr
            assert sum(l1) == expected_sum
            test_prime_assertions(l1, min_p, max_p)
            print('ok!')

        # All expected results were obtained with Wolfram Alfa
        print('starting atkin sieve tests... this may take up to a minute!')

        atkin_sieve2(20000, 21000)

        print('range tests:')
        test_for_range(0, 150, 2276, 35)
        test_for_range(12345, 67890, 208424627, 5287)
        test_for_range(23456, 78901, 260049018, 5130)
        test_for_range(34567, 89012, 302578731, 4929)
        test_for_range(45678, 90123, 270368702, 3994)
        print('range tests ok!')

        print('boundary tests:', end='')
        try:
            atkin_sieve2(min_prime=1, max_prime=0)
            assert False
        except ValueError:
            pass
        assert atkin_sieve(-10) == []
        assert atkin_sieve(-1) == []
        assert atkin_sieve(0) == []
        assert atkin_sieve(1) == []
        assert atkin_sieve(2) == [2]
        assert atkin_sieve(3) == [2, 3]
        assert atkin_sieve(5) == [2, 3, 5]
        assert atkin_sieve(150) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79,
                                    83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149]
        assert atkin_sieve2(min_prime=-1, max_prime=0) == []
        assert atkin_sieve2(min_prime=-1, max_prime=1) == []
        assert atkin_sieve2(min_prime=-1, max_prime=2) == [2]
        assert atkin_sieve2(min_prime=-1, max_prime=3) == [2, 3]
        assert atkin_sieve2(max_prime=0) == []
        assert atkin_sieve2(max_prime=1) == []
        assert atkin_sieve2(max_prime=2) == [2]
        assert atkin_sieve2(max_prime=3) == [2, 3]
        assert atkin_sieve2(min_prime=1, max_prime=1) == []
        assert atkin_sieve2(min_prime=1, max_prime=2) == [2]
        assert atkin_sieve2(min_prime=1, max_prime=3) == [2, 3]
        assert atkin_sieve2(min_prime=2, max_prime=2) == [2]
        assert atkin_sieve2(min_prime=2, max_prime=3) == [2, 3]
        assert atkin_sieve2(min_prime=2, max_prime=4) == [2, 3]
        assert atkin_sieve2(min_prime=2, max_prime=5) == [2, 3, 5]
        print(' ok!')
        print('Done.')


    test_atkin_sieve()
