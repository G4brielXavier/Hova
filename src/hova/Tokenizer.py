
KEYWORDS = [
    "anvil", "ore", "atomic", "temper", "cave", # encompass 
    "spark", "rune", "atom", # definers 
    "end", # block
    "seal", "reject", "mark", # seals
    "true", "false", # booleans
]

SYMBOLS = set("&@!()[],.:")
TYPES = ["int", "float", "str", "bool", "list"]

class Token:
    def __init__(self, type, value, ln, col):
        self.type = type
        self.value = value
        self.ln = ln
        self.col = col
        
        
def Tokenizer(Code):
    Tokens = []
    Current = ""
    CurrentType = None
    
    i = 0
    ln = 1
    col = 0
    start_col = None
    
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
                    col
                )
            )
            
        elif str(Current).lower() in TYPES:
            Tokens.append(
                Token(
                    "TYPE",
                    Current,
                    ln,
                    col
                )
            )
        elif Current.replace("_", "").isalnum() or Current.isalnum():
            Tokens.append(
                Token( 
                    "IDENTIFIER", 
                    Current,
                    ln,
                    col
                )
            )
        else:
            Tokens.append(
                Token(
                    CurrentType, 
                    Current,
                    ln,
                    col
                )
            )
            
        Current = ""
        CurrentType = None
    
    def WhileTokens():
        nonlocal start_col, CurrentType, i, ln, col, Current
        
        while i < length:

            char = Code[i]
            
            if char == '\n':
                ln += 1
                col = 0
            
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
                        col
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
                        col
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
                        col
                    )
                )
                continue        
                
            elif char.isalpha() or char.isdigit() or char == "_":
                
                flush()
                CurrentType = "IDENTIFIER"
                start_col = col
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
            col += 1
    
    WhileTokens()

    return Tokens


    