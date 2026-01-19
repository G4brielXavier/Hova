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

        NewOres = []
        NewSparks = []  
        
        if len(node['sparks']) > 0:
            for spark in node['sparks']:
                if spark['value']['type'] in ('StringLiteral', 'IntegerLiteral', 'FloatingLiteral', 'BooleanLiteral', 'ArrayLiteral'):
                    NewSparks.append(spark)
            
        if len(node['child_ores']) > 0:
            for oreChild in node['child_ores']:
                oreName = oreChild['name']
                oreSparks = oreChild['sparks']
                oreEmbeds = oreChild['child_ores']
                
                NewEmbed = {
                    "type": "EmbedOre",
                    "name": oreName,
                    "child_ores": oreEmbeds,
                    "sparks": oreSparks
                }

                NewOres.append(NewEmbed)                 
                
        node["sparks"] = NewSparks
        node['child_ores'] = NewOres
        return node
   
    
        