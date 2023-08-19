Key Lessons
===========
## Refresher
### Classes
- `self._<attr>` indicates a pseudo-private property
- Use the `@property` decorator to return the value of the private properties
- Use the `@<attr>.setter` decorator to set the value of private properties


## Variables and Memory
- Use `sys.intern` to intern a string - i.e. save it to a specific memory address. This permits faster lookups in the future
- Using sets to check for membership is ~10x faster than using tuples or lists


## Numeric Types
### Integer
- Use `bin(#)`, `oct(#)` and `hex(#)` to convert from a base 10 integer to binary, octagonal and hex, respectively
- `divmod(a, b)` returns a tuple `(a // b, a % b)`

### Fractions
- `from fractions import Fraction`
- 0.1 can't be represented by a finite number of binary digits
    - ex. `print(format(0.1, '.25f'))`
- `Fraction(math.pi).limit_denominator(10) = 22/7` - limits the denominator to help represent irrational numbers as a ratio of smaller integers
- `math.isclose(math.pi, Fraction(math.pi))` can help indicate equality between irrational and rational numbers


### Floats
- CPython floats use the C double type which implements the IEEE 754 double-precision binary float
    - sign -> 1 bit (0 = positive, 1 = negative)
    - exponent -> 11 bits (-1022, 1023)
    - significant digits -> 52 bits -> 15-17 significant (base-10) digits
- `isclose(1000.0000001, 1000.0000002) == True`
- `isclose(0.0000001, 0.0000002, abs_tol=1e-5) == True` - when comparing numbers close to zero make sure to specify the `abs_tol` param

#### Rounding
`round(1.25, 1), round(1.35, 1) == (1.2, 1.4)` - Python implements Banker's rounding - finds the closest leas significant digit that is EVEN to reduce the bias from rounding

### Decimals
- `from decimal import Decimal`
- Use `decimal.getcontext()` to change the precision, rounding type, etc.
- Use `decimal.localcontext()`, which returns a context manager, to do local calculations with altered precision, for example
    - ex. `with decimal.localcontext() as ctx: ...`
- `Decimal(0.1) != Decimal('0.1')` - make sure to pass strings into the `Decimal` constructor when converting floats
- `b = a * (b // a) + (b % a)` will always hold for the div and mod operators
- Use `".ln()`, `".exp()`, ... for decimal operations
    - Note that `".sqrt() != math.sqrt(")` since the math module converts numbers to floats before performing calculations
- Decimals take up ~4x more memory than floats, take ~20x longer to create and take ~2x longer to perform operations. Only use decimals if you need the extra precision

### Booleans
- Booleans are a subclass of integers
- `bool(object)` will check `__bool__(self)` of the object's class. If `__bool__(self)` is not implemented, `__len__(self)` is executed. If `__bool__(self)` returns `False` or `__len__(self)` is 0, `object` is falsy, otherwise the object is truthy
- `None`, `False`, `0` and empty iterables (`''`, `[]`, ...) are special cases of falsy objects. Most Python objects are truthy

#### Precedence and Short-Circuiting
- `not` -> `and` -> `or` by order of evaluation
- `True or 0 == True`, `False and 1 == False` - there's no need to evaluate the remainder of the expression once truthyness is known from the first term

#### Operators
- X or Y: if X is truthy -> return X, otherwise evaluate Y and return it
    - ex. `1 or 1/0` short-circuits the div by 0 error and returns 1
    - ex. `val = val or 'n/a'` can help coerce null/empty values (ex. `val = None`)
- X and Y: if X is falsey -> return X, otherwise evaluate and return Y
    - ex. `val and val[0] or 'n/a'` will return the first element of a string, or `'n/a'` if the string is empty or `None`

#### Chained Comparisons
- ex. `1 < 2 < 3 < 4`
