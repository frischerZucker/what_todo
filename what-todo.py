#!/usr/bin/python

import argparse
import os

from dataclasses import dataclass

@dataclass
class Args:
    """
    Arguments that can be passed to the script.
    """
    path: str
    recursive: bool

@dataclass
class Todo:
    """
    Describes a todo.
    """
    file: str
    line: int
    description: str

    def location(
        self,
    ) -> str:
        """
        Returns the todos location in the form of [file]@[line].

        :returns: str
        """
        return f"{self.file}@{self.line}"

@dataclass
class File:
    """
    Describes a file.
    """
    path: str
    name: str
    extension: str
    comment_specifier: str

supported_file_extensions: list[str] = [
    "tex",
    "py",
]

comment_specifiers: dict[str, str] = {
    "tex": "%",
    "py": "#",
}

def get_supported_files(
    directory: str,
    recursive: bool = False,
) -> list[File]:
    """
    Get a list with supported files in the directory.

    Checks the file extension of files in the directory.
    Builds a list with files that have supported extensions.

    :param directory: Path to the directory to look into.
    :type directory: str
    :param recursive: Wether subdirectories are also scanned or not.
    :type recursive: bool

    :returns: list[File]
    """
    supported_files: list[File] = []
    if recursive:
        for (current_directory, _, files) in os.walk(directory):
            supported_files.extend([File(path=os.path.join(current_directory, f), name=f, extension=f.split(".")[-1], comment_specifier=comment_specifiers[f.split(".")[-1]]) for f in files if f.split(".")[-1] in supported_file_extensions])
    else:
        file_names: list[str] = [f for f in os.listdir(directory) if f.split(".")[-1] in supported_file_extensions]

        supported_files = [File(path=os.path.join(directory, f), name=f, extension=f.split(".")[-1], comment_specifier=comment_specifiers[f.split(".")[-1]]) for f in file_names]

    return supported_files

def get_todos_from_file(
    file: File,
) -> list[Todo]:
    """
    Get a list with todos in a file.

    Iterates over the files content and checks comments for todos.
    Builds a list with all todos that are found.

    :param file: File
    :type file: File

    :returns: list[Todo] 
    """
    todos: list[Todo] = []

    line_counter: int = 0
    with open(file.path, "r") as f:
        for line in f:
            line_counter = line_counter + 1

            # We are only looking for todos in comments. -> Ignore line without comments.
            if not line.startswith(file.comment_specifier):
                continue
            
            # Line has no todo. -> Skip.
            if not "TODO:" in line:
                continue

            todos.append(Todo(file=file.name, line=line_counter, description=line))

    return todos

if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        default=os.getcwd(),
        help="Path to a directory or file to scan. Defaults to the current working directory.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Also scan subdirectories.",
    )
    args: Args = parser.parse_args(namespace=Args("", False))
    
    if not os.path.exists(args.path):
        raise FileNotFoundError(f"Path does not exist: {args.path}")

    files: list[File] = []
    if os.path.isdir(args.path):
        # Path points to a directory. -> Scan the whole directory for supported files.
        files.extend(get_supported_files(args.path, recursive=args.recursive))
    elif os.path.isfile(args.path):
        # Path points to a file. -> Directly include the file (if it is of a supported file type).
        file_name: str = os.path.basename(args.path)

        if not file_name.split(".")[-1] in supported_file_extensions:
            raise ValueError(f"File type is not supported: {file_name}")

        files.append(File(path=args.path, name=file_name, extension=file_name.split(".")[-1], comment_specifier=comment_specifiers[file_name.split(".")[-1]]))

    for f in files:
        todos: list[Todo] = get_todos_from_file(f)

        if not todos:
            continue

        print(f"TODOs in {f.name}:")
        
        for t in todos:
            print(f"  {t.location()}: {t.description[:-1]}")