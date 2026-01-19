import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hova.Runtime import Forge

from src.hova.ErrorsTreatments import (
    HovaContextError,
    HovaEmissionError,
    HovaSyntaxError,
    HovaTypeError
)

def main():
    parser = argparse.ArgumentParser(
        prog="hova",
        description="Hova CLI — execute, convert and manage Hova files.",
        epilog="Example:\n hova forge world.hova\n hova forge settings.hova -o ./out",    
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    # hova --version
    parser.add_argument(
        "--version",
        action="version",
        version=f'Hova v1.95'
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    
    # ------ forge --------
    forge = subparsers.add_parser(
        "forge",
        help="Convert a .hova file to JSON / YAML / TOML based on its atomic config."
    )
    
    forge.add_argument(
        "file", 
        help="Path of .hova file to be processed"
    )
    
    forge.add_argument(
        "-o", "--output",
        help="Custom output directory",
        default=None
    )
    
    forge.add_argument(
        "-e", "--emit",
        help="Override emit type (json / yaml / toml)",
        choices=["json", "yaml", "toml"],
        default=None
    )

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    handle(args)

def handle(args):
    
    if args.command == "forge": 
        handle_forge(args)
        return 
    
    print('[Hova CLI Alert] Unknown Command')
    sys.exit(1)
        
def handle_forge(args):
    file = args.file
    
    if not os.path.exists(file):
        print(f'[Hova CLI Alert] File not found: {file}')
        sys.exit(1)
        
    try:
        code = open(file, "r", encoding="utf-8").read()    
    except Exception as err:
        print(f'[Hova CLI Alert] Could not read file:\n{err}')
        sys.exit(1)
        
    try:
        Forge(
            input=code, 
            output_dir=args.output, 
            force_emit=args.emit
        )
    except HovaTypeError as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
    except HovaContextError as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
    except HovaEmissionError as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
    except HovaSyntaxError as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
        
        
if __name__ == '__main__':
    main()