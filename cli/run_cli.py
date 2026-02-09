import argparse
import sys
import os
import shutil
import requests
import platform



# System Info

system = platform.system().lower() # windows / linux / darwin
machine = platform.machine().lower()

current_exe_path = sys.argv[0]


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
        version=f'Hova v2.0'
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

    dimen = subparsers.add_parser(
        "dimen",
        help="Multi-convert of folders with .hova files. Its executed with 'main.hova' file"
    )
    
    dimen.add_argument("file", help="Path of 'main.hova' ot be processed")


    subparsers.add_parser(
        "upgrade",
        help="Download and replace the binary with the newest version published on Github."
    )

    args = parser.parse_args()
    
    if args.command == "forge":
        handle_forge(args)
    if args.command == "dimen":
        handle_dimen(args)
    elif args.command == "upgrade":
        handle_upgrade()
    else:
        print("[Hova CLI Alert] Unknown Command")
        sys.exit(1)
     
     
        
# Execute .hova file
        
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
    except (HovaContextError, HovaEmissionError, HovaSyntaxError, HovaTypeError) as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)


def handle_dimen(args):
    file = args.file
    
    if not os.path.exists(file):
        print(f'[Hova CLI Alert] File not found: {file}')
        sys.exit(1)
        
    try:
        code = open(file, 'r', encoding='utf-8').read()
    except Exception as err:
        print(f'[Hova CLI Alert] Could not read file:\n{err}')
        sys.exit(1)
        
        
    try:
        Dimen(input=code)
    except (HovaContextError, HovaEmissionError, HovaSyntaxError, HovaTypeError) as err:
        print(f'{err.message} - ln {err.line}, col {err.col}')
        sys.exit(1)
        
        
    
         


# Download new binary

def get_url_asset(system, machine):
    try:
        
        release = requests.get(
            "https://api.github.com/repos/G4brielXavier/hova-api-upgrade/releases/latest",
            timeout=10
        ).json()
        
    except Exception as err:
        raise Exception(f'Could not fetch release info: {err}')
        
    
    target_name = f'hova-{system}-{machine}'
    if system == "windows":
        target_name += ".exe"
        
    for asset in release["assets"]:
        if asset["name"] == target_name:
            return asset["browser_download_url"]
        
        
    raise Exception("Binary not found in release")

def handle_upgrade():
    print("[Hova CLI] Checking latest version...")
    
    try:
        url = get_url_asset(system, machine)
    except Exception as err:
        print(f'[Hova CLI Alert] {err}')
        sys.exit(1)
    
    print(f'[Hova CLI] Downloading new binary...')
    
    try:
        binary = requests.get(url).content
    except Exception as err:
        print(f'[Hova CLI Alert] Could not download binary:\n {err}')
        sys.exit(1)
    
    tmp_path = current_exe_path + ".tmp"
    
    try:
        
        with open(tmp_path + ".tmp", "wb") as f:
            f.write(binary)
            
    except Exception as err:
        print(f'[Hova CLI Alert] Could not write temp binary: \n{err}')
        sys.exit(1)
        
    try:
        
        backup_path = current_exe_path = ".old"
        
        if os.path.exists(backup_path):
            os.remove(backup_path)
            
        os.rename(current_exe_path, backup_path)
        shutil.move(tmp_path, current_exe_path)
        
        print("[Hova CLI] Upgrade Complete!")
        print(f"Previous version backed up as: {backup_path}")
        
    except Exception as err:
        print(f'[Hova CLI Alert] Could not replace binary:\n{err}')
        sys.exit(1)
   
if __name__ == '__main__':
    main()