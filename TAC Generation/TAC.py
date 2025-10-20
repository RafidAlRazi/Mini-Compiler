import re

temp_counter = 1
tac_output = []

def new_temp():
    global temp_counter
    temp_name = f"t{temp_counter}"
    temp_counter += 1
    return temp_name

# Convert a single expression into TAC
def generate_tac(expr, target):
    global tac_output
    tokens = re.findall(r'[a-zA-Z_]\w*|\d+|[-+*/=()]', expr)

    # Handle operator precedence: (* and / before + and -)
    def process_operators(tokens, ops):
        i = 0
        while i < len(tokens):
            if tokens[i] in ops:
                left = tokens[i - 1]
                op = tokens[i]
                right = tokens[i + 1]
                temp = new_temp()
                tac_output.append(f"{temp} = {left} {op} {right}")
                # Replace the 3 tokens with temp
                tokens = tokens[:i - 1] + [temp] + tokens[i + 2:]
                i = 0  # Restart after replacement
            else:
                i += 1
        return tokens

    tokens = process_operators(tokens, ['*', '/'])
    tokens = process_operators(tokens, ['+', '-'])

    # Final assignment
    if len(tokens) == 1:
        tac_output.append(f"{target} = {tokens[0]}")
    else:
        tac_output.append(f"{target} = {' '.join(tokens)}")

# Extract expressions from code and convert to TAC
def extract_expressions(code):
    # Remove comments
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', code, flags=re.S)
    # Remove variable declarations
    code = re.sub(r'\b(int|float|char|double)\b[^;]*;', '', code)

    # Find assignments like: a = b + c * d;
    assignments = re.findall(r'([a-zA-Z_]\w*)\s*=\s*([^;]+);', code)

    for target, expr in assignments:
        generate_tac(expr.strip(), target.strip())

def main():
    try:
        with open('input.txt', 'r') as file:
            code = file.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return

    extract_expressions(code)

    print("=== Three Address Code (TAC) ===")
    for line in tac_output:
        print(line)

if __name__ == '__main__':
    main()
