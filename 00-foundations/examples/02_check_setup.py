"""
Sanity-check your Python environment.

Run me:
    python 00-foundations/examples/02_check_setup.py
"""

import sys
import platform


def main() -> None:
    print("=== Python environment ===")
    print(f"Version:    {sys.version.split()[0]}")
    print(f"Executable: {sys.executable}")
    print(f"Platform:   {platform.platform()}")
    print()

    print("=== Optional libraries ===")
    for pkg in ("numpy", "pandas", "matplotlib", "pytest", "ipython"):
        try:
            mod = __import__(pkg)
            version = getattr(mod, "__version__", "unknown")
            print(f"  [OK]  {pkg:12s} {version}")
        except ImportError:
            print(f"  [--]  {pkg:12s} not installed")

    print()
    if sys.version_info < (3, 11):
        print("WARNING: This curriculum targets Python 3.11+. Consider upgrading.")
    else:
        print("Python version is good. You are set up.")


if __name__ == "__main__":
    main()
