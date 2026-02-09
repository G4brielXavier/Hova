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

# Imports to conversions
from pathlib import Path
from yaml import dump
import json
import toml

# Path controls
import os
import pathlib
import shutil 
import re

# Hova errors imports
from .ErrorsTreatments import (
    HovaEmissionError,
    IsError
)


DEV_TEST = [False, ""]


# NOTE: Hova 1.0 - 1.7 -> 2025 December, 3 - 31
# NOTE: Hova 1.8 -> 2026 January, 3 
# NOTE: Hova 1.9 -> 2026 January, 15 - "Hova is not big because has many features. It is big because not try be what not it is."
# NOTE: Hova 1.95 -> 2026 January, 19
# NOTE: Hova 2.00 -> 2026 February, 07


def Conversior(root_type, root_name, anvilStruct, file_path):
    with file_path.open("w", encoding="utf-8") as file:

        if root_type == "json": json.dump(anvilStruct, file, indent=4, ensure_ascii=False) 
        if root_type == "yaml": dump(anvilStruct, file, allow_unicode=True, sort_keys=False)
        if root_type == "toml": toml.dump(anvilStruct, file)

        print(f'[Hova Emitter] "{str(root_name).split('.')[0]}" was created as {str(root_type).upper()}!')


def Forge(input, output_dir=None, force_emit=None, returnAST=False, giveForgeInfo=False):
    
    tokens = Tokenizer(input)



    # If input is empty
    
    if len(tokens) == 0:
        raise HovaEmissionError('Hova File is empty', 0, 0)
    
    
            
    # If there are repetitions of specific keywords
    
    justKeyword = [token.value if token.type == "KEYWORD" else 0 for token in tokens]
    
    if justKeyword.count("anvil") > 1:
        raise HovaEmissionError("Hova file must have only one 'AnvilEncompass'", 0, 0)
    
    if justKeyword.count("atomic") > 1:
        raise HovaEmissionError("Hova file must have only one 'AtomicEncompass'", 0, 0)
    
    
    
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
            raise HovaEmissionError("Expected the correct EmitteDestiny. Use 'json', 'yaml', 'toml'", 0, 0)



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
        Conversior(
            root_type=root_type,
            root_name=root_name,
            anvilStruct=anvilStruct,
            file_path=file_path
        )
            
     
def Dimen(input):
    
    ast = Forge(input=input, returnAST=True)
    
    # 1. hova dimen main.hova
    # 2. read each line from main.hova file (Tokenizer, Parser) with Forge()
        # - I need read "dimension /path"
    # 3. Get the AST
    # 4. Get the folder with (path)
        # - Verify if exists with os.path.exists
        # - Open the directory and "Forge"
        # - Forge each .hova file
        
    structured_dimension = {}

    structure = """
    It will be converted by the converters
    
    {
        "foldername" : {
            "hovafilename": "ast_to_convert"
        }   
    }
    """
    
    for node in ast:
        
        if not os.path.exists(node['path']):
            print(f'[Hova Dimen] "{node['path']}" not exist as directory')
            return
        
        path = Path(node['path'])
        structured_dimension[node['path']] = []
        
        for file_path in path.iterdir():
            if file_path.is_file():
                try:
                    
                    with open(file_path, 'r', encoding="utf-8") as file:
                        content = file.read()
                        structured_dimension[node['path']].append({ "filename": file_path, "content": content })
                    
                except IOError as err:
                    print(f'[Hova Dimen] Error reading "{file_path}": {err}')
                    
                
        for foldername, files in structured_dimension.items():
            
            out_dir_hova = Path('hovabuild')
            out_dir_hova.mkdir(exist_ok=True)
            
            main_folder = out_dir_hova / Path(foldername)
            main_folder.mkdir(exist_ok=True)
            
            for file in files:
                filepath = out_dir_hova / file['filename']
                filecontent = file['content']
                
                
                struct_info_forge = Forge(
                    input=filecontent,
                    output_dir=None,
                    force_emit=None,
                    giveForgeInfo=True
                )
                
                new_filepath_regex =  re.sub(r"\bhova\b", struct_info_forge["root_type"], str(filepath))
                new_filepath = Path(new_filepath_regex)
                
                Conversior(
                    root_type=struct_info_forge['root_type'],
                    root_name=struct_info_forge['root_name'],
                    anvilStruct=struct_info_forge['anvilStruct'],
                    file_path=new_filepath
                )

                
                
    return