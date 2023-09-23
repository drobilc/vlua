from luaparser import ast

def parse(path):
    with open(path, 'r') as input_file:
        content = input_file.read()
        return ast.parse(content)