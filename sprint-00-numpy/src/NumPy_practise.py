from numpy import *


numbers = array([[1, 2, 3], [4, 5, 127]], dtype=int8)

numbers[1] = [4,0,0]
print(numbers[1])