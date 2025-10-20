import re

# Supported data types in C
data_types = ['int', 'float', 'char', 'double']

def read_input_file():
    try:
        with open('input.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: input.txt not found.")
        return ""

def extract_symbols(code):
    symbol_table = []

    # Remove single-line and multi-line comments
    code = re.sub(r'//.*?(\n|$)|/\*.*?\*/', '', code, flags=re.S)

    # Remove function definitions (e.g., int main() { ... })
    code = re.sub(r'\b(' + '|'.join(data_types) + r')\s+\w+\s*\([^)]*\)\s*\{?', '', code)

    # Match only variable declarations (excluding function headers)
    declaration_pattern = re.compile(r'\b(' + '|'.join(data_types) + r')\b\s+([^;]+);')

    matches = declaration_pattern.findall(code)
    for dtype, variables in matches:
        # Split multiple variables (e.g., a = 5, b, c = 10)
        var_list = [v.strip() for v in variables.split(',')]
        for var in var_list:
            if '=' in var:
                parts = var.split('=', 1)
                name = parts[0].strip()
                value = parts[1].strip()
            else:
                name = var
                value = 'uninitialized'

            # Clean quotes in char or string literals (optional)
            if dtype == 'char' and not (value.startswith("'") and value.endswith("'")):
                value = f"'{value}'"

            symbol_table.append({
                'name': name,
                'type': dtype,
                'value': value
            })
    return symbol_table

def print_symbol_table(symbol_table):
    print("=== Symbol Table ===")
    print("{:<10} {:<10} {:<15}".format("Name", "Type", "Value"))
    print("-" * 37)
    for entry in symbol_table:
        print("{:<10} {:<10} {:<15}".format(entry['name'], entry['type'], entry['value']))

def main():
    code = read_input_file()
    if code:
        symbol_table = extract_symbols(code)
        print_symbol_table(symbol_table)

if __name__ == '__main__':
    main()
