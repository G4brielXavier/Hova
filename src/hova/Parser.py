from .Tokenizer import Token

from .ErrorsTreatments import (
    HovaSyntaxError,
    HovaTypeError,
    HovaContextError,
    
    IsError
)

from .TokenConversions import (
    Literal,
    
    Identifier,
    
    Spark,
    Atom,
    Seal,
    
    AnvilEncompass,
    AtomicEncompass,
    OreEncompass,
    CaveEncompass,
    
    CallFunction,
)


TypesIndex = {
    "StringLiteral": "str",
    "IntegerLiteral": "int",
    "FloatingLiteral": "float",
    "BooleanLiteral": "bool",
    "ArrayLiteral": "list"
}

TypesExtended = ["StringLiteral", "IntegerLiteral", "FloatingLiteral", "BooleanLiteral", "ArrayLiteral"]
TypesAbrev = ["str", "int", "float", "list", "bool"]



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

    def Expect(value=None, type=None, no_error=False, msg=None):
        next = ViewNext()
        
        if not next:
            raise HovaSyntaxError(f'Expected "{value or type}" but got NULL.', tokens[pos-1].ln, tokens[pos-1].col)

        if no_error:
            if value is not None and next.value != value:
                return None
        
        if value is not None and next.value != value:
            raise HovaSyntaxError(f'Expected token value "{value}", but got "{next.value}"' if msg is None else msg, tokens[pos-1].ln, tokens[pos-1].col)
            
        if type is not None and next.type != type:
            raise HovaSyntaxError(f'Expected token type "{type}", but got "{next.type}"' if msg is None else msg, tokens[pos-1].ln, tokens[pos-1].col)
            
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
    
    def Parse_Block(until:str=None, encompassName:str=None, canEmpty:bool=False, insideOf:str=None, uniqueChild:bool=None, definerEncompass:list=None) -> list: 
        nodes = None
        
        if encompassName == 'OreEncompass':
            nodes = {
                "sparks": [],
                "ores": []
            }
        else:
            nodes = []
         
        while True:
            next = ViewNext()
            
            if not next:
                raise HovaSyntaxError(f'Expected "{until}" to close "{encompassName}", but reached EOF.', tokens[pos-1].ln, tokens[pos-1].col)

            if next.value == until:
                break
            
            if insideOf and context_stack[-1] != insideOf:
                raise HovaContextError(f'This is must be insideOf {insideOf}, so is {context_stack[-1]}', next.ln, next.col)
              
            before = pos
            node = Parse_Primary()
            
            if IsError(node): raise node
            
            if uniqueChild:
                for it in nodes:   
                    
                    if context_stack[-1] == 'anvil':
                        if node['type'] == 'AtomicEncompass':
                            continue
                    
                    # elif not node['type'] in ('StructLiteral', 'SymbolLiteral', 'IntegerLiteral', 'FloatingLiteral', 'BooleanLiteral'):                  
                    #     if it['name'] == node['name']:
                    #         return HovaError('202', f'Already exists a {definerEncompass} called "{node['name']}".', next.ln)
                        
            if node is None:
                raise HovaSyntaxError(f'Parser stalled in "{encompassName}". Token "{next.value}" not consumed.', next.ln, next.col)
            
            if pos == before:
                raise HovaSyntaxError(f'Infinite loop detected in "{encompassName}". Token "{next.value}"', next.ln, next.col)
            
            if not node['type'] in ('StructLiteral', 'SymbolLiteral'):
                
                if node['type'] == 'OreEncompass' or node['type'] == 'AtomicEncompass':
                    if encompassName == 'OreEncompass':
                        nodes['ores'].append(node)
                    else:
                        nodes.append(node)
                elif node['type'] == 'Spark':
                    if encompassName == 'OreEncompass':
                        nodes['sparks'].append(node)
                    else:
                        nodes.append(node)
                elif node['type'] == 'Atom':
                    nodes.append(node)
        
        untilTok = Expect(until)
        if IsError(untilTok): raise HovaSyntaxError(f'Expected "end" to close "{encompassName}" keyword', tokens[pos-1].ln, tokens[pos-1].col)
        
        return nodes
    
    def Parse_Array(until:str=None, arrayName:str=None):
        items = []
        
        while True:
            next = ViewNext()
            
            if not next:
                raise HovaSyntaxError(f'Expected "{until}" to close "{arrayName}", but reached EOF.', tokens[pos-1].ln, tokens[pos-1].col)
                
            if next.value == until:
                break
            
            before = pos
            node = Parse_Primary()

            if not ViewNext().value == "]" and ViewNext() and not ViewNext().value == ",":
                raise HovaSyntaxError(f'Expected "," after each item', tokens[pos-1].ln, tokens[pos-1].col)
            
            if not ViewNext().value == "]":
                virTok = Expect(value=',')
                if IsError(virTok): 
                    return virTok

            if node is None:
                raise HovaSyntaxError(f'Parser stalled in "{arrayName}". Token "{next.value}" not consumed', next.ln, next.col)
                
            if IsError(node): raise node
            
            if pos == before:
                raise HovaSyntaxError(f'Infinite loop detected in "{arrayName}"', next.ln, next.col)
                
            items.append(node)
            
                
        closedArray = Expect(until)
        if IsError(closedArray): raise HovaSyntaxError(f'Expected "]" to close the Array "{arrayName}"', next.ln, next.col)
        
        return items
            
    def Parse_Callee(kwName:str=None) -> dict:
        if not ViewNext() or ViewNext().value != "(":
            raise HovaSyntaxError(f'Expected "()" after "{kwName}" literal.', tokens[pos-1].ln, tokens[pos-1].col)
        
        parenOpenTok = Expect(value='(')
        if IsError(parenOpenTok): raise parenOpenTok # (
            
        args = []
        while True:
            next = ViewNext()
            
            if next.value == ')':
                break
            
            if NextIsNone():
                raise HovaSyntaxError('100', f'Reached None with CalleeFunction {kwName}', next.ln, next.col)
            
            node = Parse_Primary()
            
            if IsError(node): raise node
            
            args.append(node)
            
        parenCloseTok = Expect(value=')')
        if IsError(parenCloseTok): raise parenCloseTok # )
        
        return CallFunction(callee=kwName.lower(), args=args)
    
    def Parse_Namespace(setting) -> dict:
        namespaces = [setting]
        
        Expect(value='.')
        
        if ViewNext() and ViewNext().type == 'IDENTIFIER':
            node = Parse_Primary()
            if IsError(node): raise node
            namespaces.append(node['name'])
        
        Expect(value='.')
        
        if ViewNext() and ViewNext().type == 'IDENTIFIER':
            node = Parse_Primary()
            if IsError(node): raise node
            namespaces.append(node['name'])

        return namespaces
    
    def Parse_Arguments(name:str, fromName:str):
        args = []
        
        if not ViewNext() or not ViewNext().value == '(':
            raise HovaSyntaxError('100', f'Expected "(" in "{fromName}"', tokens[pos].ln, tokens[pos].col)
        
        ParenOpen = Expect(value='(')
        if IsError(ParenOpen): raise ParenOpen
        
        while True:
            next = ViewNext()
            
            if next.value == ')':
                break 
            
            if NextIsNone():
                raise HovaSyntaxError(f'Reached None in "{name}" {fromName}.', next.ln, next.col)
        
            before = pos
            node = Parse_Primary()
            
            if not ViewNext().value == ')' and ViewNext() and not ViewNext().value == ',':
                raise HovaSyntaxError(f'Expected "," after each item.', next.ln, next.col)
            
            if not ViewNext().value == ')':
                virTok = Expect(value=',')
                if IsError(virTok): raise virTok
                
            if node is None:
                raise HovaSyntaxError(f'Parser stalled in "{fromName}". Token "{next.value}" not consumed.', next.ln, next.col)
        
            if IsError(node): raise node
            
            if pos == before:
                raise HovaSyntaxError(f'Infinite loop detected in "{fromName}". Token "{next.value}"', next.ln, next.col)                
    
            args.append(node)
            
        ParenClosed = Expect(value=')')
        if IsError(ParenClosed): 
            return HovaSyntaxError('100', f'Expected ")" to close "TemperArguments"', tokens[pos-1].ln, tokens[pos-1].col)

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
            if not t in TypesExtended:
                raise HovaTypeError(f'This {t} type not exist.', value.ln, value.col)
        
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
            raise HovaSyntaxError("Expected 'AnvilName' after 'anvil' keyword", tokens[pos-1].ln, tokens[pos-1].col)
        
        tok = tokens[pos]
        
        context_stack.append('anvil')
        
        # ==========================================================
        # AnvilName
        AnvilNameTok = Expect(type="IDENTIFIER")
        if IsError(AnvilNameTok): raise AnvilNameTok
        
        AnvilName = AnvilNameTok.value
        
        # ==========================================================
        
        children = Parse_Block(
            until='end', 
            encompassName="AnvilEncompass",
            definerEncompass=["OreEncompass", "AtomicEncompass", "CaveEncompass"],
            canEmpty=True,
            uniqueChild=True
        )
        
        if IsError(children):
            raise children 
        
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
        return AnvilEncompass(
            name=AnvilName,
            atomic=AnvilAtomic,
            children=children,
            line=tok.ln,
            col=tok.col
        )

    def Parse_Atomic():
        
        if not context_stack or not context_stack[-1] == 'anvil':
            raise HovaContextError('You are declaring an AtomicEncompass outside an AnvilEncompass', tokens[pos-1].ln, tokens[pos-1].col)
        
        if NextIsNone():
            raise HovaSyntaxError("There is something wrong with AtomicEncompass", tok.ln, tok.col)
        
        tok = tokens[pos]
        
        if not context_stack[-1] == 'anvil':
            raise HovaContextError("'AtomicEncompass' must be inside an 'AnvilEncompass'.", tok.ln, tok.col)
    
        if context_stack[0] == 'anvil' and ViewNext().value == 'end' or not ViewNext().value in ('ore', 'cave'):
            context_stack.append('atomic')
        
        atoms = []
        
        if not Next():
            raise HovaSyntaxError("Expected 'end' to close 'AtomicEncompass'", tok.ln, tok.col)
        
        if context_stack[0] == 'anvil':
            if Next() is None:
                raise HovaSyntaxError("Expected 'end' to close 'AtomicEncompass'", tok.ln, tok.col)
        
        atomsChildren = Parse_Block(
            until='end', 
            encompassName="AtomicEncompass", 
            definerEncompass=["AtomDefiner"],
            canEmpty=True,
            uniqueChild=True
        )
            
        if IsError(atoms):
            raise atoms
                
        if NextIsNone():
            raise HovaSyntaxError("Expected 'end' to close 'AtomicEncompass'", tok.ln, tok.col)

        if context_stack[-1] == "anvil" and ViewNext() and ViewNext().value != 'end':
            raise HovaSyntaxError("Expected 'end' to close 'AtomicEncompass'", tok.ln, tok.col)

        context_stack.pop()
        return AtomicEncompass(
            atoms=atomsChildren,
            line=tokens[pos].ln,
            col=tokens[pos].col
        )
    
    def Parse_Cave():
        
        if not context_stack or not context_stack[-1] == 'anvil':
            raise HovaContextError('You are declaring an CaveEncompass outside an AnvilEncompass', tokens[pos-1].ln, tokens[pos-1].col) 
        
        if NextIsNone():
            raise HovaSyntaxError("Expected 'CaveName' after 'cave' keyword", tokens[pos-1].ln, tokens[pos-1].col)
    
        tok = tokens[pos]
        context_stack.append('cave')
        
        # ==============================================
        # CaveName
        CaveNameTok = Expect(type='IDENTIFIER')
        if IsError(CaveNameTok): raise CaveNameTok
        
        CaveName = CaveNameTok.value
        
        # ===============================================
    
        children = Parse_Block(
            until='end',
            encompassName="CaveEncompass",
            uniqueChild=True
        )

        if IsError(children): raise children
        
        # ===============================================
        
        context_stack.pop()
        return CaveEncompass(
            CaveName, 
            children, 
            tok.ln, 
            tok.col
        )
    
    def Parse_Ore():
    
        if not context_stack:
            if not context_stack[-1] == 'anvil':
                raise HovaContextError('You are declaring an OreEncompass outside an AnvilEncompass', tokens[pos-1].ln, tokens[pos-1].col)
            
            if not context_stack[-1] == 'cave':
                raise HovaContextError('You are declaring an OreEncompass outside an AnvilEncompass or CaveEncompass', tokens[pos-1].ln, tokens[pos-1].col)
        
        if NextIsNone():
            raise HovaSyntaxError("Expected 'OreName' after 'ore' keyword", tok.ln, tok.col)
            
        tok = tokens[pos]
        
        # If ore is not inside an anvil
        if not context_stack[0] == 'anvil':
            raise HovaContextError("'OreEncompass' must be inside an 'AnvilEncompass'.", tok.ln, tok.col)
    
        if context_stack[0] == 'anvil' and not ViewNext().type == 'IDENTIFIER':
            raise HovaSyntaxError("Expected 'OreName' after 'ore' keyword", tok.ln, tok.col)
        
        context_stack.append('ore')
        
        # 1. Get the Ore name
        NameTok = Expect(type="IDENTIFIER")
        if IsError(NameTok): raise NameTok
        EntityName = NameTok.value
        
        if context_stack[0] == 'anvil':        
            if Next() is None:
                raise HovaSyntaxError("Expected 'end' after 'OreName' identifier", tok.ln, tok.col)
        
        children = Parse_Block(
            until='end', 
            encompassName='OreEncompass', 
            definerEncompass=['SparkDefiner', 'OreEncompass'],
            canEmpty=True, 
            uniqueChild=True
        )
        
        # Verify if its an error
        if IsError(children): raise children
        
        # Sparks = []
        # Seals = []

        # If its block, get seals and sparks separatelly 
            
        # for child in children:
            
        #     if child['type'] == 'Seal':
        #         Seals.append(child)
        #     else:
        #         Sparks.append(child)
                    
        context_stack.pop()
        return OreEncompass(
            seals=[],
            name=EntityName, 
            sparks=children['sparks'] if len(children['sparks']) > 0 else [],
            child_ores=children['ores'] if len(children['ores']) > 0 else [],
            line=tokens[pos].ln,
            col=tokens[pos].col
        )   

    # Parses for Definers
    
    def Parse_Spark():
        # PromptTest = spark Sides int : 4
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'ore':
            raise HovaContextError('You are declaring a SparkDefiner outside an OreEncompass', tok.ln, tok.col)
        
        if NextIsNone():
            raise HovaSyntaxError('Expected "SparkName" after "spark" literal.', tok.ln, tok.col)

        # 1 = Sides                           
        SparkNameTok = Expect(type="IDENTIFIER")
        if IsError(SparkNameTok): raise HovaSyntaxError('Expected "SparkName" but something is wrong', tok.ln, tok.col)
        
        SparkName = SparkNameTok.value
        
        # 2 - Types (int, str, bool, list, float) [OPTIONAL]
        SparkTypeTok = None
        if ViewNext().type != "SYMBOL": SparkTypeTok = Expect(type="TYPE")
        SparkType = None if IsError(SparkTypeTok) or SparkTypeTok is None else SparkTypeTok.value
        
        if SparkType and not TypeExist(SparkType):
            raise HovaTypeError(f'This type from Spark {SparkName} not exist or is wrong', tok.ln, tok.col)
        
        # 3 - :
        twoDots = Expect(value=":")
        if IsError(twoDots): raise HovaSyntaxError(f'Expected spark finished. You can put ":" or a type value (optional).', tok.ln, tok.col)

        # 4 - 4
        if not DefinerValueIsCorrect():
            raise HovaSyntaxError(f'Expected a correct value to Spark Definer', tok.ln, tok.col)
        
        SparkValue = Parse_Primary()
        
        if IsError(SparkValue): raise SparkValue
        
        if SparkType is not None and not TypeIsCorrect(SparkValue, SparkType):
            raise HovaTypeError(f'The Spark "{SparkName}" has a value with different type of {SparkType}', tok.ln, tok.col)
                 
        return Spark(SparkName, SparkType, SparkValue)   
    
    def Parse_Atom():
        tok = tokens[pos]
        
        if not context_stack or not context_stack[-1] == 'atomic':
            raise HovaContextError('You are declaring an AtomDefiner outside an AtomicEncompass', tok.ln, tok.col)
        
        if NextIsNone():
            raise HovaSyntaxError('Expected "AtomName" after "atom" literal.', tok.ln, tok.col)
    
        
        AtomNameTok = Expect(type="IDENTIFIER")
        if IsError(AtomNameTok): 
            AtomNameTok = Expect(type="KEYWORD")
            if AtomNameTok and AtomNameTok.value == "hova":
                AtomName = Parse_Namespace(AtomNameTok.value) 
            
                if IsError(AtomName): raise AtomName
        else:
            AtomName = AtomNameTok.value
        
        if IsError(AtomNameTok): raise HovaSyntaxError('Expected "AtomName" after "atom" literal.', tok.ln, tok.col)
    
        twoDots = Expect(value=":")
        if IsError(twoDots): raise HovaSyntaxError(f'Expected ":" after "{AtomName}"', tok.ln, tok.col)
        
        if not DefinerValueIsCorrect('StringLiteral') or ViewNext().value == "end":
            raise HovaTypeError(f'Expected a "str" to AtomDefiner', tok.ln, tok.col)

        
        AtomValue = Parse_Primary()

        
        if IsError(AtomValue): raise AtomValue
        
        isTyped = IsType(AtomValue, ['StringLiteral', "BooleanLiteral"])
        
        if not isTyped:
            raise HovaTypeError(f'Expected a "StringValue" to AtomDefiner', tok.ln, tok.col)
        
        if IsError(isTyped): raise isTyped
        
        return Atom(AtomName, AtomValue)

    # Parse for Annotation
    
    def Parse_Seal():
        
        tok = tokens[pos]
        
        if NextIsNone() or ViewNext().type == "KEYWORD":
            raise HovaSyntaxError(f'Expected @SealName() after "seal" literal', tok.ln, tok.col)
        
        atSignTok = Expect(value='@')
        if IsError(atSignTok): raise atSignTok
        
        if NextIsNone(): raise HovaSyntaxError(f'Expected "@SealName()" after "seal" literal', tok.ln, tok.col)
        
        SealNameTok = Expect(type="KEYWORD")
        if IsError(SealNameTok): raise SealNameTok
        
        SealName = SealNameTok.value
        
        if not ViewNext().value == '(': raise HovaSyntaxError(f'Expected "(" after "@SealName()"', tok.ln, tok.col)
        
        parenOpenTok = Expect(value='(')
        if IsError(parenOpenTok): raise parenOpenTok
        
        SealArgs = []
        
        while True:  
            next = ViewNext()
            
            if next.value == ')':
                break
                
            if NextIsNone():
                raise HovaSyntaxError(f'Reached None with Seal arguments from {SealName}', next.ln, tok.col)
        
            node = Parse_Primary()
            
            if not Next().value == ")" and not ViewNext() and not ViewNext().value == ',':
                raise HovaSyntaxError(f'Expected "," after each item', next.ln, tok.col)
            
            virTok = Expect(value=',')
            if IsError(virTok): raise virTok
            
            if IsError(node): raise node
            
            if SealName == 'mark' and IsType(node['value'], 'StringLiteral'):
                raise HovaTypeError(f'@mark() just accept Strings as arguments.', next.ln, tok.col)
            
            SealArgs.append(node)
            
        parenCloseTok = Expect(value=')')
        if IsError(parenCloseTok): raise parenCloseTok
            
        return Seal(SealName, SealArgs)
                  
    
    # NOTE: Parse_Primary
    # Controls all tokens that are sended for it, when find a keyword it call the parser of keyword in specific
    # > PARSERCONTROLS
    # - StringLiteral, IntegerLiteral, FloatingLiteral and BooleanLiteral
    # - ArrayLiteral
    # - AnvilEncompass, AtomicEncompass, OreEncompass
    # - SparkDefiner, AtomDefiner
    # - () and []
    # - @SealName()
    
    def Parse_Primary():
        if NextIsNone():
            return None
        
        token = ConsumeToken()
        
        if token.value in ('end'):
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
                            
        if token.type == "KEYWORD": 
            keyword = token.value.lower()
            
            # Encompass Conditions
            
            if keyword == "anvil":
                return Parse_Anvil()

            if keyword == 'ore':
                return Parse_Ore()  
            
            if keyword == "atomic":
                return Parse_Atomic()
            
            if keyword == 'cave':
                return Parse_Cave()  
            
            
            # Definers Conditions
            
            if keyword == 'spark':
                return Parse_Spark()   
            
            if keyword == 'atom':
                return Parse_Atom()   
            
            if keyword == 'seal':
                return Parse_Seal()
            
            # To Namespace
            
            if keyword == 'hova':
                return Parse_Namespace()

            
            # OfStructure
            
            if keyword in ("true", "false"):
                return Literal("BooleanLiteral", token.value)  

        if token.type == "IDENTIFIER":
            return Identifier(token.value)
        
        raise HovaSyntaxError(f'Token "{token.value}" not exist', token.ln, token.col)
    
    
    
    
    ast = []
    
    while ViewNext():
        ast_node = Parse_Primary()
        
        if IsError(ast_node):
            return ast_node   
     
        ast.append(ast_node)
        
    return ast

    