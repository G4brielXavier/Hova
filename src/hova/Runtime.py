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


def Forge(input, output_dir=None, force_emit=None):
    
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
    
    
    nodeAST = Parser(tokens) # Tokens -> AST
    Interpreted = []
    AnvilData = {}
    
    if IsError(nodeAST): raise nodeAST

    # DEBUG TOKENIZER
    if DEV_TEST[0] is True and DEV_TEST[1] == "T":
        for token in tokens:
            print(f'{token.type}: {token.value} - at line {token.ln}')
    
    # DEBUG PARSER
    if DEV_TEST[0] is True and DEV_TEST[1] == "P":
        for node in nodeAST:
            print()
            print(node)
            print()
        

    # Emitter Exec
    if DEV_TEST[0] is False and DEV_TEST[1] == "":
        
        # Get AST Interpreted
        for node in nodeAST:
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
        with file_path.open("w", encoding="utf-8") as file:

            if root_type == "json": json.dump(anvilStruct, file, indent=4, ensure_ascii=False) 
            if root_type == "yaml": dump(anvilStruct, file, allow_unicode=True, sort_keys=False)
            if root_type == "toml": toml.dump(anvilStruct, file)

            print(f'[Hova Emitter] "{str(root_name).split('.')[0]}" was created as {str(root_type).upper()}!')