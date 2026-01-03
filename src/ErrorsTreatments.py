# ERROR TREATMENTS
# Tratamento de erros proprio da Hova

# -------------------------------------------------
# CATEGORIA                                CÓDIGO |
# -------------------------------------------------
# Syntax                                   EV100  |          
# Scope                                    EV202  |
# Type                                     EV300  |
# Reference                                EV404  |
# Emission                                 EV500  |
# -------------------------------------------------
 
# Syntax - Erros de Escrita e estrutura, faltas de espaço ou tabulação
# Scope - Erros de escopo, definidores foram de englobadores 
# Type - Erros de tipo de valor
# Reference - Erro de inexistência, definidor não declarado ou algo inexistente
ErrorIndexCode = {
    "100": "Syntax",
    "202": "Scope",
    "300": "Type",
    "404": "Reference",
    "500": "Emission"
}

class HovaError:
    def __init__(self, code, message, line:any=None):
        self.code = code
        self.message = message
        self.line = line
        
    def Log(self):
        print(f'[HOVA : {ErrorIndexCode[self.code]}Error] - {self.message} { f'At line {self.line}' if self.line else '' }')

    