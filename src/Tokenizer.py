# Annotations
# @anchor -> Show as favourite
# @deprecated -> Show Info in Terminal
# @hidden -> Hidden from Emitter to ignore
import re

KEYWORDS = [
    "anvil", "ore", "charm", "atomic", "temper",
    "spark", "rune", "atom", "det", # to Encompass 
    "end", "by", "be", # to pass
    "seal", "reject", "mark", # annotations
    "true", "false",
    "hova"
]

SYMBOLS = set("&@!()[],.:")
TYPES = ["int", "float", "str", "bool", "list"]

class Token:
    def __init__(self, type, value, ln):
        self.type = type
        self.value = value
        self.ln = ln
        
        
def Tokenizer(Code):
    Tokens = []
    Current = ""
    CurrentType = None
    
    i = 0
    ln = 1
    
    length = len(Code)
    
    def flush():
        nonlocal Current, CurrentType, Tokens
        
        if not Current:
            return
        
        if str(Current).lower() in KEYWORDS:
            Tokens.append(
                Token( 
                    "KEYWORD", 
                    str(Current).lower(),
                    ln,
                )
            )
            
        elif str(Current).lower() in TYPES:
            Tokens.append(
                Token(
                    "TYPE",
                    Current,
                    ln
                )
            )
        elif Current.replace("_", "").isalnum() or Current.isalnum():
            Tokens.append(
                Token( 
                    "IDENTIFIER", 
                    Current,
                    ln,
                )
            )
        else:
            Tokens.append(
                Token(
                    CurrentType, 
                    Current,
                    ln,
                )
            )
            
        Current = ""
        CurrentType = None
    
    
    while i < length:
        char = Code[i]
        
        if char == '\n':
            ln += 1
        
        if char.isspace():
            flush()
            i += 1
            continue

        elif char == "." and i + 1 < length and Code[i + 1] == ".":
            i += 2
            while i < length and Code[i] != "\n":
                i += 1
            continue
        
        elif char == "." and i + 1 < length and Code[i + 1] == "/":
            i += 2
            
            while i < length and not (Code[i] == "/" and i + 1 < length and Code[i + 1] == "."):
                i += 1
            i += 2
            continue
        
        elif char in SYMBOLS:
            flush()
            Tokens.append(
                Token(
                    "SYMBOL",
                    char,
                    ln,
                )
            )
            
            i += 1
            continue
        
        elif char in ('"', "'"):
            flush()
            
            quote = char
            i += 1
            Value = ""
            
            while i < length and Code[i] != quote:
                Value += Code[i]
                i += 1
                
            i += 1
            Tokens.append(
                Token(
                    "STRING",
                    Value,
                    ln,
                )
            )
            continue
        
        elif char.isdigit():
            flush()
            value = ""
            has_dot = False
            
            while i < length and (Code[i].isdigit() or Code[i] == "."):
                if Code[i] == ".":
                    if has_dot: 
                        break
                    
                    if not (i + 1 < length and Code[i + 1].isdigit()):
                        break
                
                    has_dot = True
                
                value += Code[i]
                i += 1 
                
            Tokens.append(
                Token(
                    "NUMBER_FLOATING" if has_dot else "NUMBER_INTEGER",
                    value,
                    ln,
                )
            )
            continue        
            
        elif char.isalpha() or char.isdigit() or char == "_":
            flush()
            CurrentType = "IDENTIFIER"
            Current += char
            i += 1
            
            while i < length and (Code[i].isalnum() or Code[i] == "_"):
                Current += Code[i]
                i += 1
            
            flush()
            Current = ""
            continue
            
        # FALLBACK
        i += 1
    
    return Tokens


    