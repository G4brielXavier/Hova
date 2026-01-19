from .Tokenizer import Token

def Literal(type, value, line:int=None, col:int=None) -> dict:
    return {
        "type": type,
        "value": value,
        "line": line,
        "col": col
    }
    
def Identifier(name, line:int=None, col:int=None) -> dict:
    return {
        "type": "Identifier",
        "name": name,
        "line": line,
        "col": col
    }
    
def Spark(name, type, value, line:int=None, col:int=None) -> dict:
    return {
        "type": "Spark",
        "valType": type,
        "name": name,
        "value": value,
        "line": line,
        "col": col
    }
    
def Atom(name, value, line:int=None, col:int=None) -> dict:
    return {
        "type": "Atom",
        "name": name,
        "value": value,
        "line": line,
        "col": col
    }

    
def Seal(name, args=None, line:int=None, col:int=None) -> dict:
    return {
        "type": "Seal",
        "name": name,
        "args": args,
        "line": line,
        "col": col,
    }
    

# EncompassConverters
     
def AnvilEncompass(name, atomic, children, line:int=None, col:int=None) -> dict:
    return {
        "type": "AnvilEncompass",
        "name": name,
        "atomic": atomic,
        "children": children,
        "line": line,
        "col": col
    }

def OreEncompass(seals, name, sparks, child_ores, line:int=None, col:int=None) -> dict:
    return {
        "type": "OreEncompass",
        "name": name,
        "seals": seals,
        "sparks": sparks,
        "child_ores": child_ores,
        "line": line,
        "col": col
    }

def AtomicEncompass(atoms, line:int=None, col:int=None) -> dict:
    return {
        "type": "AtomicEncompass",
        "atoms": atoms,
        "line": line,
        "col": col
    }

def CallFunction(callee, param=None, args=[], line:int=None, col:int=None) -> dict:
    return {
        "type": "CallFunction",
        "callee": callee,
        "param": param,
        "args": args,
        "line": line,
        "col": col
    }
    
def NamespaceEmitter(props, val, line:int=None, col:int=None) -> dict:
    return {
        "type": "NamespaceEmit",
        "props": props,
        "val": val,
        "line": line,
        "col": col
    }

    
def CaveEncompass(name:Token, children, line:int=None, col:int=None) -> dict:
    return {
        "type": "CaveEncompass",
        "name": name,
        "ores": children,
        "line": line,
        "col": col
    }