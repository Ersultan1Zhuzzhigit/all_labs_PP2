
from itertools import permutations
def string_permutations(str):
    return [''.join(p) for p in permutations(str)]
str=input("string=")
print(string_permutations(str))
