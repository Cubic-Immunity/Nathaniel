# --- Homework 1+2 Review ---
# --- Vocabulary Review ---
"""
1. Git vs. GitHub
Git is the version-control system, while GitHub is a web-hosted 
service for Git repositories.

2. Terminal vs. Command Line
The terminal is the program/window that hosts a shell, while
the command line (or shell) is the interface where you type commands.

3. Local vs. Remote Repository
A local repo is the Git repository on your machine, whereas the
remote repo is the Git repository hosted elsewhere, like GitHub.

4. Version Control
A system to track and manage changes to files over time, like Git.

5. Staging Area
The temporary holding where you collect changes, from "git add",
before commiting them, with "git commit".

6. git add
Adds changes to the staging area.

7. git commit
Commits changes from the staging area (can have a message 
describing the change).

8. git push
Sends your local commits to a remote repository, like GitHub.

9. git status
Shows the current repo state (like changes, staged files, 
untracked files, and current branch).

10. git pull
Fetches and merges changes from the remote repo 
into your local branch.

11. pwd
"Print working directory": shows the absolute path of the 
current directory.

12. ls
"List" files/directories in the current directory.

13. cd
"Change directory" to another directory.

14. nano
A simple terminal text editor.

15. touch
Creates an empty file.

16. mv
Move or rename files/directories.

17. rm
Remove (delete) files.

18. cat
Print the contents of a file to the terminal.

"""

# --- A Directory Tree ---
"""
1). pwd
2). ls
3). cd ../brianna_repo
    git pull origin main
4). mv homework.py ../judy_decal/homework/
5). cd ../judy_decal/homework
6). cat homework.py or nano homework.py
7). git add .
    git commit -m "describe changes"
    git push origin main
8). This error means the remote repo has commits that Judy doesn't 
    have locally. To resolve this, you need to re-synch the two 
    repos with "git pull origin main".
9). cd ~/Recents
 
"""

# --- Homework 3 Review ---
# --- Data Types ---
def checkDataType(x):
    """Retrns the data type of the input"""
    return print(type(x))

# --- Conditionals ---
def evenOrOdd(x):
    if x % 2 == 0:
        return print("'Even'")
    else:
        return print("'Odd'")

# --- Loops ---
def sumWithLoop(lst):
    total = 0
    for num in lst:
        total += num
    return print(total)

# --- Homework 4 Review ---
# --- Lists ---
def duplicatelist(lst):
    new_lst = []
    for i in lst:
        new_lst.append(i)
        new_lst.append(i)
    return print(new_lst)

# --- Debugging ---
def square(num):
    return num * num

print(square(5))