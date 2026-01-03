from src.Tokenizer import Tokenizer
from src.Parser import Parser
from src.Emitter import Emitter
from src.Interpreter import FunctionInterpreter

from src.ToMarkdown import AnvilToMarkdown
from src.ToINI import ToINI

from pathlib import Path
from yaml import dump
import json
import toml

from .ErrorsTreatments import HovaError


DEV_TEST = [False, ""]


# NOTE: Hova 0.1.8 -> 2026 January, 3
# NOTE: Hova 0.1.9 -> Soon ... (0 ) _ (0 )

# code = """
# """

def Forge(input, output_dir=None, force_emit=None):
    
    tokens = Tokenizer(input)


    # If input is empty
    if len(tokens) == 0:
        return HovaError('100', 'Hova File is empty').Log()
        
    # If there are reppetitive specific keywords
    justKeyword = [token.value if token.type == "KEYWORD" else 0 for token in tokens]
    
    if justKeyword.count("anvil") > 1:
        return HovaError("100", "Hova file must have only one 'AnvilEncompass'").Log()
        
        
    if justKeyword.count("charm") > 1:
        return HovaError("100", "Hova file must have only one 'CharmEncompass'").Log()
    
    
    if justKeyword.count("atomic") > 1:
        return HovaError("100", "Hova file must have only one 'AtomicEncompass'").Log()
    
    
    nodeAST = Parser(tokens)
    Interpreted = []
    AnvilData = {}
    Runes = {}
    Tempers = {}

    if isinstance(nodeAST, HovaError): 
        nodeAST.Log()
        return

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
            Interpreted.append(FunctionInterpreter(node, Runes, Tempers))
            
        for item in Interpreted:
            if item in ('CharmInterpreted', 'TemperInterpreted'):
                continue

            AnvilData = item
            
        # Emitter: This convert all AST_NODES to Dictionaries with { key:value } to best readable of the conversors
        emitted = Emitter(AnvilData, True) 
        
        if isinstance(emitted, HovaError):
            emitted.Log()
            return
        
        anvilStruct = emitted['anvilData']
        emitterConfig = emitted['emitterConfigData']

        # OUT HOVA 
        out_dir_hova = Path(f'outHova')
        out_dir_hova.mkdir(exist_ok=True)

        root_name = next(iter(anvilStruct))
        emitData = list(anvilStruct.values())[0]
        
        if emitData["atomic"] == {}:
            return HovaError('500', f'Expected an "atomic" inside the anvil "{list(emitted.keys())[0]}".').Log()
        
        atomicKeys = [k for k in emitData['atomic']]
        
        if not force_emit:
            if not "emit" in atomicKeys:
                return HovaError('500', "EmitType not defined. Put it inside an \"atomic\": 'atom emit : \"<filetype>\"'.").Log()
        
        root_type = emitData["atomic"]["emit"] if not force_emit else force_emit
        
        if force_emit is not None:
            anvilStruct[root_name]['atomic']['emit'] = force_emit
        
        if emitterConfig['hova']['encompass']['hideAtomic'] == 'on':
            del anvilStruct[root_name]['atomic']
            

        if not str(root_type).lower() in ("json", "yaml", "toml"):
            return HovaError('500', "Expected the correct EmitteDestiny. Use 'json', 'yaml', 'toml'").Log()

        directoryNameByType = out_dir_hova / Path(str(root_type).capitalize())
        directoryNameByType.mkdir(exist_ok=True)
        
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

        with file_path.open("w", encoding="utf-8") as file:

            if root_type == "json": json.dump(anvilStruct, file, indent=4, ensure_ascii=False) 
            if root_type == "yaml": dump(anvilStruct, file, allow_unicode=True, sort_keys=False)
            if root_type == "toml": toml.dump(anvilStruct, file)

            print(f'[Hova Successfully] "{str(root_name).split('.')[0]}" was created as {str(root_type).upper()}!')
        