import sys
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

def main():
    print("Enter code (Press Ctrl+D on Linux/macOS or Ctrl+Z then Enter on Windows to finish):")
    code_input = sys.stdin.read()
    
    lexer.input(code_input)
    
    print("\n" + "="*55)
    print(f"{'TOKEN TYPE':<15} {'VALUE':<20} {'LINE':<10} {'OFFSET':<10}")
    print("="*55)
    
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"{tok.type:<15} {str(tok.value):<20} {tok.lineno:<10} {tok.lexpos:<10}")

if __name__ == '__main__':
    main()