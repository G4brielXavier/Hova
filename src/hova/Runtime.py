# RUNTIME
# Its the file where the hova starts to be analized
# Steps
# 1. Input
# 2. Tokenizer
# 3. Parser
# 4. Interpreter
# 5. Emitter
# 6. Convertion 
# 7. Out

# Imports from Hova
from .Tokenizer import Tokenizer
from .Parser import Parser
from .Emitter import Emitter
from .Interpreter import FunctionInterpreter
from .Writter import Writter

# Imports to conversions
from pathlib import Path
from yaml import dump
import json
import toml

# Path controls
import os
import re

# Hova errors imports
from .ErrorsTreatments import (
    HovaEmissionError,
    IsError
)


DEV_TEST = [False, ""]

logmain = Writter()
logrun = Writter()
logdimen = Writter()

# NOTE: Hova 1.0 - 1.7 -> 2025 December, 3 - 31
# NOTE: Hova 1.8 -> 2026 January, 3 
# NOTE: Hova 1.9 -> 2026 January, 15 - "Hova is not big because has many features. It is big because not try be what not it is."
# NOTE: Hova 1.95 -> 2026 January, 19
# NOTE: Hova 2.05 -> 2026 February, 07
# NOTE: Hova 3.0 -> 2026


def Converter(root_type, root_name, anvilStruct, file_path, silent=False):
    with file_path.open("w", encoding="utf-8") as file:

        if root_type == "json": json.dump(anvilStruct, file, indent=4, ensure_ascii=False) 
        if root_type == "yaml": dump(anvilStruct, file, allow_unicode=True, sort_keys=False)
        if root_type == "toml": toml.dump(anvilStruct, file)
        
        if not silent:
            logmain.SayMain(f'[Hova Converter] "{str(root_name).split('.')[0]}" was created as {str(root_type).upper()}!')
            print()

def Forge(input, output_dir=None, force_emit=None, returnAST=False, giveForgeInfo=False, silent=False):
    
    if not giveForgeInfo:
        logrun.silent = silent
    else:
        logrun.silent = True

    logrun.SayMain("[Hova Forge] Forge Initiated!")
    print()
    
    tokens = Tokenizer(input)


    # If input is empty
    
    if len(tokens) == 0:
        logrun.SayError("Hova file is empty")
        return
    
    
            
    # If there are repetitions of specific keywords
    
    justKeyword = [token.value if token.type == "KEYWORD" else 0 for token in tokens]
    
    if justKeyword.count("anvil") > 1:
        logmain.SayError("Hova file must have only one 'AnvilEncompass'")
        return
    
    if justKeyword.count("atomic") > 1:
        logmain.SayError("Hova file must have only one 'AtomicEncompass'")
        return
    
    # Main Process
    
    NodeAST = Parser(tokens) # Tokens -> AST
    
    if (returnAST): return NodeAST
    
    Interpreted = []
    AnvilData = {}
    
    if IsError(NodeAST): raise NodeAST



    # Debug Tokenizer
    
    if DEV_TEST[0] is True and DEV_TEST[1] == "T":
        for token in tokens:
            print(f'{token.type}: {token.value}')
            
        return
    
    
    
    # Debug Parser
    
    if DEV_TEST[0] is True and DEV_TEST[1] == "P":
        for node in NodeAST:
            print()
            print(node)
            print()
            
        return
        


    # Emitter Time Execution
    
    if DEV_TEST[0] is False and DEV_TEST[1] == "":
        
        
        # Get AST Interpreted
        
        for node in NodeAST:
            Interpreted.append(FunctionInterpreter(node))
            
        for item in Interpreted:
            AnvilData = item
        
        
        
        # Emitter: This convert all AST_NODES to Dictionaries with { key:value } to best readability of the conversors
        
        emitted = Emitter(AnvilData, canUpdate=True) 
        
        
        if IsError(emitted): raise emitted
        
        anvilStruct = emitted['anvilData'] # Anvil informations
        emitterConfig = emitted['emitterConfigData'] # Atomic Configs 



        # Create the 'hovabuild' directory

        out_dir_hova = Path(f'hovabuild')
        out_dir_hova.mkdir(exist_ok=True)

        root_name = next(iter(anvilStruct)) # Filename
        
        logrun.SayLog(f'Forging "{root_name}"...')
        
        emitData = list(anvilStruct.values())[0]
        
        atomicKeys = [k for k in emitData['atomic']]


        
        # Get the Emit file type from Atomic or 'force_emit' param.

        root_type = emitData["atomic"]["emit"] if not force_emit else force_emit


        if giveForgeInfo:
            return {
                "anvilStruct": anvilStruct,
                "root_type": root_type,
                "root_name": root_name
            }

        
        if force_emit is not None:
            anvilStruct[root_name]['atomic']['emit'] = force_emit
        
        if emitterConfig['hideAtomic'] == 'on':
            del anvilStruct[root_name]['atomic']
            

        if not str(root_type).lower() in ("json", "yaml", "toml"):
            logrun.SayError("Expected the correct file type to emite. Use 'json', 'yaml', or 'toml'")
            return



        # Create and put the file type folder inside of 'hovabuild' folder

        directoryNameByType = out_dir_hova / Path(str(root_type).lower())
        directoryNameByType.mkdir(exist_ok=True)


        
        # Verify If the 'outDir' was setted inside AtomicEncompass or 'output_dir' in Forge's params 

        directoryAnvil = None
        directoryAnvilDefined = None
        
        if not output_dir and not "outDir" in atomicKeys:
            directoryAnvil = directoryNameByType
        else:
            directoryAnvilDefined = emitData["atomic"]["outDir"] if not output_dir else output_dir
            directoryAnvil = directoryNameByType / Path(directoryAnvilDefined)
            directoryAnvil.mkdir(exist_ok=True)

        safe_name = "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in root_name).strip()
        file_path = directoryAnvil / f'{safe_name}.{root_type}'



        # Get the all data and 'dump' to converts for the file type setted
        Converter(
            root_type=root_type,
            root_name=root_name,
            anvilStruct=anvilStruct,
            file_path=file_path, 
        )
                
def Dimen(input, silent=False):
    

    logdimen.silent = silent
    
    logdimen.SayMain("[Hova Dimen] Entering the Dimension!")
    print()
    
    ast = Forge(input=input, returnAST=True)
    
    # 1. hova dimen main.hova
    # 2. read each line from main.hova file (Tokenizer, Parser) with Forge()
        # - I need read "dimension /path"
    # 3. Get the AST
    # 4. Get the folder with (path)
        # - Verify if exists with os.path.exists
        # - Open the directory and "Forge"
        # - Forge each .hova file
    
    dimensions = []
    
    for node in ast:
        
        if not os.path.exists(node['path']):
            logdimen.SayError(f'[Hova Dimen] "{node['path']}" not exist as directory')
            return
        
        dimensions.append(node['path'])
        
    for foldername in dimensions:
        path = Path(foldername)
        files = []
        
        for file_path in path.iterdir():
            if file_path.is_file():
                try:
                    
                    with open(file_path, 'r', encoding="utf-8") as file:
                        files.append({ "filename": file_path, "content": file.read() })
                    
                except IOError as err:
                    logdimen.SayError(f'[Hova Dimen] Error reading "{file_path}": {err}')
                    
            
        logdimen.SayLog(f'[Hova Dimen] Extrating "{foldername}" dimension...')
            
        out_dir_hova = Path('hovabuild')
        out_dir_hova.mkdir(exist_ok=True)
        
        main_folder = out_dir_hova / Path(foldername)
        main_folder.mkdir(exist_ok=True)
        
        
        for file in files:
            logdimen.SayLog("[Hova Dimen > Forge] Waiting the forge finish...")
            
            filepath = out_dir_hova / file['filename']
            filecontent = file['content']
            
            info = Forge(
                input=filecontent,
                output_dir=None,
                force_emit=None,
                giveForgeInfo=True
            )
            
            if not info:
                logdimen.SayError("[Hova Dimen Alert] Ocurred an error in the process.")
                return
            
            new_filepath_regex =  re.sub(r"\bhova\b", info["root_type"], str(filepath))
            new_filepath = Path(new_filepath_regex)
            
            Converter(
                root_type=info['root_type'],
                root_name=info['root_name'],
                anvilStruct=info['anvilStruct'],
                file_path=new_filepath
            )
            
        logdimen.SayMain(f'[Hova Dimen] Dimension "{foldername}" Successfully issued!')
        print()
        
       
    return