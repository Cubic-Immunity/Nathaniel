# File: homework3.py

# --- Print Functions ---
def say_goodbye(name):
    """Says goodbye to the given name"""
    print(f'Goodbye, {name}')

def circle_area(radius):
    """Calculates the area of a circle with a given radius"""
    area = 3.14 * radius ** 2
    print(area)

# --- Return Functions ---
def subtract(a, b):
    """Subtracts the two given numbers a-b"""
    return a - b

def multiply(a, b):
    """Multiplies the two given numbers a*b"""
    return a * b

def divide(a, b):
    """Divides the two given numbers a/b"""
    return a / b

# --- Conditionals ---
def min_max_temp(lst):
    """Return a tuple containing the (min, max) temperature"""
    min_val = min(lst)
    max_val = max(lst)
    return (min_val, max_val)

def is_weekend(day_num):
    """Takes an integer (1=Monday, ..., 7=Sunday) and returns True if it's a weekend, False otherwise."""
    if day_num == 6 or day_num == 7:
        return True
    else:
        return False
    
def fuel_efficiency(distance, fuel):
    """Calculates and returns fuel efficiency in miles per gallon."""
    return distance / fuel

def encrypt(n):
    """Takes an integer n, moves the last digit to the front, and returns the result."""
    if n < 10:
        return n  # single-digit numbers stay the same
    
    last_digit = n % 10        # get the last digit
    rest = n // 10             # remove the last digit
    num_digits = len(str(rest))  # count digits in the remaining number
    
    # Move last digit to front
    result = last_digit * (10 ** num_digits) + rest
    return result

# --- Loops ---
def power(x, y):
    """Computes x raised to the power of y using a for loop."""
    result = 1
    for _ in range(y):
        result *= x
    return result

def find_min_for(lst):
    """Finds the minimum entry within a list using a for loop"""
    if not lst:
        return None  # handle empty list
    min_val = lst[0]
    for num in lst:
        if num < min_val:
            min_val = num
    return min_val

def find_max_for(lst):
    """Finds the maximum entry within a list using a for loop"""
    if not lst:
        return None # handle empty list
    max_val = lst[0]
    for num in lst:
        if num > max_val:
            max_val = num
    return max_val

def find_min_while(lst):
    """Find the mimimum entry within a list using a while loop"""
    if not lst:
        return None # handle empty list
    min_val = lst[0]
    i = 1
    while i < len(lst):
        if lst[i] < min_val:
            min_val = lst[i]
        i += 1
    return min_val

def find_max_while(lst):
    """Find the maximum entry within a list using a while loop"""
    if not lst:
        return None # handle empty list
    max_val = lst[0]
    i = 1
    while i < len(lst):
        if lst[i] > max_val:
            max_val = lst[i]
        i += 1
    return max_val

def sum_of_digits(n):
    """Finds the sum of the digits within a number"""
    n = abs(n)  # make sure it works for negative numbers
    total = 0
    while n > 0:
        total += n % 10  # add last digit
        n //= 10         # remove last digit
    return total

print(sum_of_digits(91537))