TypesIndex = {
    "StringLiteral": "str",
    "IntegerLiteral": "int",
    "FloatingLiteral": "float",
    "BooleanLiteral": "bool",
    "ArrayLiteral": "list"
}

from src.Parser import Spark, Literal
from src.ErrorsTreatments import HovaError
 

def FunctionInterpreter(node, runes, tempers):
    NewNode = []
    Runes = runes
    Tempers = tempers
    
    # RUNES
    def isExistRune(key):
        for k, _ in Runes.items():
            if k == key:
                return True
            
        return False
    
    def NewRune(key, value):
        if isExistRune(key):
            return HovaError('404', f'Already exists a RuneDefiner named "{key}".')    
        
        Runes[key] = value
        
    def GetRune(key):
        if not isExistRune(key):
            return HovaError('404', f'Not exists a RuneDefiner named "{key}".')
            
        return Runes[key]
    
    # TEMPERS
    
    def isExistTemper(key:str) -> bool:
        for temperKey, _ in Tempers.items():
            if temperKey == key:
                return True
            
        return False
        
        
    def NewTemper(name:str, data:dict):
        if isExistTemper(name):
            return HovaError(f'404', f'Already exists a TemperEncompass named "{name}"')
        
        Tempers[name] = data
        
    def GetTemper(name:str):
        if not isExistTemper(name):
            return HovaError('404', f'Not exists a TemperEncompass named "{name}"')
        
        return Tempers[name]
    
    
    # Integrated Functions
    def IntegratedFunctionIntepreter(data_func):
        FuncInformations = None
        
        if data_func["type"] == "Spark":
            FuncInformations = data_func["value"]
            
        elif data_func["type"] == "CallFunction":
            FuncInformations = data_func

            if FuncInformations["callee"] == "userune":
                RuneName = FuncInformations["args"][0]["name"]
                RuneData = GetRune(RuneName)
                
                return RuneData
        
            if FuncInformations["callee"] == "usedetail":
                ...
                
        
            
    
    # To Create Runes
 
    if node["type"] == "CharmEncompass":
        if node['runes'] == [] or len(node["runes"]) == 0:
           return 'CharmInterpreted' 
        
        for rune in node["runes"]:
            runeKey = rune["name"]
            runeValue = rune["value"]
            NewRune(runeKey, runeValue)
            
        return 'CharmInterpreted'
    
    if node["type"] == "TemperEncompass":
        if node['children'] == [] or len(node['children']) == 0:
            return 'TemperInterpreted'
        
        temperName = node['name']
        temperArguments = node['args']
        temperDetails = node['children']
    
        TemperDict = {
            "args": temperArguments,
            "details": temperDetails
        }
    
        NewTemper(temperName, TemperDict)
        
        return 'TemperInterpreted'
    
    if node["type"] == "AnvilEncompass":
        oresInterpreted = []
        
        for ore in node["ores"]:
            oresInterpreted.append(FunctionInterpreter(ore, runes, tempers))
            
        node["ores"] = oresInterpreted
        
        NewNode = node
        return NewNode
             
    if node["type"] == "OreEncompass":

        NewSparks = []
        CurrentSparks = node['sparks']
        
        if isinstance(CurrentSparks, dict):
            
            
            
            callee = CurrentSparks['callee']
            temperIdentifier = CurrentSparks['temperName'].value
            temperCallArgs = CurrentSparks['temperArgumentsValue']
            
            TemperMain = GetTemper(temperIdentifier)
            TemperMainArgs = [arg['name'] for arg in TemperMain['args']]
            TemperMainDetails = TemperMain['details']
            
            TemperLengthArgs = len(TemperMain['args'])
            TemperCallLengthArgs = len(temperCallArgs)
            
            if TemperCallLengthArgs == 0:
                return HovaError('404', f'You are letting {temperIdentifier}\'s args empty.')
            
            if TemperCallLengthArgs > TemperLengthArgs:
                return HovaError('404', f'{temperIdentifier} expects only {TemperLengthArgs} args.')
            
            if TemperCallLengthArgs > 0 and not TemperCallLengthArgs == TemperLengthArgs:
                return HovaError('404', f'{temperIdentifier} not match with length expected.')
            
            ArgumentOrganized = {}
            
            
            
            for argIndex, argValue in enumerate(TemperMainArgs):
                ArgumentOrganized[argValue] = temperCallArgs[argIndex]
                
            
                
            for detail in TemperMainDetails:
                detailName = detail['name']
                detailValue = detail['value']
                detailArgName = None
                
                if detailValue['type'] == "CallFunction":
                    if detailValue['callee'] == 'usedetail':
                        detailArgName = detailValue['args'][0]
                
                
                ArgValue = ArgumentOrganized[detailArgName]
                
                NewSpark = Spark(detailName, None, ArgValue)
                NewSparks.append(NewSpark)        
        
        else:
            
            for spark in node["sparks"]:
                
                if spark["value"]["type"] in ("StringLiteral", "IntegerLiteral", "FloatingLiteral", "BooleanLiteral", "ArrayLiteral"):
                    NewSparks.append(spark)
                
                if spark["value"]["type"] == "CallFunction":
                    spark["value"] = IntegratedFunctionIntepreter(spark)
                    NewSparks.append(spark)
                
        node["sparks"] = NewSparks
        return node

                
    
        