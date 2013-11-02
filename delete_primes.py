#Find all primes such that removing all digits in succession moving leftward yields only prime numbers
#Mario Livio made a post about this, so I thought I'd give it a shot

from math import sqrt, ceil

def make_num(lon):
    return sum(10**(p - 1) * lon[-p] for p in range(1,len(lon)+1))
    
#Very naive but this is a one-off so it's all good
def isprime(n):
    if n==1:
        return False 
    else:
        return not any(n/x == n//x for x in range(2, ceil(sqrt(n))+1))
     
def next_primes(lon):
    return [lon+[x] for x in range(1,10) if isprime(make_num(lon+[x]))]

def find_delprimes(lon):
    print(make_num(lon))    
    result = [make_num(lon)]
    for ln in next_primes(lon):
        result.extend(find_delprimes(ln)) 
    return result

if __name__ == '__main__':
    print("Max: %s"%max(find_delprimes([])))
    
