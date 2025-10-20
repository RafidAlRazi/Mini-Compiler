import re

# Define token types
keywords = {'int', 'float', 'return', 'if', 'else', 'while', 'for', 'do', 'break', 'continue', 'void', 'char', 'double'}
operators = {'+', '-', '*', '/', '=', '==', '!=', '<', '>', '<=', '>='}
separators = {'(', ')', '{', '}', '[', ']', ';', ','}

# Regex patterns
token_specification = [
    ('NUMBER',   r'\d+(\.\d*)?'),     # Integer or decimal number
    ('ID',       r'[A-Za-z_]\w*'),    # Identifiers
    ('OP',       r'==|!=|<=|>=|[+\-*/=<>]'),  # Operators
    ('SEP',      r'[(){}[\];,]'),     # Separators
    ('SKIP',     r'[ \t]+'),          # Skip over spaces and tabs
    ('NEWLINE',  r'\n'),              # Line endings
    ('MISMATCH', r'.'),               # Any other character
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
get_token = re.compile(tok_regex).match

def tokenize(code):
    line_num = 1
    pos = 0
    mo = get_token(code, pos)
    while mo:
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            print(f'NUMBER     : {value}')
        elif kind == 'ID':
            if value in keywords:
                print(f'KEYWORD    : {value}')
            else:
                print(f'IDENTIFIER : {value}')
        elif kind == 'OP':
            print(f'OPERATOR   : {value}')
        elif kind == 'SEP':
            print(f'SEPARATOR  : {value}')
        elif kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            print(f'Unexpected character {value!r} on line {line_num}')
        pos = mo.end()
        mo = get_token(code, pos)

    if pos != len(code):
        print('Unexpected character %r on line %d' % (code[pos], line_num))


# Read from input.txt
with open('input.txt', 'r') as file:
    source_code = file.read()

print("Lexical Analysis Output:\n")
tokenize(source_code)
