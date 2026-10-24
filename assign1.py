import os
import ply.lex as lex

tokens = (
    'FLOAT',
    'INTEGER',
    'IDENTIFIER',
    'EQ',
    'ASSIGN',
    'PLUS',
    'MINUS',
    'TIMES',
)

t_EQ     = r'=='
t_ASSIGN = r'='
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def process_file():
    filepath = input("Enter the input file path (e.g., sample_code.txt): ").strip()
    
    if not os.path.isfile(filepath):
        print(f"Error: The file '{filepath}' was not found.")
        return

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            source_content = f.read()

        lexer.input(source_content)

        print("\n" + "="*55)
        print(f"TOKENS GENERATED FROM: {filepath}")
        print("="*55)
        print(f"{'TOKEN TYPE':<15} {'VALUE':<20} {'LINE':<10} {'OFFSET':<10}")
        print("-" * 55)

        while True:
            tok = lexer.token()
            if not tok:
                break
            print(f"{tok.type:<15} {str(tok.value):<20} {tok.lineno:<10} {tok.lexpos:<10}")

    except Exception as err:
        print(f"Failed to read file: {err}")

if __name__ == '__main__':
    process_file()