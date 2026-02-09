class HovaError(Exception):
    def __init__(self, message:str, start_ln:any=None, start_col:any=None, end_ln:any=None, end_col:any=None):
        self.message = message
        self.start_ln = start_ln - 1
        self.start_col = start_col
        self.end_ln = end_ln
        self.end_col = end_col

# for Syntax errors that occurs in code
class HovaSyntaxError(HovaError):
    def __init__(self, message:str, start_ln:any=None, start_col:any=None, end_ln:any=None, end_col:any=None):
        super().__init__(message, start_ln, start_col, end_ln, end_col)
        
# for Context errors alert if an ore is outside an anvil or spark is outside an ore
class HovaContextError(HovaError):
    def __init__(self, message:str, start_ln:any=None, start_col:any=None, end_ln:any=None, end_col:any=None):
        super().__init__(message, start_ln, start_col, end_ln, end_col)
        
# for Type errors if a spark value is different from what was defined
class HovaTypeError(HovaError):
    def __init__(self, message:str, start_ln:any=None, start_col:any=None, end_ln:any=None, end_col:any=None):
        super().__init__(message, start_ln, start_col, end_ln, end_col)
        
# for errors that occurs in Emission's time
class HovaEmissionError(HovaError):
    def __init__(self, message:str, start_ln:any=None, start_col:any=None, end_ln:any=None, end_col:any=None):
        super().__init__(message, start_ln, start_col, end_ln, end_col)
        
        
# function that verify If is an error or not
def IsError(code):
    return True if isinstance(code, HovaError) else False