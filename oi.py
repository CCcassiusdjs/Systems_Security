import importlib

try:
    importlib.util.find_spec('pycipher')
    print("pycipher library is installed.")
except ImportError:
    print("pycipher library is not installed.")