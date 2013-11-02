#little demo of memoization and closures in Python

#Black-box memoization here only works if of the form
# fib = memoize(fib)
#    i.e., the names of the assignment target and the argument to memoize are the same. This exploits the fact that the function passed to memoize calls itself recursively, but that name will have been redefined to be the memoized version. This does not work if you want to do something like
#   fib_m = memoize(fib)
#   To do so would require some nice introspection, or possibly some macro preprocessing with ASTs
def memoize(fun):
    fun = memoize_fun(fun)
    return fun

def memoize_fun(f):
    cache = {}
    def fn(x):
        if x in cache:
            return cache[x]
        else:
            res = f(x)
            cache.update({x:res})
            return res
    return fn
    

def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n-1) + fib(n-2)
        
#this works
fibm = memoize(lambda n: 1 if n == 1 or n ==2 else fibm(n-1) + fibm(n-2))

#does not cache intermediate results on the call tree
fibm2 = memoize(fib)

#DOES cache all intermediate results on the call tree in the closure
fib = memoize(fib)

def get_memcache(f):
    return f.__closure__[0].cell_contents