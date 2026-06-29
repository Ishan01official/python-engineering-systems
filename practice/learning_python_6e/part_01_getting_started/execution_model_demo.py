"""Show how Python runs a file: source -> bytecode -> runtime objects.

Run from the repo root:

    python practice/learning_python_6e/part_01_getting_started/execution_model_demo.py
"""

import dis
import importlib.util
import inspect
import os
import py_compile
import sys
from pathlib import Path


DATA = "global data object"


def section(title):
    print(f"\n=== {title} ===")


def show_runtime_paths():
    source_path = Path(__file__).resolve()
    expected_bytecode_path = importlib.util.cache_from_source(str(source_path))

    section("1. Source File")
    print(f"Current working directory: {Path.cwd()}")
    print(f"Python executable:         {sys.executable}")
    print(f"Source file __file__:      {__file__}")
    print(f"Resolved source path:      {source_path}")

    section("2. Bytecode")
    print("When you run a script directly, Python compiles it in memory first.")
    print("For learning, this demo also writes a .pyc bytecode file explicitly.")
    print(f"Expected .pyc path:        {expected_bytecode_path}")
    py_compile.compile(str(source_path), cfile=expected_bytecode_path, doraise=True)
    print(f"Bytecode file exists:      {Path(expected_bytecode_path).exists()}")


def show_code_objects():
    section("3. Code Objects")
    print(f"main function object:      {main}")
    print(f"main.__code__:             {main.__code__}")
    print(f"main code filename:        {main.__code__.co_filename}")
    print(f"main local variable names: {main.__code__.co_varnames}")
    print(f"main constants:            {main.__code__.co_consts}")

    section("4. Disassembled Bytecode For main()")
    dis.dis(main)


def main():
    message = "local data object"
    number = 2**100
    frame = inspect.currentframe()

    section("5. Runtime Namespaces")
    print(f"Module name __name__:      {__name__}")
    print(f"Global DATA value:         {DATA}")
    print(f"Global DATA id:            {id(DATA)}")
    print(f"Local message value:       {message}")
    print(f"Local message id:          {id(message)}")
    print(f"Local number value:        {number}")
    print(f"Local number id:           {id(number)}")

    section("6. Where Variables Live")
    print("A Python variable is a name in a namespace, not a fixed memory box.")
    print("DATA is a name in globals():")
    print(f"  globals()['DATA'] ->     {globals()['DATA']!r}")
    print("message and number are names in main()'s local frame:")
    print(f"  frame.f_locals ->        {frame.f_locals}")

    section("7. Object Types")
    print(f"type(DATA):                {type(DATA)}")
    print(f"type(message):             {type(message)}")
    print(f"type(number):              {type(number)}")
    print(f"Process id:                {os.getpid()}")


if __name__ == "__main__":
    show_runtime_paths()
    show_code_objects()
    main()
