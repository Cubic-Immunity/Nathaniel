# File: homework1.py

# --- Variables and Data Types ---
a = 10
print(a)
print(type(a)) # integers (int), whole number

b = 1.5
print(b)
print(type(b)) # float, integers with a fractional component

c = 3j
print(c)
print(type(c)) # complex number (complex), has both a real and a fractional part

d = "hello"
print(d)
print(type(d)) # string (str), textual data (not limited to words)

e = [1, 2, 3]
print(e)
print(type(e)) # list, stores ordered collection of items

f = {"name": "Ellen", "favorite fruit": "strawberry"}
print(f)
print(type(f)) # dictionary (dict), has key-value pairs to map values to certain keys

g = (1, 2)
print(g)
print(type(g)) # tuple, is an immutable, ordered collection of items

h = ["apple", "banana", "strawberry"]
print(h)
print(type(h)) # list, contains a list of strings

i = True
print(i)
print(type(i)) # boolean (bool), gives truth value of something (1=True, 0=False)

j = None
print(j)
print(type(j)) # NoneType, indicates the absence of a value

k = [True, "blue", 12]
print(k)
print(type(k)) # list, list that contains a bool, string, and int

l = str(14)
print(l)
print(type(l)) # string, cast an int through the string method str()

m = 1e4
print(m)
print(type(m)) # float, gives 10,000.0

"""
1. How many different data types did you find?
    We found 9 different data types.
2. List all the data types you found.
    Int, float, complex, str, list, dict, tuple, bool, and NoneType
3. What variables have the same data types?
    B/m are floats, d/l are strings, and e/h/k are lists.
4. What was the data type of l? Why is it not an integer? What does str() do?
    The data type of l was a strings, it was not an integer becausethe str() method that 14 was 
    placed within converts its data type to a string.
5. Look up one more data type not given above. Repeat the same procedure.
    x = range(6)
    print(x)
    print(type(X)) # range, immutable sequence of intgers
"""

# --- Booleans ---
print(10 > 9) # True, 10 is greater than 9
print(10 == 9) # False, 10 does not equal 9
print(10 <= 9) # False, 10 is not less than or equal to 9
print(bool("abc")) # True, the string is non-empty
print(bool(123)) # True, 123 is non-zero
print(bool(["apple", "cherry", "banana"])) # True, list is non-empty
print(bool(True)) # True, true is true
print(bool(False)) # False, false is false
print(bool(0)) # False, integer is zero
print(bool("")) # False, empty string
print(bool(" ")) # True, string non-empty (spaces make it non-empty)
print(bool(())) # False, empty tuple
print(bool([])) # False, empty list
print(bool({})) # False, empty dictionary
print(bool(True and False)) # False, something cannot be both true and false
print(bool(True and True)) # True, both sides are true 
print(bool(False and False)) # False, both sides are not true
print(bool(True or False)) # True, at least one side is true
print(bool(True or True)) # True, at least one side is true
print(bool(False or False)) # False, no side is true
print(bool(not(False))) # True, not switched the truth value of false making it true
print(bool(not(True))) # False, not switched the truth value of true making it false 

"""
1. What pattern do you notice about expressions returning True or False?
    If they are empty then they are false, and true if they have are conytaining something.
    They are true so long as they are non-zero and fasle otherwise.
2. Which expression surprised you about its result?
    The empty ones since I had forgotten that empty lists, dictionaries, etc. are considered false 
    in regards to their truth value.
3. Create an expression, not given above, that will return True. Why is it True?
    print(bool())
4. Create an expression, not given above, that will return False. Why is it False?
    print(1e4 == None) # This is False because 10,000 doesn't equal None, it has a real value
"""

# --- Operators ---
 # --- Arithemetic Operators ---
print(10 + 5) # 15, + performs addition
print(10 - 5) # 5, - performs subtraction
print(2 * 4) # 8, * performs multiplcation
print(6 / 3) # 2, / performs division
print(5 % 2) # 1, % returns the remainder of the division
print(3 ** 2) # 9, ** peforms exponentiation
print(15 // 2) # 7, // performs floor division (integer division) wherein only the integer part of the division is returned

 # --- Comparison Operators ---
print(5 == 2) # False, 5 does not equal 2
print(10 != 10) # False, 10 does equal 10
print(2 < 5) # True, 2 is less than 5
print(12 > 5) # True, 12 is greater than 5
print(5 <= 6) # True, 5 is less than or equal to 6
print(1 >= 10) # False, 1 is not greater than or equal to 10

 # --- Assignments Operators ---
x = 5
x += 5
print(x) # 10, x = x + 5 = 10

x = 5
x -= 4
print(x) # 1, x = x - 4 = 1

x = 5
x *= 3
print(x) # 15, x = x * 3 = 15

 # --- Logical Operators ---
"""
1. What does the operator and do? Write an expression that results in True. Write an expression that results in False.
    The operator and checks the truth value of whatever is on either side of it and returns True only
    when what is on both sides of it are also True.
2. What does the operator or do? Write an expression that results in True. Write an expression that results in False.
    The or operator checks the truth value of whatever is on either side of it and returns True so long as
    at least one of the things on either side of it is True.
3. What does the operator not do? Write an expression that results in True. Write an expression that results in False.
    The not operator switches the truth value of whatever it is being applied to, so True becomes False
    and False becomes True.
"""

"""
1. What is the difference between / and //?
    The difference is that / gives you regular division (a float), while // gives you floor divion
    wherein only the integer part of the division is returned.
2. What is the difference between % and //?
    The difference is that % gives you the remainder of the division, while // gives you the whole integer
    part of the division.
3. What operator would you use to calculate the remainder when dividing two numbers? Give an example.
    You would use the % operator to get the remainder when dividing two numbers. Example: 9 % 3 = 0
4. How do assignment operators work?
    Assignment operators work by assinging values to a variable, like the equal sign =. There are
    also shorthanded assignment operators like in the examples above +=, -=, *=, whereby you use the 
    variable itself in calculating its new value.
"""
 # --- Strings ---
my_string = "hello"

print(my_string) # Prints: hello
print(my_string[0]) # Prints: h
print(my_string[1]) # Prints: e
print(my_string[2]) # Prints: l
print(my_string[3]) # Prints: l
print(my_string[4]) # Prints: o
print(my_string[-1]) # Prints: o
print(my_string[1:3]) # Prints: el
print(my_string[0:5:2]) # Prints: hlo
print(len(my_string)) # Prints: 5
print(my_string + " goodbye") # Prints: hello goodbye
print(my_string * 7) # Prints:hellohellohellohellohellohellohello
"""
1. Define the term slicing. For which of the manipulations did you slice your string?
    Slicing is a method by which we can extract specific portions of seqeunces. We sliced the string anytime
    we called my_string[] with whatever was inside the brackets [].
2. Call the following, describe the result:
    name = "Oski"
    print("Hello, my name is", name)

    This prints out the following: Hello, my name is Oski.
3. Call the following, describe the result.
    name = "Oski"
    print(f"Hello, my name is {name}")

    This prints out the following: Hello, my name is Oski.
4. What is the difference between the two last print statements? Hint: Look up f-strings.
    The difference is that the first one concatenates the variable name to the end of the string being 
    printed out, while the second uses f-strings to embed the variable into the string allowing for more
    versatilitiy in its usage.
"""
 # --- Terminal commands ---
"""
1. cd
    # cd
    # change directories, used to move from one folder (directory) to another
    # example: cd python_decal_fa25
2. ls
    # ls 
    # list, list of the contents of the current directory
    # example: ls
3. ls -a
    # ls -a
    # list all, lists all the contents of a directory, even the hidden folders
    # example: ls -a
4. mkdir
    # mkdir
    # make directory, makes a new directory (folder) in the current directory
    # example: mkdir homework1
5. cat
    # cat
    # concatenate, prints out the contents of a file to the terminal.
    # example: cat homework1.py
6. pwd
    # pwd
    # print working directory, prints out the full path to current directory you are in
    # example: pwd
7. cd ..
    # cd ..
    # goes up one level up to the parent directory
    # example: cd ..
8. cd .
    # cd .
    # keeps you in the current directory
    # example: cd . 
9. cd ∼
    # cd ~
    # takes you to the home directory
    # example: cd ~
10. cp
    # cp
    # copy, creates a copy of a file or folder (needs -r after cp if copying a folder)
    # example: cp DataTypes.py DataTypes_Backup.py
11. mv
    # mv
    # move, moves or renames a file or folder
    # example: mv DataTypes_Backup.py DataTypes_Backup1.py
12. rm (be careful with this one)
    # rm
    # remove, deletes a file or folder (needs -r after rm to remove a folder)
    # example: rm DataTypes_Backup1.py
13. clear
    # clear
    # clears the terminal of all previous commands
    # example: clear
14. grep
    # grep
    # global regular expression print, searches for certain text inside a file
    # example: grep "Hello" DataTypes.py
"""

"""
1. Look up 3 other commands not present. Define and explain how to use them on the command line.
    # touch <file name>
    # creates an empty file

    # echo 'text'
    # echo 'text' > file or 'text' >> file name
    # print text or write into a file ("text" > file name to overwrite if it already exists and 
                                       "text" >> file name to append it to the file without overwriting)

    # history
    # shows a list of the commands you have typed suring the terminal session
2. What is the difference between ls and ls -a?
    The difference is that ls will list out the visible contents of a directory, while ls -a will print
    out all the contents of a directory including the hidden things.
3. What is a hidden file?
    A file that is not visible to the user by default (folders can also be hidden).
4. Look up 3 other flags (e.g., -a was a flag for the ls command). Define and explain how to use them on the command line.
    There is also:
    # <command> --help
    # will print out the available flags for that command, essentially the documentation

    # <command> -l
    # makes the printout be in long listing form, essentially containing extra info about the contents

    # <command> -h
    # Can combine -l (long listing) with -h (human-readable) to show file sizes kb/mb/gb.
    # Note: On Git Bash for Windows, -h may still show sizes in bytes due to implementation differences.
"""

# --- Running Your Script ---