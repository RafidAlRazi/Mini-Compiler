import re

# ==============================
# 1️⃣ LEXICAL ANALYZER
# ==============================
def lexical_analysis(code):
    KEYWORDS = {'int', 'float', 'void', 'if', 'else', 'while', 'for', 'return', 'char', 'double'}
    token_specification = [
        ('COMMENT_LINE',    r'//.*'),
        ('COMMENT_MULTI',   r'/\*[\s\S]*?\*/'),
        ('LITERAL_STRING',  r'"([^"\\]|\\.)*"'),
        ('LITERAL_FLOAT',   r'\d+\.\d+'),
        ('LITERAL_INT',     r'\d+'),
        ('OPERATOR_MULTI',  r'==|!=|<=|>=|\+\+|--'),
        ('OPERATOR_SINGLE', r'[+\-*/=><]'),
        ('SEPARATOR',       r'[;,(){}[\]]'),
        ('KEYWORD_IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('SKIP',            r'\s+'),
        ('MISMATCH',        r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    print("\n" + "="*40)
    print("  LEXICAL ANALYSIS OUTPUT  ")
    print("="*40)

    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)

        if kind == 'SKIP' or kind.startswith('COMMENT'):
            continue
        elif kind == 'KEYWORD_IDENTIFIER':
            if value in KEYWORDS:
                tokens.append(("KEYWORD", value))
            else:
                tokens.append(("IDENTIFIER", value))
        elif kind.startswith('LITERAL'):
            tokens.append(("LITERAL", value))
        elif kind.startswith('OPERATOR'):
            tokens.append(("OPERATOR", value))
        elif kind == 'SEPARATOR':
            tokens.append(("SEPARATOR", value))
        elif kind == 'MISMATCH':
            print(f"!!! ERROR: Unexpected character '{value}' at position {mo.start()}")
        else:
            tokens.append((kind, value))

    for kind, val in tokens:
        print(f"{kind:<12}: '{val}'")

    return tokens


# ==============================
# 2️⃣ SYMBOL TABLE GENERATION
# ==============================
data_types = ['int', 'float', 'char', 'double']

def extract_symbols(code):
    symbol_table = []
    # Remove comments
    code = re.sub(r'//.*?(\n|$)|/\*.*?\*/', '', code, flags=re.S)
    # Remove function headers
    code = re.sub(r'\b(' + '|'.join(data_types) + r')\s+\w+\s*\([^)]*\)\s*\{?', '', code)
    # Match variable declarations
    declaration_pattern = re.compile(r'\b(' + '|'.join(data_types) + r')\b\s+([^;]+);')

    matches = declaration_pattern.findall(code)
    for dtype, variables in matches:
        var_list = [v.strip() for v in variables.split(',')]
        for var in var_list:
            if '=' in var:
                parts = var.split('=', 1)
                name = parts[0].strip()
                value = parts[1].strip()
            else:
                name = var
                value = 'uninitialized'
            symbol_table.append({
                'name': name,
                'type': dtype,
                'value': value
            })
    return symbol_table

def print_symbol_table(symbol_table):
    print("\n" + "="*40)
    print("          SYMBOL TABLE")
    print("="*40)
    print("{:<10} {:<10} {:<15}".format("Name", "Type", "Value"))
    print("-" * 37)
    for entry in symbol_table:
        print("{:<10} {:<10} {:<15}".format(entry['name'], entry['type'], entry['value']))


# ==============================
# 3️⃣ THREE ADDRESS CODE (TAC)
# ==============================
temp_counter = 1
tac_output = []

def new_temp():
    global temp_counter
    t = f"t{temp_counter}"
    temp_counter += 1
    return t

def generate_tac(expr, target):
    global tac_output
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[-+*/=()]', expr)

    def process_operators(tokens, ops):
        i = 0
        while i < len(tokens):
            if tokens[i] in ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                t = new_temp()
                tac_output.append(f"{t} = {left} {op} {right}")
                tokens = tokens[:i - 1] + [t] + tokens[i + 2:]
                i = 0
            else:
                i += 1
        return tokens

    tokens = process_operators(tokens, ['*', '/'])
    tokens = process_operators(tokens, ['+', '-'])

    if len(tokens) == 1:
        tac_output.append(f"{target} = {tokens[0]}")
    else:
        tac_output.append(f"{target} = {' '.join(tokens)}")

def extract_tac(code):
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    code = re.sub(r'\b(int|float|char|double)\b[^;]*;', '', code)
    assignments = re.findall(r'([a-zA-Z_]\w*)\s*=\s*([^;]+);', code)
    for target, expr in assignments:
        generate_tac(expr.strip(), target.strip())
    return tac_output


# ==============================
# 4️⃣ ASSEMBLY CODE GENERATION
# ==============================
reg_counter = 1
assembly_output = []

def new_register():
    global reg_counter
    reg = f"R{reg_counter}"
    reg_counter += 1
    return reg

def generate_assembly(expr, target):
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[-+*/=()]', expr)

    def process_operators(tokens, ops):
        global assembly_output
        i = 0
        while i < len(tokens):
            if tokens[i] in ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                reg = new_register()
                assembly_output.append(f"MOV {reg}, {left}")
                if op == '*':
                    assembly_output.append(f"MUL {reg}, {right}")
                elif op == '/':
                    assembly_output.append(f"DIV {reg}, {right}")
                elif op == '+':
                    assembly_output.append(f"ADD {reg}, {right}")
                elif op == '-':
                    assembly_output.append(f"SUB {reg}, {right}")
                tokens = tokens[:i - 1] + [reg] + tokens[i + 2:]
                i = 0
            else:
                i += 1
        return tokens

    tokens = process_operators(tokens, ['*', '/'])
    tokens = process_operators(tokens, ['+', '-'])
    if len(tokens) == 1:
        assembly_output.append(f"MOV {target}, {tokens[0]}")
    else:
        assembly_output.append(f"MOV {target}, {' '.join(tokens)}")

def extract_assembly(code):
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    code = re.sub(r'\b(int|float|char|double)\b[^;]*;', '', code)
    assignments = re.findall(r'([a-zA-Z_]\w*)\s*=\s*([^;]+);', code)
    for target, expr in assignments:
        generate_assembly(expr.strip(), target.strip())
    return assembly_output


# ==============================
# 🚀 MAIN PIPELINE
# ==============================
def main():
    try:
        with open('input.txt', 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    # 1. Lexical Analysis
    lexical_analysis(code)

    # 2. Symbol Table
    symbol_table = extract_symbols(code)
    print_symbol_table(symbol_table)

    # 3. Three Address Code
    tac = extract_tac(code)
    print("\n" + "="*40)
    print("     THREE ADDRESS CODE (TAC)")
    print("="*40)
    for line in tac:
        print(line)

    # 4. Assembly Code
    asm = extract_assembly(code)
    print("\n" + "="*40)
    print("        ASSEMBLY CODE")
    print("="*40)
    for line in asm:
        print(line)

if __name__ == '__main__':
    main()
