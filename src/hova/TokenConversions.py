from .Tokenizer import Token

def Literal(type, value, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": type,
        "value": value,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    
def Identifier(name, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "Identifier",
        "name": name,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    
def Spark(name, type, value, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "Spark",
        "valType": type,
        "name": name,
        "value": value,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    
def Atom(name, value, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "Atom",
        "name": name,
        "value": value,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }

    
def Seal(name, args=None, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "Seal",
        "name": name,
        "args": args,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    

# EncompassConverters
     
def AnvilEncompass(name, atomic, children, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "AnvilEncompass",
        "name": name,
        "atomic": atomic,
        "children": children,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }

def OreEncompass(seals, name, sparks, child_ores, abstract, mimic_from, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "OreEncompass",
        "abstract": abstract,
        "mimic_from": mimic_from,
        "name": name,
        "seals": seals,
        "sparks": sparks,
        "child_ores": child_ores,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }

def AtomicEncompass(atoms, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "AtomicEncompass",
        "atoms": atoms,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }

def CallFunction(callee, param=None, args=[], start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "CallFunction",
        "callee": callee,
        "param": param,
        "args": args,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    
def NamespaceEmitter(props, val, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "NamespaceEmit",
        "props": props,
        "val": val,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }

    
def CaveEncompass(name:Token, children, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "CaveEncompass",
        "name": name,
        "ores": children,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }
    
    
def Dimension(path, start_ln:int=None, start_col:int=None, end_ln:int=None, end_col:int=None) -> dict:
    return {
        "type": "Dimension",
        "path": path,
        "start_ln": start_ln,
        "start_col": start_col,
        "end_ln": end_ln,
        "end_col": end_col
    }