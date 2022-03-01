# td

> Your todo list for your terminal, made in Python

~~copied~~ Inspired by [Swatto's td app](https://github.com/Swatto/td) 

## Usage

### Installation

### Information

*td* will look at a `.todos` files to store your todos (like Git does: it will try recursively in each parent folder). This permit to have different list of todos per folder. If the file doesn't exist, the program will create it for you.

### CLI

```
Usage: td [OPTIONS] COMMAND [ARGS]...

  pyToDo - your Python to-do manager for your terminal.

  If no command is passed, print to-do list.

Options:
  -d, --done     print done todos
  -a, --all      print all todos
  -v, --version  Show the version and exit.
  -h, --help     Show this message and exit.

Commands:
  add (a)      Add a new to-do.
  clean (c)    Remove finished todos from the list
  init (i)     Initialize a collection of to-dos in current directory path
  modify (m)   Modify the text of an existing todo.
  reorder (r)  Reset ids of todo (no arguments) or swap the position of two...
  search (s)   Search a string in all todos.
  split        Print tasks split between categories.
  toggle (t)   Change the status of a todo to 'done' by giving his id.
  working (w)  Change the status of a todo to 'working' by giving his id.
```
