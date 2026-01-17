from .ErrorsTreatments import (
    HovaSyntaxError,
    HovaTypeError,
    HovaContextError,
    HovaReferenceError,
    HovaEmissionError,
    IsError
)

EmitterConfig = {
    "visual": "default",
    "engine": "none",
    "hideAtomic": "off",
    "onelineSpark": "off",
    "hideConfig": "off"
}



def UpdateEmitterConfig(atomicConfig):
    
    atoms = atomicConfig['atoms']
    
    for atom in atoms:
        key = atom['name']
        value = atom['value']
        
        EmitterConfig[key] = value['value']
            
        
        

def Emitter(node, canUpdate:bool=False):
    
    if IsError(node): raise node
    
    if node['type'] == 'AnvilEncompass':
        if not node['atomic'] == 'undefined':
            AllKeyAtoms = [p['name'] for p in node['atomic']['atoms']]

        if node['atomic'] == 'undefined':
            
            AtomicDefault = {
                "type": "AtomicEncompass",
                "atoms": [
                    {
                        "type": "Atom",
                        "name": "emit",
                        "value": { "type": "StringLiteral", "value": "json", "line": 0, "col": 0 },
                        "line": 0,
                        "col": 0
                    },
                    {
                        "type": "Atom",
                        "name": "visual",
                        "value": { "type": "StringLiteral", "value": "default", "line": 0, "col": 0 },
                        "line": 0,
                        "col": 0
                    }
                ]
            }
            node['atomic'] = AtomicDefault       
        elif not 'emit' in AllKeyAtoms:
            EmitStruct = {
                "type": "Atom",
                "name": "emit",
                "value": { "type": "StringLiteral", "value": "json", "line": 0, "col": 0 },
                "line": 0,
                "col": 0
            }
            
            node['atomic']['atoms'].append(EmitStruct) 

    if canUpdate: UpdateEmitterConfig(node['atomic'])

    def ConvertTo(type:str=None, val:str=None) -> any:
        match(type):
            case 'StringLiteral': return str(val)
            case 'IntegerLiteral': return int(val)
            case 'FloatingLiteral': return float(val)
            case 'BooleanLiteral': return bool(val)
            case 'ArrayLiteral':
                items = []
                for item in val:
                    items.append(ConvertTo(item['type'], item['value']))
                return list(items)
    
    if isinstance(node, str): return "undefined"
    
    if node["type"] == "AnvilEncompass":
                
        AnvilName = node["name"] # AnvilName
        AnvilAtomic = node["atomic"] # AtomicMetadata
        AnvilChildren = node["children"] # Ores
        
        Children = {}
        
        for child in AnvilChildren:
            ore = Emitter(child)
            
            if IsError(ore): raise ore
            
            keyName = child['name']

            if not 'ignored' in ore:
                Children[keyName] = ore

                    
        if EmitterConfig['visual'] == 'minimal':
            AnvilDict = {
                AnvilName: {
                    "atomic": Emitter(AnvilAtomic, False) if AnvilAtomic != "undefined" else {},
                }
            }   
            
            for k, v in Children.items():
                AnvilDict[AnvilName][k] = v
        else:
            AnvilDict = {
                AnvilName: {
                    "atomic": Emitter(AnvilAtomic, False) if AnvilAtomic != "undefined" else {},
                    "ores": Children
                }
            }   
            
        return { 'anvilData': AnvilDict, 'emitterConfigData': EmitterConfig }
    
    if node["type"] == "CaveEncompass":
        
        CaveName = node['name']
        CaveOres = node['ores']
        
        Ores = {}
        
        for ore in CaveOres:
            oreEmitted = Emitter(ore)
    
            if IsError(oreEmitted): raise oreEmitted
            
            keyName = ore['name']
            
            if not 'ignored' in oreEmitted:
                Ores[keyName] = oreEmitted
                
        if EmitterConfig['visual'] == 'minimal':
            for name, value in Ores.items():
                Ores[name] = value
                
        return Ores
    
    if node["type"] == "OreEncompass":
        
        Seals = node["seals"]
        OreSparks = node["sparks"]
        MessageImportant_Seal = []

        # SETUP ANNOTATIONS        
        if not Seals == []:
            for seal in Seals:
                if seal["name"] == 'reject': MessageImportant_Seal.append({"message": 'IGNORE_IT', "args": []})
                if seal["name"] == "mark": MessageImportant_Seal.append({"message": 'MARK_IT', "args": seal["args"]})
            
        Sparks = {}
        OreDict = {}
        
        # ADDING ANNOTATIONS EMITTED
        if not MessageImportant_Seal == []:
            for seal_msg in MessageImportant_Seal:
                if seal_msg["message"] == "MARK_IT":
                    MarksToAdd = []
                    
                    for mark in seal_msg['args']:
                        MarksToAdd.append(mark["value"])
                    
                    OreDict["marks"] = MarksToAdd
                    
                if seal_msg["message"] == "IGNORE_IT":
                    OreDict["ignored"] = seal_msg["args"]
        
        # ADDING SPARKS EMITTED
        for child in OreSparks:
            spark = Emitter(child)
            Sparks[child["name"]] = spark
        
        if EmitterConfig['visual'] == 'minimal':
            for name, value in Sparks.items():
                OreDict[name] = value
        else:
            OreDict["sparks"] = Sparks
    
        return OreDict
    
    if node["type"] == "AtomicEncompass":
        
        AtomConfig = ['engine', 'hideAtomic', 'hideConfig', 'visual']
        
        Atoms = {
            "config": {}
        }
        
        for atom in node["atoms"]:
            atomEmitted = Emitter(atom)
            
            if atom['name'] in AtomConfig:
                Atoms['config'][atom['name']] = atomEmitted
            else:
                AtomKey = atom['name']
                Atoms[AtomKey] = atomEmitted
                
        if EmitterConfig['hideConfig'] == 'on':
            del Atoms['config']
        
        return Atoms
    
    if node["type"] == "Atom":
        
        AtomValue = node["value"]['value']
        return AtomValue
    
    if node["type"] == "Spark":

        if EmitterConfig['visual'] == "complex" or EmitterConfig['visual'] == "high" or EmitterConfig['visual'] == "default":
            SparkFinalStruct = {}
            
            SparkValue = node["value"]['value']
            SparkType = node['value']['type']
        
            SparkValue = ConvertTo(SparkType, node['value']['value'])
            
            SparkFinalStruct['type'] = SparkType
            SparkFinalStruct['value'] = SparkValue

            return SparkFinalStruct
        
        elif EmitterConfig['visual'] == "minimal" or EmitterConfig['visual'] == "basic":
            SparkType = node['value']['type']
            SparkValue = ConvertTo(SparkType, node['value']['value'])

            return SparkValue
    
    if node['type'] == 'EmbedOre':
        
        EmbedItems = node['items']
        return EmbedItems