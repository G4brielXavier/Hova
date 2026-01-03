import argparse
import sys
import os

from src.Runtime import Forge

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
        version=f'Hova v0.1.8'
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
        "--emit",
        help="Override emit type (json / yaml / toml)",
        choices=["json", "yaml", "toml"],
        default=None
    )
    
    forge.add_argument(
        "--silent",
        action="store_true",
        help="Suppress logs and just process"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    handle(args)

def handle(args):
    
    if args.command == "forge": handle_forge(args)
    
    print('Unknown command')
    sys.exit(1)
        
        

def handle_forge(args):
    file = args.file
    
    if not os.path.exists(file):
        print(f'[Hova CLI] File not found: {file}')
        sys.exit(1)
        
    try:
        code = open(file, "r", enconding="utf-8").read()    
    except Exception as err:
        print(f'[Hova CLI Error] Could not read file:\n{err}')
        sys.exit(1)
        
    if not args.silent:
        print(f'⚒️  Forging: {file}')
        
    try:
        Forge(code, output_dir=args.output, force_emit=args.emit)
    except Exception as err:
        print("\n Forge Failed!")
        print(err)
        sys.exit(1)
    
    if not args.silent:
        print("Done!")
        