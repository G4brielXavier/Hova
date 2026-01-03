from .ErrorsTreatments import HovaError

EmitterConfig = {
    "hova": {
        "struct": {
            "mode": "complex"
        },
        "encompass": {
            "directSparks": "off",
            "directOres": "off",
            "hideAtomic": "off"
        },
        "definer": {
            "types": "on",
            "view": "normal"
        },
    }
}



def UpdateEmitterConfig(atomicConfig):
    
    atoms = atomicConfig['atoms']
    
    for atom in atoms:
        if isinstance(atom['name'], list):
            fromConfig = atom['name'][0]
            fromType = atom['name'][1]
            fromSetting = atom['name'][2]
            
            value = atom['value']
            
            EmitterConfig[fromConfig][fromType][fromSetting] = value['value']
            
        
        

def Emitter(node, canUpdate:bool=False):
    
    if isinstance(node, HovaError):
        return node
    
    if node['type'] == 'AnvilEncompass':
        if node['atomic'] == 'undefined':
            return HovaError('500', f'"AtomicEncompass" is undefined.')
    
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
    
    if isinstance(node, str):
        return "undefined"

    
    if node["type"] == "AnvilEncompass":
                
        AnvilName = node["name"] # AnvilName
        AnvilAtomic = node["atomic"] # AtomicMetadata
        AnvilChildren = node["ores"] # Ores
        
        Children = {}
        
        for child in AnvilChildren:
            ore = Emitter(child)
            
            if isinstance(ore, HovaError):
                return ore
            
            keyName = child['name']

            if not 'ignored' in ore:
                Children[keyName] = ore

                    
        if EmitterConfig['hova']['encompass']['directOres'] == 'on':
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
        
        if EmitterConfig['hova']['encompass']['directOres'] == 'on':
            for name, value in Sparks.items():
                OreDict[name] = value
        elif EmitterConfig['hova']['encompass']['directOres'] == 'off':
            OreDict["sparks"] = Sparks
    
        return OreDict
    
    if node["type"] == "AtomicEncompass":
        
        Atoms = {
            "config": {}
        }
        
        for atom in node["atoms"]:
            atomEmitted = Emitter(atom)
            
            if isinstance(atom['name'], list):
                AtomKey = '.'.join(atom['name'])
                Atoms['config'][AtomKey] = atomEmitted
            else:
                AtomKey = atom['name']
                Atoms[AtomKey] = atomEmitted
            
        
        return Atoms
    
    if node["type"] == "Atom":
        
        AtomValue = node["value"]['value']
        return AtomValue
    
    if node["type"] == "Spark":

        if EmitterConfig['hova']['definer']['types'] == 'on':
            SparkFinalStruct = {}
            
            SparkValue = node["value"]['value']
            SparkType = node['value']['type']
        
            SparkValue = ConvertTo(SparkType, node['value']['value'])
            
            SparkFinalStruct['type'] = SparkType
            SparkFinalStruct['value'] = SparkValue

            return SparkFinalStruct
        
        elif EmitterConfig['hova']['definer']['types'] == 'off':
            SparkType = node['value']['type']
            SparkValue = ConvertTo(SparkType, node['value']['value'])

            return SparkValue
        
        