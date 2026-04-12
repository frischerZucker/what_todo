# What-TODO

What-TODO is a tool to scan a directory for TODO-notes written in comments.  
I often leave reminders in my code like this:
```python
...
# TODO: Change whatever
...
```
In projects including multiple files, keeping track of all these notes becomes quite a challenge.
__What-TODO__ helps by scanning supported files for comments containing _"TODO:"_ and listing each entry together with its file name and line number, giving a quick overview over what needs attention.

## Installation

Clone the repository and place the script where ever you want it to be:

```bash
git clone https://github.com/frischerZucker/what_todo.git
```

## Usage

You can run the script using Python. 
There are no requirement besides Python and its Standard Library.

```python
python what-todo.py [-h] [-r] [dir]
```
You can pass it a path to the directory that should be scanned using the positional argument __dir__. 
If none is passed it defaults to the current working directory.

You can also use the following optional arguments:  
__--help__ Show a help message.  
__--recursive__ Also scan subdirectories of the scanned directory.

## License

This project is licensed under the BSD‑2‑Clause license.