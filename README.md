# Thesis guide

Work flow on the projects will contain 3 main parts: working with **git**, working with coding on **python** and working with **LateX**

Literature will be provided in the form of files in directory `literature`. Consider using some...

## Git flow

In order to use git properly one may suggest to look into `https://git-scm.com/` for information. Site provides the git GUI for MacOS and Windows, and some free materials. Better way to use git is to use console comands. For Linux/MacOS it is similar to use build-in terminal (with bash/power-shell). For Windows `https://git-scm.com/downloads/win` GUI installation also provide git bash to use it with console comands.

Project structure building shell file can be found in `scripts/technical/building.sh`

### Work in terminal

Frequently used commands in console are:
1. `mkdir {dir_name}` - make directory dir_name
2. `cd {relative_path}` - go to position relative_path
3. `ls` - list all entities in current directory (`-al` - with shadowed files and mode)

Frequently used git commands:
1. `git status` - current status
2. `git add {file_name}` - add file_name to next commit (`add .` - add all files)
3. `git commit -m "{commit_messege}"` - commit with commit_messege as commit messege
4. `git push` - push to remote repository
5. `git pull` - pull from repository
6. `git checkout another_branch` - checkout to another_branch. All not stashed changes will be discarded.
7. `git checkout -b new_branch` - checkout to new_branch
8. `git clone {http-to-repo} {new-dir-for-repo}` - clone remote repo to computer

## Python flow

There are two major schools of using python: IDE and jupyter.

### IDE

The better IDE for python is PyCharm (`https://www.jetbrains.com/pycharm/`). One may just use community edition. It's perfectly fine.

Another IDE to use is VS (Visual Studio Code, cause its free) (`https://code.visualstudio.com/`).

What ever you choose, don't forget to download extensions for python (i.e. pure python from `https://www.python.org/downloads/`) or conda interpreter via `https://www.anaconda.com/`

### Jupyter

"Jupyter has a lot of moons but this is not one of them". Personally, I recommend this option only for those who are not
interesting in development. It's just harder to do in Jupyter. Jupyter-notebook and Jupyter-lab are available at `https://www.anaconda.com/`

### Work in python

Python is OOP, so there are two major approaches to write code here.

First is highly OOP style, where every piece of data is bound to an object and all transformations are performed via specific methods of another objects. 

Second is a little bit simpler but requires a bit more work with files:

All functional transformations and operations are stored in modules and divided by functionality, like data preparation goes to preparation module and model training goes to training module.

In practice, the best work style is what gives the cleaner result for shorter time)

## Project flow

Before the deadline I expect from u three entity:
1. Code that prepare data, train model and present results in some way
2. Remote repo at github.com
3. .tex file with research description, i.e. took some data, tried some models, here results.

Second part requires from u to be log in github.com. After creating account there - give me ur emails/logins for closing this repository)

Third part requires from u using some tex utilities. The fastest and simplest way of writing using latex is using https://www.overleaf.com/
