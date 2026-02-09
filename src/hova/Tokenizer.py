from .TokenClass import Token
from .ErrorsTreatments import HovaSyntaxError
from .Utils import (
    KEYWORDS,
    TYPES,
    SYMBOLS
)


class Scanner:
    def __init__(self, code):
        self.code = code
        self.index = 0
        self.ln = 1
        self.col = 0
        
        
    def peek(self):
        return self.code[self.index] if self.index < len(self.code) else None
    
    def next(self):
        return self.code[self.index + 1] if self.index + 1 < len(self.code) else None
    
    def advance(self):
        char = self.peek()
        
        if char == '\n':
            self.ln += 1
            self.col = 0
        else:
            self.col += 1
            
        self.index += 1
        return char
    
    
def Tokenizer(code):
    scan = Scanner(code)
    tokens = []
    
    def scan_identifier(scan):
        start_ln, start_col = scan.ln, scan.col
        value = ""
        
        while scan.peek() and (scan.peek().isalnum() or scan.peek() == "_"):
            value += scan.advance()
            
        token_type = (
            "KEYWORD" if value.lower() in KEYWORDS
            else "TYPE" if value.lower() in TYPES
            else "IDENTIFIER"
        )
        
        return Token(token_type, value, start_ln, start_col, scan.ln, scan.col)
    
    
    def scan_number(scan):
        start_ln, start_col = scan.ln, scan.col
        value = ""
        has_dot = False
        
        while scan.peek() and (scan.peek().isdigit() or scan.peek() == '.'):
            curr_char = scan.peek()
            next_char = scan.next()
        
            if curr_char.isdigit():
                value += curr_char
                scan.advance()
                continue
                
            if curr_char == '.' and next_char and next_char.isdigit() and not has_dot:
                value += curr_char
                scan.advance()
                has_dot = True
                continue
            
            break
                
        token_type = "NUMBER_FLOATING" if has_dot else "NUMBER_INTEGER"
        return Token(token_type, value, start_ln, start_col, scan.ln, scan.col)
        
        
    def scan_string(scan):
        start_ln, start_col = scan.ln, scan.col 
        
        quote = scan.peek()
        scan.advance()
        
        value = ""
        
        while scan.peek() and not scan.peek() == quote:
            curr_char = scan.peek()
            value += curr_char
            scan.advance()
            
        scan.advance()
        
        return Token("STRING", value, start_ln, start_col, scan.ln, scan.col)

    
    def scan_commentary(scan):
        scan.advance() # get .
        scan.advance() # get .
        
        while not scan.peek() == "\n":
            scan.advance()
         
                     
    def scan_symbol(scan):
        start_ln, start_col = scan.ln, scan.col
        value = scan.peek()
        
        return Token("SYMBOL", value, start_ln, start_col, scan.ln, scan.col)
    
    
    
    
    while scan.peek() is not None:
        
        char = scan.peek()
        
        if char.isspace():
            scan.advance()
            continue
        
        if char.isalpha() or char == '_':
            tokens.append(scan_identifier(scan))  
            continue
            
        if char.isdigit():
            tokens.append(scan_number(scan))
            continue    
        
        if char in SYMBOLS:
            tokens.append(scan_symbol(scan))
            scan.advance()
            continue
        
        if char in ("'", '"'):
            tokens.append(scan_string(scan))
            continue
        
        if char == "." and scan.next() == ".":
            scan_commentary(scan)
            continue
        
        raise HovaSyntaxError(
            f'Unexpected character {char}',
            scan.ln,
            scan.col
        )          
    
    return tokens