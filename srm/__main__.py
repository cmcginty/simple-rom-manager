"""
Default module run when importing the package from the command line and also the main entry point
defined in setup.py.  Ex:

    python3 -m srm
"""
import sys


def main():
    """Program entry point."""
    print('Starting SRM...')
    sys.exit()

if __name__ == '__main__':
    main()
