#! /usr/bin/env python3

import sys
import math
import numpy

class SES:
    # modular exponentiation
    def mod_pow(self, a, b, n):
        x = 1
        while b > 0:
            if b % 2 == 1:
                x = (x*a)%n
            a = (a*a) % n
            b >>= 1
        
        return x

    # method for testing primality of number
    def is_prime(self, n):
        prime = True
        nums = []
        # Generating set of "random" numbers of size lg(n)
        for i in range(2, int(math.log2(n))):
            nums.append(numpy.random.randint(2,n))

        for i in nums:
            if ((self.mod_pow(i,n,n))%n != i%n):
                return False
        
        return True

    def gen(self):
        p = 100
        q = 100

        # picking two random primes p,q = 3 (mod 4)
        while not self.is_prime(p) and not p%4 == 3:
            p = numpy.random.randint(100, 10000)

        while not self.is_prime(q) and not q%4 == 3:
            q = numpy.random.randint(100, 10000)

        n = p*q

        # x0 is a random integer in the range from 1 to p*q
        x0 = numpy.random.randint(1,n)

        print("(p:{}, q:{}, x_0:{})".format(p,q,x0))

    def enc(self):
        # Taking in the seed
        vals = input("Please specify the seed (p, q, x0) for generation: ").split(" ")

        # invalid input
        if len(vals) != 3:
            print("Please enter only 3 values: p, q, x_0")
            exit(0)

        p = int(vals[0])
        q = int(vals[1])
        x0 = int(vals[2])

        n = p*q
        
        l = int(input("Please specify a length for the random number (in bits): ")) 
        #l = int(sys.argv[1])
        msg = input("Please specify a binary string to encode: ")
        

        num = 0

        i = 0
        mask = 0b1

        # Random number generator
        # b_i = b_(i-1)^2 mod N
        while i < l:
            num <<= 1

            x = self.mod_pow(x0, 2, n)
            lsb = x & mask
            num |= lsb

            x0 = x
            
            i += 1

        # output "randomly generated" number in binary and decimal
        output = format(num, '#0{}b'.format(l+2))[2:]

        if len(output) < len(msg):
            print("Message is too long for secret!")
            exit(1)


        #print(output)
        #print(' '.join([output[i:i+4] for i in range(0, len(output), 4)]))

        secret = ""

        i = 0
        while (i < len(msg) and i < len(output)):
            secret += str(int(msg[i]) ^ int(output[i]))
            i+=1

        # Output the secret
        print("Secret is: {}".format(' '.join([secret[i:i+4] for i in range(0, len(secret), 4)])))

    def dec(self):

        secret = input("Please enter the secret to be decoded (omit any spaces): ")
        seed = input("Please input the seed in the format 'p q x0': ").split(" ")

        p = int(seed[0])
        q = int(seed[1])
        x0 = int(seed[2])

        n = p * q

        l = len(secret)
        i = 0
        mask = 0b1
        num = 0

        while i < l:
            num <<= 1

            x = self.mod_pow(x0, 2, n)
            lsb = x & mask
            num |= lsb

            x0 = x
            
            i += 1

        output = format(num, '#0{}b'.format(l+2))[2:]

        msg = ""

        i = 0
        while (i < len(secret) and i < len(output)):
            msg += str(int(secret[i]) ^ int(output[i]))
            i+=1

        # Output the secret
        print("Original Message is: {}".format(' '.join([msg[i:i+4] for i in range(0, len(msg), 4)])))

        


class Main:
    def main():
        while True:
            ses = SES()
            s = input("Type 'g' for keygen, 'e' for encryption, 'd' for encryption: ")
            if (s == "g"):
                ses.gen()
                exit(0)
            elif (s == "e"):
                ses.enc()
                exit(0)
            elif (s == "d"):
                ses.dec()
                exit(0)
            else:
                print("Invalid choice")
        

if __name__ == "__main__":
    Main.main()