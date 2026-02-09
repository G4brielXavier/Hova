
KEYWORDS = ["anvil", "ore", "atomic", "cave", "spark", "atom", "end", "true", "false", "dimension"]
TYPES = ["int", "float", "str", "bool", "list", "sufx"]
SYMBOLS = set("!()[],:")
SUFIXES = ['k', 'm', 'b', 't']

TypesIndex = {
    "StringLiteral": "str",
    "IntegerLiteral": "int",
    "FloatingLiteral": "float",
    "BooleanLiteral": "bool",
    "ArrayLiteral": "list",
    "SufixLiteral": "sufx"
}

TypesExtended = ["StringLiteral", "IntegerLiteral", "FloatingLiteral", "BooleanLiteral", "ArrayLiteral", "SufixLiteral"]
TypesAbrev = ["str", "int", "float", "list", "bool", "sufx"]