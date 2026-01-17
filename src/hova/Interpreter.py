TypesIndex = {
    "StringLiteral": "str",
    "IntegerLiteral": "int",
    "FloatingLiteral": "float",
    "BooleanLiteral": "bool",
    "ArrayLiteral": "list"
}

from .Parser import Spark, Literal
from .ErrorsTreatments import (
    HovaSyntaxError,
    HovaTypeError,
    HovaContextError,
    HovaReferenceError,
    HovaEmissionError
)
 

def FunctionInterpreter(node):
    NewNode = []
 
    if node["type"] == "AnvilEncompass":
        oresInterpreted = []
        
        for ore in node["children"]:
            oresInterpreted.append(FunctionInterpreter(ore))
            
        node["children"] = oresInterpreted
        
        NewNode = node
        return NewNode
     
    if node['type'] == "CaveEncompass":
        oresInside = []
        
        for ore in node['ores']:
            oreNode = FunctionInterpreter(ore)
            oresInside.append(oreNode)
            
        node['ores'] = oresInside
        
        newNode = node
        return newNode
             
    if node["type"] == "OreEncompass":

        NewSparks = []

        # print(node)

        for spark in node["sparks"]:
            
            if spark['type'] == 'OreEncompass':
                OreName = spark['name']
                OreItems = spark['sparks']
                
                NewEmbed = {
                    "type": "EmbedOre",
                    "name": OreName,
                    "items": {}
                }
                
                for ore in OreItems:

                    ItemKey = ore['name']
                    ItemValue = ore['value']['value']
                    
                    NewEmbed['items'].update({ItemKey : ItemValue})
                    
                NewSparks.append(NewEmbed)
                
            
            if spark['type'] == 'Spark':
                if spark["value"]["type"] in ("StringLiteral", "IntegerLiteral", "FloatingLiteral", "BooleanLiteral", "ArrayLiteral"):
                    NewSparks.append(spark)    
                
        node["sparks"] = NewSparks
        return node

                
    
        