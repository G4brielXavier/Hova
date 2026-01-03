# HOVA PARSER 0.5.5

# TODO: Implementação de erros nos resto dos Definers






from .Tokenizer import Token
from .ErrorsTreatments import HovaError

def Literal(type, value) -> dict:
    return {
        "type": type,
        "value": value
    }
    
def Identifier(name) -> dict:
    return {
        "type": "Identifier",
        "name": name
    }
    
def Spark(name, type, value) -> dict:
    return {
        "type": "Spark",
        "valType": type,
        "name": name,
        "value": value
    }
    
def Atom(name, value) -> dict:
    return {
        "type": "Atom",
        "name": name,
        "value": value
    }
    
def Rune(name, type, value) -> dict:
    return {
        "type": "Rune",
        "valType": type,
        "name": name,
        "value": value
    }

    
def Seal(name, args=None) -> dict:
    return {
        "type": "Seal",
        "name": name,
        "args": args 
    }
    
    
def Detail(name, type, value) -> dict:
    return {
        "type": "Detail",
        "name": name,
        "typeVal": type,
        "value": value
    }

# EncompassConverters
     
def AnvilEncompass(name, atomic, ores) -> dict:
    return {
        "type": "AnvilEncompass",
        "name": name,
        "atomic": atomic,
        "ores": ores,
    }

def OreEncompass(seals, name, sparks) -> dict:
    return {
        "type": "OreEncompass",
        "name": name,
        "seals": seals,
        "sparks": sparks
    }
    
def CharmEncompass(runes) -> dict:
    return {
        "type": "CharmEncompass",
        "runes": runes
    }
    
def AtomicEncompass(atoms) -> dict:
    return {
        "type": "AtomicEncompass",
        "atoms": atoms
    }

def CallFunction(callee, param=None, args=[]) -> dict:
    return {
        "type": "CallFunction",
        "callee": callee,
        "param": param,
        "args": args
    }
    
def NamespaceEmitter(props, val) -> dict:
    return {
        "type": "NamespaceEmit",
        "props": props,
        "val": val
    }


def TemperEncompass(name:Token, args:list, children:dict) -> dict:
    return {
        "type": "TemperEncompass",
        "name": name,
        "args": args,
        "children": children
    }


TypesIndex = {
    "StringLiteral": "str",
    "IntegerLiteral": "int",
    "FloatingLiteral": "float",
    "BooleanLiteral": "bool",
    "ArrayLiteral": "list"
}

types = [
    "StringLiteral",
    "IntegerLiteral",
    "FloatingLiteral",
    "BooleanLiteral",
    "ArrayLiteral",
]

TypesAbrev = [
    "str", "int", "float", "list", "bool"
]



# NOTE: How Hova's Parser works?

# 1. Firstly is executed the while True 
# - Inside is created a variable called 'ast' that will be returned to Runtime with all nodes
# - And execute the Parse_Primary and each token 

# 2. Parse_Primary analize each token
# - If your type is STRING, NUMBER_INTEGER, NUMBER_FLOATING, it become Literal
# - If its keyword, find and execute your own parser. Like Atomic that has your Parser_Atomic()
# - All Parsers returns a DictStructure to Parse_Primary and it returns to While True to be add in ast list



def Parser(tokens):
    pos = 0
    context_stack = []
    
    def ViewNext():
        return tokens[pos] if pos < len(tokens) else None
    
    def Next():
        return tokens[pos+1] if pos+1 < len(tokens) else None
        
    def ConsumeToken():
        nonlocal pos
        token = tokens[pos]
        pos += 1
        return token

    def IsError(code):
        return True if isinstance(code, HovaError) else False

    def Expect(value=None, type=None, no_error=False, msg=None):
        next = ViewNext()
        
        if not next:
            return HovaError('100', f'Expected "{value or type}" but got NULL.', tokens[pos-1].ln)

        if no_error:
            if value is not None and next.value != value:
                return None
        
        if value is not None and next.value != value:
            return HovaError('100', f'Expected token value "{value}", but got "{next.value}"' if msg is None else msg, tokens[pos-1].ln)
            
        if type is not None and next.type != type:
            return HovaError('100', f'Expected token type "{type}", but got "{next.type}"' if msg is None else msg, tokens[pos-1].ln)
            
        return ConsumeToken()
    
    def NextIsNone():
        if ViewNext() is None:
            return True
        return False
    
    def debugTokens(token, where=""):
        if token is None:
            return
        
        print(
            f'[PRIMARY {where}] \n'
            f'type={token.type} \n'
            f'value={repr(token.value)} \n'
        )
    
    # GENERIC FUNCTIONS
    
    def Parse_Block(until:str=None, encompassName:str=None, canEmpty:bool=False, insideOf:str=None, uniqueChild:bool=None, definerEncompass:str=None) -> list: 
        nodes = []
         
        while True:
            next = ViewNext()
            
            if not next:
                # print(f'The next is None ')
                return HovaError('100', f'Expected "{until}" to close "{encompassName}", but reached EOF.', tokens[pos-1].ln)

            if next.value == until:
                # print(f'The next is equal {until}')
                break
            
            if insideOf and context_stack[-1] != insideOf:
                return HovaError('100', f'This is must be insideOf {insideOf}, so is {context_stack[-1]}', next.ln)
            
            
            before = pos
            node = Parse_Primary()
            
            if IsError(node): return node
            
            if uniqueChild:
                for it in nodes:   
                    
                    if context_stack[-1] == 'anvil':
                        if node['type'] == 'AtomicEncompass':
                            continue
                    
                    # elif not node['type'] in ('StructLiteral', 'SymbolLiteral', 'IntegerLiteral', 'FloatingLiteral', 'BooleanLiteral'):                  
                    #     if it['name'] == node['name']:
                    #         return HovaError('202', f'Already exists a {definerEncompass} called "{node['name']}".', next.ln)
                        
            
            if node is None:
                return HovaError('404', f'Parser stalled in "{encompassName}". Token "{next.value}" not consumed.', next.ln)
            
            if pos == before:
                return HovaError('404', f'Infinite loop detected in "{encompassName}". Token "{next.value}"', next.ln)
            
            if not node['type'] in ('StructLiteral', 'SymbolLiteral'):
                nodes.append(node)
        
        untilTok = Expect(until)
        # print(f'{encompassName} = {ViewNext().value}')
        if IsError(untilTok): return HovaError('100', f'Expected "end" to close "{encompassName}" keyword', tokens[pos-1].ln)
        
        
        return nodes
    
    def Parse_Array(until:str=None, arrayName:str=None):
        items = []
        
        while True:
            next = ViewNext()
            
            if not next:
                return HovaError('100', f'Expected "{until}" to close "{arrayName}", but reached EOF.', tokens[pos-1].ln)
                
            if next.value == until:
                break
            
            before = pos
            node = Parse_Primary()

            if not ViewNext().value == "]" and ViewNext() and not ViewNext().value == ",":
                return HovaError('100', f'Expected "," after each item', next.ln)
            
            if not ViewNext().value == "]":
                virTok = Expect(value=',')
                if IsError(virTok): 
                    return virTok

            if node is None:
                return HovaError('404', f'Parser stalled in "{arrayName}". Token "{next.value}" not consumed', next.ln)
                
            if IsError(node): return node
            
            if pos == before:
                return HovaError('404', f'Infinite loop detected in "{arrayName}"', next.ln)
                
            items.append(node)
            
                
        closedArray = Expect(until)
        if IsError(closedArray): return HovaError('100', f'Expected "]" to close the Array "{arrayName}"', next.ln)
        
        return items
            
    def Parse_Callee(kwName:str=None) -> dict:
        if not ViewNext() or ViewNext().value != "(":
            return HovaError('100', f'Expected "()" after "{kwName}" literal.', tokens[pos-1].ln)
        
        parenOpenTok = Expect(value='(')
        if IsError(parenOpenTok): return parenOpenTok # (
            
        args = []
        while True:
            next = ViewNext()
            
            if next.value == ')':
                break
            
            if NextIsNone():
                return HovaError('100', f'Reached None with CalleeFunction {kwName}', next.ln)
            
            node = Parse_Primary()
            
            if IsError(node): return node
            
            args.append(node)
            
        parenCloseTok = Expect(value=')')
        if IsError(parenCloseTok): return parenCloseTok # )
        
        return CallFunction(callee=kwName.lower(), args=args)
    
    def Parse_Namespace(setting) -> dict:
        namespaces = [setting]
        
        Expect(value='.')
        
        if ViewNext() and ViewNext().type == 'IDENTIFIER':
            node = Parse_Primary()
            if IsError(node): return node
            namespaces.append(node['name'])
        
        Expect(value='.')
        
        if ViewNext() and ViewNext().type == 'IDENTIFIER':
            node = Parse_Primary()
            if IsError(node): return node
            namespaces.append(node['name'])

        return namespaces
    
    def Parse_Arguments(name:str, fromName:str):
        args = []
        
        if not ViewNext() or not ViewNext().value == '(':
            return HovaError('100', f'Expected "(" in "{fromName}"', tokens[pos].ln)
        
        ParenOpen = Expect(value='(')
        if IsError(ParenOpen): return ParenOpen
        
        while True:
            next = ViewNext()
            
            if next.value == ')':
                break 
            
            if NextIsNone():
                return HovaError('100', f'Reached None in "{name}" {fromName}.', next.ln)
        
            before = pos
            node = Parse_Primary()
            
            if not ViewNext().value == ')' and ViewNext() and not ViewNext().value == ',':
                return HovaError('100', f'Expected "," after each item.', next.ln)
            
            if not ViewNext().value == ')':
                virTok = Expect(value=',')
                if IsError(virTok): return virTok
                
            if node is None:
                return HovaError('404', f'Parser stalled in "{fromName}". Token "{next.value}" not consumed.', next.ln)
        
            if IsError(node): return node
            
            if pos == before:
                return HovaError('404', f'Infinite loop detected in "{fromName}". Token "{next.value}"', next.ln)                
    
            args.append(node)
            
        ParenClosed = Expect(value=')')
        if IsError(ParenClosed): 
            return HovaError('100', f'Expected ")" to close "TemperArguments"', tokens[pos-1].ln)

        return args
    
    # To help
    
    def TypeIsCorrect(val, type) -> bool:
        if val["type"] != "EmptyLiteral" and val["type"] != "Identifier" and val["type"] != "CallFunction":
            if not TypesIndex[val["type"]] == type:
                return False
            
        return True
    
    def DefinerValueIsCorrect(oneType:str=None) -> bool:
        KEYWORD = [
            'true', 'false'
        ]
        
        if not oneType:
            if not ViewNext().type in ('STRING', 'NUMBER_INTEGER', 'NUMBER_FLOATING', "SYMBOL") and not ViewNext().value in KEYWORD and not ViewNext().value == '[':
                return False 
            return True
        else:   
            if not ViewNext().type == oneType and ViewNext().value in KEYWORD:
                return False
            return True
     
    def IsType(value:Token=None, typeList:list=None) -> bool:
        for t in typeList:
            if not t in types:
                return HovaError('300', f'This {t} type not exist.')
        
        for t in typeList:
            if value['type'] == t:
                return True
        return False     
    
    def TypeExist(type:str) -> bool:
        
        for t in TypesAbrev:
            if t == type: return True
    
        return False
    
    # Parses for Encompasses
    
    def Parse_Anvil():
        if NextIsNone():
            return HovaError('100', "Expected 'AnvilName' after 'anvil' keyword", tokens[pos-1].ln)
        
        tok = tokens[pos]
        
        context_stack.append('anvil')
                
        # anvil ManCharacters by me be
        # end like json to Characters
        
        # ==========================================================
        # AnvilName
        AnvilNameTok = Expect(type="IDENTIFIER")
        if IsError(AnvilNameTok): return AnvilNameTok
        
        AnvilName = AnvilNameTok.value
        
        # ==========================================================
        # between 'be' and 'end'
        if NextIsNone():
            return HovaError('100', f'Expected "be" after {AnvilName} identifier', tok.ln)
        
        beTok = Expect(value='be') # Consume 'be'
        if IsError(beTok): return beTok
        
        children = Parse_Block(
            until='end', 
            encompassName="AnvilEncompass",
            definerEncompass="OreEncompass",
            uniqueChild=True
        )
        
        if IsError(children):
            return children 
        
        # ==========================================================
        # atomic inside (optional)
        AnvilAtomic = "undefined"
        for i, child in enumerate(children):
            if isinstance(child, dict):
                if child["type"] == "AtomicEncompass":
                    AnvilAtomic = child
                    children.pop(i)
            else:
                return child
                
        # ==========================================================
        context_stack.pop()
        return AnvilEncompass(AnvilName, AnvilAtomic, children)

    def Parse_Atomic():
        
        # print(f'Current Stack: {context_stack}')
        # print(f'Recent Stack: {context_stack[-1]}')
        
        if not context_stack or not context_stack[-1] == 'anvil':
            return HovaError('202', 'You are declaring an AtomicEncompass outside an AnvilEncompass', None)
        
        if NextIsNone():
            return HovaError('100', "Expected 'be' after 'atomic' keyword", tok.ln)
        
        tok = tokens[pos]
        
        if not context_stack[-1] == 'anvil':
            return HovaError('202', "'AtomicEncompass' must be inside an 'AnvilEncompass'.", tok.ln)
            
        if context_stack[-1] == 'anvil' and ViewNext().value != 'be':
            return HovaError('100', "Expected 'be' after 'atomic' keyword", tok.ln)
            
        context_stack.append('atomic')
        
        atoms = []
        beTok = Expect(value='be')
        if IsError(beTok): return beTok
        
        if not Next():
            return HovaError('100', "Expected 'end' to close 'AtomicEncompass'", tok.ln)
        
        if ViewNext().value == 'end' and not Next().value == 'like':
            endTok = Expect(value="end")
            if IsError(endTok): return endTok
            
            context_stack.pop()
            return AtomicEncompass(atoms)
        
        atoms = Parse_Block(
            until='end', 
            encompassName="AtomicEncompass", 
            definerEncompass="AtomDefiner",    
            uniqueChild=True
        )
            
        if IsError(atoms):
            return atoms
                
        if NextIsNone():
            return HovaError('100', "Expected 'end' to close 'AtomicEncompass'", tok.ln)

        if context_stack[-1] == "anvil" and ViewNext() and ViewNext().value != 'end':
            return HovaError('100', "Expected 'end' to close 'AtomicEncompass'", tok.ln)

        context_stack.pop()
        return AtomicEncompass(atoms)
    
    def Parse_Charm():

        if context_stack and context_stack[-1] == 'anvil':
            return HovaError('202', 'You are declaring a CharmEncompass inside an AnvilEncompass. That should stay out.', None)
        
        if NextIsNone() or ViewNext().value != 'be':
            return HovaError('100', "Expected 'be' after 'charm' keyword", tokens[pos-1].ln)
            
        
        tok = tokens[pos]
        
        Runes = []

        context_stack.append('charm')
                        
        Expect(value='be')
                
        if ViewNext() and ViewNext().value == "end":
            endTok = Expect(value="end")
            if IsError(endTok): return HovaError('100', "Expected 'end' to close 'CharmEncompass' keyword", tok.ln)
            
            context_stack.pop()
            return CharmEncompass(Runes)
        
        Runes = Parse_Block(
            until='end', 
            encompassName="CharmEncompass",
            definerEncompass="RuneDefiner",
            uniqueChild=True
        )
        
        if IsError(Runes):
            return Runes

        if NextIsNone():
            return HovaError('100', "Expected 'end' to close 'CharmEncompass' keyword", tok.ln)
            
        context_stack.pop()
        return CharmEncompass(Runes)
    
    def Parse_Ore():
    
        if not context_stack or not context_stack[-1] == 'anvil':
            return HovaError('202', 'You are declaring an OreEncompass outside an AnvilEncompass', None)
        
        if NextIsNone():
            return HovaError('100', "Expected 'OreName' after 'ore' keyword", tok.ln)
            
        tok = tokens[pos]
        
        # If ore is not inside an anvil
        if not context_stack[-1] == 'anvil':
            return HovaError('202', "'OreEncompass' must be inside an 'AnvilEncompass'.", tok.ln)
    
        if context_stack[-1] == 'anvil' and not ViewNext().type == 'IDENTIFIER':
            return HovaError('100', "Expected 'OreName' after 'ore' keyword", tok.ln)
        
        sparks = []
        typeDeclare = None
        context_stack.append('ore')
        
        # 1. Get the Ore name
        NameTok = Expect(type="IDENTIFIER")
        if IsError(NameTok): return NameTok
        EntityName = NameTok.value
        
        if context_stack[0] == 'anvil' and ViewNext().value != 'be':        
            if context_stack[0] == 'anvil' and ViewNext().value != ':':
                return HovaError('100', "Expected 'be' or ':' after 'OreName' identifier", tok.ln)
        
        if ViewNext().value == 'be':     
            typeDeclare = 'be'   
            beTok = Expect(value='be')
            if IsError(beTok): return beTok
        elif ViewNext().value == ':':
            typeDeclare = ':'   
            twoDots = Expect(value=':')
            if IsError(twoDots): return twoDots
        
        # If has spark or seals, get all them
        if typeDeclare == 'be':
            
            children = Parse_Block(
                until='end', 
                encompassName='OreEncompass', 
                definerEncompass='SparkDefiner',
                canEmpty=True, 
                uniqueChild=True
            )

        elif typeDeclare == ':':
            
            TemperName = Expect(type='IDENTIFIER')
            if IsError(TemperName): return TemperName
            
            TemperArgs = Parse_Arguments(EntityName, 'OreEncompass')
            if IsError(TemperArgs): return TemperArgs
            
            TemperDict = {
                "type": "TemperCaller",
                "callee": "usetemper",
                "temperName": TemperName,
                "temperArgumentsValue": TemperArgs
            }
            
            children = TemperDict
            context_stack.pop()
            return OreEncompass([], EntityName, children)
        
        if IsError(children): return children

            # if context_stack[0] == "anvil" and ViewNext().value == "end" and Next() is None:
            #     print(tokens[pos-1].value)
            #     print(ViewNext().value)
            #     print(Next().value)
            #     return HovaError('100', "Expected 'end' to close 'OreEncompass'", tok.ln)
                
        # If is Empty, let empty
        if len(children) == 0:            
            context_stack.pop()
            return OreEncompass([], EntityName, children) 

        Sparks = []
        Seals = []

        if typeDeclare == 'be':
            
            for child in children:
                
                if child['type'] == 'Seal':
                    Seals.append(child)
                else:
                    Sparks.append(child)
                    
            children = []

            if IsError(sparks):
                return sparks
        
        context_stack.pop()
        return OreEncompass(Seals, EntityName, Sparks)      
    
    def Parse_Temper():
        if NextIsNone():
            return HovaError('100', "Expected 'TemperName' after 'temper' literal", tokens[pos-1].ln)
        
        tok = tokens[pos]
        
        if not context_stack == []:
            return HovaError('202', "'TemperEncompass' can not be defined inside from other encompass.", tok.ln)
        
        context_stack.append('temper')
        
        # Temper Name
        TemperNameTok = Expect(type='IDENTIFIER')
        if IsError(TemperNameTok): return TemperNameTok
        
        TemperName = TemperNameTok.value
        
        # Temper Arguments
        
        if not ViewNext().value == "(":
            return HovaError('100', f'Expected "(args, ...)" after "{TemperName}"', tok.ln)
        
        parenOpen = Expect(value='(')
        if IsError(parenOpen): return parenOpen
        
        arguments = []
        
        while True: 
            next = ViewNext()
            
            if next.value == ")":
                break
            
            if NextIsNone():
                return HovaError('100', f'Reached None in "{TemperName}" Temper.', next.ln)
            
            before = pos
            node = Parse_Primary()
            
            if not ViewNext().value == ')' and ViewNext() and not ViewNext().value == ',':
                return HovaError('100', f'Expected "," after each item.', next.ln)
            
            if not ViewNext().value == ')':
                virTok = Expect(value=',')
                if IsError(virTok): return virTok
            
            if node is None:
                return HovaError('404', f'Parser stalled in "TemperArguments". Token "{next.value}" not consumed.', next.ln)
            
            if IsError(node): return node
            
            if pos == before:
                return HovaError('404', f'Infinite loop detected in "TemperArguments". Token "{next.value}"', next.ln)
            
            arguments.append(node)
            
        ParenClosed = Expect(value=')')
        if IsError(ParenClosed): 
            return HovaError('100', f'Expected ")" to close "TemperArguments"', tok.ln)
        
        # Between 'be' and 'end'
        
        beTok = Expect(value='be')
        if IsError(beTok): return beTok
        
        children = Parse_Block(
            until="end",
            encompassName="TemperEncompass",
            uniqueChild=True
        )

        if IsError(children): return children
        
        context_stack.pop()
        return TemperEncompass(TemperName, arguments, children)            
        
    
    # Parses for Definers
    
    def Parse_Spark():
        # PromptTest = spark Sides <int> : 4
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'ore':
            return HovaError('202', 'You are declaring a SparkDefiner outside an OreEncompass', tok.ln)
        
        if NextIsNone():
            return HovaError('100', 'Expected "SparkName" after "spark" literal.', tok.ln)

        # 1 = Sides                           
        SparkNameTok = Expect(type="IDENTIFIER")
        if IsError(SparkNameTok): return HovaError('100', 'Expected "SparkName" but something is wrong', tok.ln)
        
        SparkName = SparkNameTok.value
        
        SparkTypeTok = Expect(type="TYPE")
        SparkType = None if IsError(SparkTypeTok) else SparkTypeTok.value
        
        if SparkType and not TypeExist(SparkType):
            return HovaError('300', f'This type from Spark {SparkName} not exist or is wrong', tok.ln)
        
        # 3 - :
        twoDots = Expect(value=":")
        if IsError(twoDots): return HovaError('100', f'Expected spark finished. You can put ":" or a type value (optional).', tok.ln)

        # 4 - 4
        if not DefinerValueIsCorrect():
            return HovaError('100', f'Expected a correct value to Spark Definer', tok.ln)
        
        SparkValue = Parse_Primary()
        
        if IsError(SparkValue): return SparkValue
        
        if SparkType is not None and not TypeIsCorrect(SparkValue, SparkType):
            return HovaError('300', f'The Spark "{SparkName}" has a value with different type of {SparkType}', tok.ln)
                 
        return Spark(SparkName, SparkType, SparkValue)   
    
    def Parse_Atom():
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'atomic':
            return HovaError('202', 'You are declaring an AtomDefiner outside an AtomicEncompass', tok.ln)
        
        if NextIsNone():
            return HovaError('100', 'Expected "AtomName" after "atom" literal.', tok.ln)
    
        
        AtomNameTok = Expect(type="IDENTIFIER")
        if IsError(AtomNameTok): 
            AtomNameTok = Expect(type="KEYWORD")
            if AtomNameTok and AtomNameTok.value == "hova":
                AtomName = Parse_Namespace(AtomNameTok.value) 
            
                if IsError(AtomName): return AtomName
        else:
            AtomName = AtomNameTok.value
        
        if IsError(AtomNameTok): return HovaError('100', 'Expected "AtomName" after "atom" literal.', tok.ln)
    
        twoDots = Expect(value=":")
        if IsError(twoDots): return HovaError('100', f'Expected ":" after "{AtomName}"', tok.ln)
        
        if not DefinerValueIsCorrect('StringLiteral') or ViewNext().value == "end":
            return HovaError('100', f'Expected a "str" to AtomDefiner', tok.ln)

        
        AtomValue = Parse_Primary()

        
        if IsError(AtomValue): return AtomValue
        
        isTyped = IsType(AtomValue, ['StringLiteral', "BooleanLiteral"])
        
        if not isTyped:
            return HovaError('100', f'Expected a "StringValue" to AtomDefiner', tok.ln)
        
        if IsError(isTyped): return isTyped
        
        return Atom(AtomName, AtomValue)
    
    def Parse_Rune():
        
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'charm':
            return HovaError('202', 'You are declaring a RuneDefiner outside a CharmEncompass', tok.ln)
        
        if NextIsNone():
            return HovaError('100', 'Expected "RuneName" after "rune" literal', tok.ln)
        
        RuneNameTok = Expect(type="IDENTIFIER")
        if IsError(RuneNameTok): return HovaError('100', 'Expected "RuneName" but something is wrong', tok.ln)
        
        RuneName = RuneNameTok.value
        
        RuneTypeTok = Expect(type="TYPE")
        RuneType = None if IsError(RuneTypeTok) else RuneTypeTok.value
        
        twoDots = Expect(value=":")
        if IsError(twoDots): return HovaError('100', f'Expected rune finished. You can put ":" or a type value (optional).', tok.ln)
        
        if not DefinerValueIsCorrect():
            return HovaError('100', f'Expected a correct value to Rune Definer.', tok.ln)
        
        RuneValue = Parse_Primary()
        
        if IsError(RuneValue): return RuneValue

        if not TypeIsCorrect(RuneValue, RuneType):
            return HovaError('300', f'The Rune "{RuneName}" has a value with diferent type of <{RuneType}>', tok.ln)
    
        return Rune(RuneName, RuneType, RuneValue)
    
    def Parse_Detail():
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'temper':
            return HovaError('202', 'You are declaring a DetailDefiner outside a TemperEncompass', tok.ln)
        
        if NextIsNone():
            return HovaError('100', 'Expected "DetailName" after "det" literal', tok.ln)
        
        DetNameTok = Expect(type='IDENTIFIER')
        if IsError(DetNameTok): return HovaError('100', 'Expected "DetailName" but something is wrong', tok.ln)
        
        DetName = DetNameTok.value
        
        # type
        
        DetTypeTok = Expect(type='TYPE')
        DetType = None if IsError(DetTypeTok) else DetTypeTok.value
        
        if DetType and not TypeExist(DetType):
            return HovaError('300', f'This type from Det "{DetName}" not exist or is wrong', tok.ln)
        
        # :
        twoDots = Expect(value=':')
        if IsError(twoDots): return HovaError('100', f'Expected Detail finished. You can put ":" or a type value (optional) after {DetName}', tok.ln)
        
        # Value
        
        if not DefinerValueIsCorrect():
            return HovaError('100', f'Expected a correct value to Detail Definer.', tok.ln)
        
        DetValue = Parse_Primary()
        
        if IsError(DetValue): return DetValue
        
        if DetValue is not None and not TypeIsCorrect(DetValue, DetType):
            return HovaError('300', f'The Detail "{DetName}" has a value with different type of "{DetType}"', tok.ln)
    
        return Detail(DetName, DetType, DetValue)
    
    # Parse for Annotation
    
    def Parse_Seal():
        
        tok = tokens[pos]
        
        if NextIsNone() or ViewNext().type == "KEYWORD":
            return HovaError('100', f'Expected @SealName() after "seal" literal', tok.ln)
        
        atSignTok = Expect(value='@')
        if IsError(atSignTok): return atSignTok
        
        if NextIsNone(): return HovaError('100', f'Expected "@SealName()" after "seal" literal', tok.ln)
        
        SealNameTok = Expect(type="KEYWORD")
        if IsError(SealNameTok): return SealNameTok
        
        SealName = SealNameTok.value
        
        if not ViewNext().value == '(': return HovaError('100', f'Expected "(" after "@SealName()"', tok.ln)
        
        parenOpenTok = Expect(value='(')
        if IsError(parenOpenTok): return parenOpenTok
        
        SealArgs = []
        
        while True:  
            next = ViewNext()
            
            if next.value == ')':
                break
                
            if NextIsNone():
                return HovaError('100', f'Reached None with Seal arguments from {SealName}', next.ln)
        
            node = Parse_Primary()
            
            if not Next().value == ")" and not ViewNext() and not ViewNext().value == ',':
                return HovaError('100', f'Expected "," after each item', next.ln)
            
            virTok = Expect(value=',')
            if IsError(virTok): return virTok
            
            if IsError(node): return node
            
            if SealName == 'mark' and IsType(node['value'], 'StringLiteral'):
                return HovaError('200', f'@mark() just accept Strings as arguments.', next.ln)
            
            SealArgs.append(node)
            
        parenCloseTok = Expect(value=')')
        if IsError(parenCloseTok): return parenCloseTok
            
        return Seal(SealName, SealArgs)
                  
    
    # NOTE: Parse_Primary
    # Controls all tokens that are sended for it, when find a keyword it call the parser of keyword in specific
    # > PARSERCONTROLS
    # - StringLiteral, IntegerLiteral, FloatingLiteral and BooleanLiteral
    # - ArrayLiteral
    # - AnvilEncompass, AtomicEncompass, CharmEncompass, OreEncompass
    # - SparkDefiner, AtomDefiner, RuneDefiner
    # - () and []
    # - @SealName()
    
    def Parse_Primary():
        if NextIsNone():
            return None
        
        token = ConsumeToken()
        
        if token.value in ('be', 'end'):
            return None
            
        if token.type == "STRING":
            return Literal("StringLiteral", token.value)
        
        if token.type == "NUMBER_INTEGER":
            return Literal("IntegerLiteral", token.value)
        
        if token.type == "NUMBER_FLOATING":
            return Literal("FloatingLiteral", token.value)
        
        if token.type == "SYMBOL":
            
            if token.value == "[": 
                
                Items = []
                Items = Parse_Array(until=']')
                
                if IsError(Items): return Items
                
                return Literal("ArrayLiteral", Items)   
                            
            if token.value == "&":
                
                RuneNameTok = Expect(type='IDENTIFIER')
                if IsError(RuneNameTok): return RuneNameTok
                
                RuneName = RuneNameTok.value
                
                return CallFunction(callee="userune", args=[RuneName])
            
            if token.value == "!":
                
                DetNameTok = Expect(type='IDENTIFIER')
                if IsError(DetNameTok): return DetNameTok
                
                DetNameArg = DetNameTok.value
                
                return CallFunction(callee="usedetail", args=[DetNameArg]) 
               
            if token.value in ('(', ')', ',', ':'):
                return Literal("SymbolLiteral", token.value)
                            
        if token.type == "KEYWORD": 
            keyword = token.value.lower()
            
            # Encompass Conditions
            
            if keyword == "anvil":
                return Parse_Anvil()

            if keyword == 'ore':
                return Parse_Ore()  
            
            if keyword == "atomic":
                return Parse_Atomic()
            
            if keyword == "charm":
                return Parse_Charm() 
            
            if keyword == 'temper':
                return Parse_Temper()      
            
            
            # Definers Conditions
            
            if keyword == 'spark':
                return Parse_Spark()   
            
            if keyword == 'atom':
                return Parse_Atom()   
            
            if keyword == 'rune':
                return Parse_Rune() 
            
            if keyword == 'seal':
                return Parse_Seal()
            
            if keyword == 'det':
                return Parse_Detail()
            
            # To Namespace
            
            if keyword == 'hova':
                return Parse_Namespace()

            
            # OfStructure
            
            if keyword in ("true", "false"):
                return Literal("BooleanLiteral", token.value)  

        if token.type == "IDENTIFIER":
            return Identifier(token.value)
        
        return HovaError('100', f'Token "{token.value}" not exist', token.ln)
    
    
    
    
    # NOTE: The Initializer
    # AST receive nodes from Parse_Primary
    ast = []
    
    while ViewNext():
        ast_node = Parse_Primary()
        
        if IsError(ast_node):
            return ast_node   
     
        ast.append(ast_node)
        
    return ast

    