#! /usr/bin/env python3
import numpy
import math
import sys

# Implementing (t,m) polynomial secret sharing
# Uses mod_pow and is_prime from previous assignments in CMSC456

# modular exponentiation
def mod_pow(a, b, n):
    x = 1
    while b > 0:
        if b % 2 == 1:
            x = (x*a)%n
        a = (a*a) % n
        b >>= 1
    
    return x

# method for testing primality of number
def is_prime(n):
    prime = True
    nums = []
    # Generating set of "random" numbers of size lg(n)
    for i in range(2, int(math.log2(n))):
        nums.append(numpy.random.randint(2,n))

    for i in nums:
        if ((mod_pow(i,n,n))%n != i%n):
            return False
    
    return True

# Picking a prime of size  ~ 2^|s|
def pick_prime(size):
    n = int(math.pow(2, size))

    while not is_prime(n):
        n += 1

    return n

# Input for the secret to be shared (integer in this case)
secret = input("Enter a secret: ")
if secret == None:
    print("Please enter a secret")
    exit(0)

# in case of error lol
if sys.argv[1] == None or sys.argv[2] == None or sys.argv[1] == "" or sys.argv[2] == "":
    print("Usage: secret-sharing.py <t> <m>")
    exit(0)

# Arguments for secret sharing: t is the minimum amount of participants who can get secret
# m is the total number of participants in the scheme.
t = int(sys.argv[1])
m = int(sys.argv[2])

# pick prime approx. size of 2^|s|
p = pick_prime(int(math.floor(math.log2(int(secret))) + 1))

# Coefficients are random numbers in set [1,t-1]
coeffs = [numpy.random.randint(1, p) for i in range(0, t)]
# the constant is the secret
coeffs[0] = int(secret)

# Evaluate f(i) % p for all A_1...A_m
parts = [int(numpy.polynomial.polynomial.polyval(i, coeffs))%p for i in range(m+1)]

# Printing the results out
for i in range(1, len(parts)):
    print("A{}: {}".format(i, parts[i]))
