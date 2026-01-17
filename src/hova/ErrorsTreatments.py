class HovaError(Exception):
    def __init__(self, message:str, line:any=None, col:any=None):
        self.message = message
        self.line = line - 1
        self.col = col
        
class HovaSyntaxError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
        
class HovaContextError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
        
class HovaTypeError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
        
class HovaReferenceError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
        
class HovaEmissionError(HovaError):
    def __init__(self, message:str, line:any=None, col:any=None):
        super().__init__(message, line, col)
        
def IsError(code):
    return True if isinstance(code, HovaError) else False