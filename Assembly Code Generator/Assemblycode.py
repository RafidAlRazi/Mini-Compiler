import re

reg_counter = 1
assembly_output = []

def new_register():
    global reg_counter
    reg = f"R{reg_counter}"
    reg_counter += 1
    return reg

# Converts a single expression into pseudo-assembly code
def generate_assembly(expr, target):
    global assembly_output
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[-+*/=()]', expr)

    def process_operators(tokens, ops):
        global assembly_output
        i = 0
        while i < len(tokens):
            if tokens[i] in ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]

                reg1 = new_register()
                if op in ['*', '/']:
                    assembly_output.append(f"MOV {reg1}, {left}")
                    if op == '*':
                        assembly_output.append(f"MUL {reg1}, {right}")
                    else:
                        assembly_output.append(f"DIV {reg1}, {right}")
                elif op in ['+', '-']:
                    assembly_output.append(f"MOV {reg1}, {left}")
                    if op == '+':
                        assembly_output.append(f"ADD {reg1}, {right}")
                    else:
                        assembly_output.append(f"SUB {reg1}, {right}")

                # Replace the 3 tokens with reg1
                tokens = tokens[:i - 1] + [reg1] + tokens[i + 2:]
                i = 0  # restart
            else:
                i += 1
        return tokens

    tokens = process_operators(tokens, ['*', '/'])
    tokens = process_operators(tokens, ['+', '-'])

    # Final assignment
    if len(tokens) == 1:
        assembly_output.append(f"MOV {target}, {tokens[0]}")
    else:
        assembly_output.append(f"MOV {target}, {' '.join(tokens)}")

# Extract expressions from code and convert to assembly
def extract_expressions(code):
    # Remove comments
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)

    # Remove variable declarations
    code = re.sub(r'\b(int|float|char|double)\b[^;]*;', '', code)

    # Find assignments
    assignments = re.findall(r'([a-zA-Z_]\w*)\s*=\s*([^;]+);', code)

    for target, expr in assignments:
        generate_assembly(expr.strip(), target.strip())

def main():
    try:
        with open('input.txt', 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    extract_expressions(code)

    print("=== Assembly Code ===")
    for line in assembly_output:
        print(line)

if __name__ == '__main__':
    main()
