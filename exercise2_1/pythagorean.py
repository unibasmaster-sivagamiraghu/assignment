import math

def hypothenuse(a, b):
    return math.sqrt(a**2 + b**2)

def display_results(a, b):
    c = hypothenuse(a, b)
    print(f"{a:.2f}^2 + {b:.2f}^2 = {c:.2f}^2")

# Test the function with the specified values
display_results(3, 4)    # Output should be: 3.00^2 + 4.00^2 = 5.00^2
display_results(1, 1)    # Output should be: 1.00^2 + 1.00^2 = 1.41^2
