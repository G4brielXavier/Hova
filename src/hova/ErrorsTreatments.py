class HovaError(Exception):
    def __init__(self, message:str, line:any=None, col:any=None):
        self.message = message
        self.line = line - 1
        self.col = col

# for Syntax errors that occurs in code
class HovaSyntaxError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
# for Context errors alert if an ore is outside an anvil or spark is outside an ore
class HovaContextError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
# for Type errors if a spark value is different from what was defined
class HovaTypeError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
# for errors that occurs in Emission's time
class HovaEmissionError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
        
# function that verify If is an error or not
def IsError(code):
    return True if isinstance(code, HovaError) else False