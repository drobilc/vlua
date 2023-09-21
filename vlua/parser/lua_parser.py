from antlr4 import *
from .LuaLexer import LuaLexer
from .LuaParser import LuaParser

def parse(path):
    input_stream = FileStream(path)
    lexer = LuaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LuaParser(stream)
    return parser.chunk()