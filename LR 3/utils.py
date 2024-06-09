import functools

def memoized(func):
  @functools.wraps(func)
  def inner(*args, **kwargs):
    key = f'{args[0]}, {func.__name__}'
    if key not in inner.cache:
      inner.cache[key] = func(*args, **kwargs)
    return inner.cache[key]

  inner.cache = {}
  return inner

@memoized
def factorial1(n):
    from math import factorial
    return factorial(n)

@memoized
def factorial2(n):
  from scipy.special import factorial
  return factorial(n)
