#File: homework4.py

# --- Lists ---
# foods = ['sushi', 'cereal', 'carrots', 'fish', 'apple']
# print(foods[1])
# print(foods[-1])
# foods.append('rice')
# print(foods)
# foods.insert(0, 'apple')
# print(foods)
"""
I encountered this error, 
TypeError: 'str' object cannot be interpreted as an integer
I originally wrote: foods.append('apple', 0)
I mixed up the keywords. I fixed it by swapping the arguements position.
"""
# del foods[2]
# print(foods)
# print(len(foods))
# for food in foods:
#     print(food.upper())
"""
I encountered this error,
SyntaxError: Missing parentheses in call to 'print'. Did you mean print(...)?
I originally wrote: print food.upper()
I forgot to use parentheses. I fixed this by adding the parentheses.
"""
# new_foods = foods[::len(foods)-1]
# print(new_foods)
# if 'potato' in new_foods:
#     print('A potato!')
# else:
#     print('No potato')

# --- Slicing and Striding ---
# numbers = list(range(0, 21))
def get_first_15(lst):
    """ Takes a list of numbers and returns the first 15 elements"""
    return lst[:15]
def get_every_5th(lst):
    """ Takes the list and returns every 5th element from it."""
    return lst[::5]
def reverse_and_stride(lst):
    """ Takes the list and reverses it, then returns every 3rd element of the reversed list"""
    reversed_lst = lst[::-1]
    return reversed_lst[2::3]
"""
I encountered this error,
SyntaxError: invalid syntax
I orginally wrote: return reversed_lst = lst[::-1]
I was trying to use assignment in the return of the function, and python did not like that.
I fixed this by moving it into the function, and not inside return.
"""
# step1 = get_first_15(numbers)
# print(step1)
# step2 = get_every_5th(step1)
# print(step2)
# step3 = reverse_and_stride(step2)
# print(step3)

# --- Nested Lists ---
numbers = [
[1, 2, 3],
[4, 5, 6],
[7, 8, 9]
]
# print(numbers[2])
# print(numbers[1][1])
# numbers.append([10, 11, 12])
# print(numbers)
def sum_nested(lst):
    """ Sums the elements within a nested list"""
    total = 0
    for row in lst:
        total += sum(row)
    return total
print(sum_nested(numbers))

# --- Create a 5x5 List ----
def create_5x5():
    """ Creates a 5x5 nested list that contains values from 1 to 25"""
    matrix = []
    num = 1
    for i in range(5):
        row = []
        for j in range(5):
            row.append(num)
            num += 1
        matrix.append(row)
    return matrix
# numbers_5x5 = create_5x5()
# print(numbers_5x5)

def replace_multiples_of_3(lst):
    """ Replaces all mulitples of 3 with a ?"""
    for row in range(len(lst)):
        for col in range(len(lst[row])):
            if lst[row][col] % 3 == 0:
                lst[row][col] = '?'
    return lst
# updated_5x5 = replace_multiples_of_3(numbers_5x5)
# print(updated_5x5)

def sum_not_questions(lst):
    """ Sums the elements in the list as long as they are not ?"""
    total = 0
    for row in lst:
        for num in row:
            if num != '?':
                total += num
    return total
# total_sum = sum_not_questions(updated_5x5)
# print(total_sum)

# --- Dictionaries ---
# ages = {
# "Katie": 30,
# "Mariam": 42,
# "Safia": 25,
# "Mira": 48
# }
# print(ages["Katie"])
# ages["Mira"] = 100
# print(ages)
# ages.pop("Mariam")
# print(ages)
# for name, age in ages.items():
#     print(f"{name}: {age}")

# print(sum_nested(numbers))