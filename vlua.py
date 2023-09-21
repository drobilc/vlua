import argparse
from vlua.parser.lua_parser import parse
from vlua.generator.html_generator import generate_html

if __name__ == '__main__':

    # Configure Python's argument parser.
    parser = argparse.ArgumentParser(
        prog='vlua',
        description='A tool for converting Lua code into visual representations for enhanced program comprehension.',
    )
    
    # Add required argument "filename" - the path to the lua file that we want
    # to convert into visual language.
    parser.add_argument(
        'filename',
        help='Path to the input Lua file that will be converted to visual representation.'
    )

    # Add optional argument 
    parser.add_argument(
        '--output-file', '-o',
        help='Path to the visual representation of the input lua program.' \
            'If not provided, the generated data will be printed directly to the console.'
    )

    arguments = parser.parse_args()

    # Step 1: Read input file and perform lexing and parsing steps using antlr4
    # parsing library. The output will be an abstract syntax tree (ast)
    # representation of the program.
    ast = parse(arguments.filename)

    # Step 2: Convert the abstract syntax tree to HTML using a visitor
    # [HtmlGenerator]. See [vlua.generator.html_generator] for implementation.
    html = generate_html(ast)

    # Step 3: If the [arguments.output_file] is set, save the generated HTML,
    # otherwise print it to console.
    if arguments.output_file is not None:
        with open(arguments.output_file, 'w+') as output_file:
            output_file.write(html)
    else:
        print(html)