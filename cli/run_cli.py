import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.hova.Runtime import (
    Forge,
    Dimen
)

from src.hova.ErrorsTreatments import (
    HovaContextError,
    HovaEmissionError,
    HovaSyntaxError,
    HovaTypeError
)




# CLI

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
        "-v",
        action="version",
        version=f'Hova v2.05 Stable'
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    
    # ------ forge --------
    forge = subparsers.add_parser(
        "forge",
        help="Convert a .hova file to JSON / YAML / TOML based on its atomic config."
    )
    
    forge.add_argument("file", help="Path of .hova file to be processed")
    forge.add_argument("-o", "--output", help="Output directory", default=None)
    forge.add_argument("-e", "--emit", help="Override emit type", choices=["json", "yaml", "toml"], default=None)
    forge.add_argument("-s", "--silent", action="store_true", help="Disable all output logs")


    # ----- dimen -----
    dimen = subparsers.add_parser(
        "dimen",
        help="Multi-convert of folders with .hova files. Its executed with 'main.hova' file"
    )
    
    dimen.add_argument("file", help="Path of 'main.hova' ot be processed")
    dimen.add_argument("-s", "--silent", action="store_true", help="Disable all output logs")




    args = parser.parse_args()
    
    if args.command == "forge": 
        handle_forge(args)
    
    elif args.command == "dimen": 
        handle_dimen(args)

    else:
        print("[Hova CLI Alert] Unknown Command")
        sys.exit(1)
     
     
        
# Execute .hova file
        
def handle_forge(args):
    file = args.file
    
    if not os.path.exists(file):
        print(f'[Hova CLI Alert] File not found: "{file}"')
        sys.exit(1)
        
    try:
        code = open(file, "r", encoding="utf-8").read()    
    except Exception as err:
        print(f'[Hova CLI Alert] Could not read "{file}":\n"{err}"')
        sys.exit(1)
        
    try:
        Forge(
            input=code, 
            output_dir=args.output, 
            force_emit=args.emit,
            silent=args.silent
        )
    except (HovaContextError, HovaEmissionError, HovaSyntaxError, HovaTypeError) as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)


def handle_dimen(args):
    file = args.file
    
    if not os.path.exists(file):
        print(f'[Hova CLI Alert] File not found: "{file}"')
        sys.exit(1)
        
    try:
        code = open(file, 'r', encoding='utf-8').read()
    except Exception as err:
        print(f'[Hova CLI Alert] Could not read "{file}":\n{err}')
        sys.exit(1)
        
        
    try:
        Dimen(
            input=code,
            silent=args.silent
        )
    except (HovaContextError, HovaEmissionError, HovaSyntaxError, HovaTypeError) as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
        
        
    
            
if __name__ == '__main__':
    main()