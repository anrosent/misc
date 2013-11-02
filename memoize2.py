#little demo of memoization and closures in Python
def memoize(fun):
    cache = {}
    def memoized_fun(*args):
        t = tuple(args)
        if t not in cache:
            res = fun(*args)
            cache.update({t:res})
            return res
        else:
            return cache[t]
    return memoized_fun
    
    
    

"""
def memoize(f):
    cache = {}
    def fn(x):
        if x in cache:
            return cache[x]
        else:
            res = f(x)
            cache.update({x:res})
            return res
    return fn
"""

def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
        
#this works, but you have to put it the function in a lambda form, rather than just calling fibm = memoize(fib)
fibm = memoize(lambda n: 1 if n == 1 or n ==2 else fibm(n-1) + fibm(n-2))

def get_memcache(f):
    return f.__closure__[0].cell_contents    