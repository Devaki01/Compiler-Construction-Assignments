import ply.lex as lex

tokens = (
    'FLOAT',
    'INTEGER',
    'IDENTIFIER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'EQ',
    'ASSIGN',
)

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQ     = r'=='
t_ASSIGN = r'='

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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()


def run_lexer_on_text(data: str):
    """Feeds input text to lexer and prints generated tokens."""
    lexer.input(data)
    lexer.lineno = 1  
    
    print("\n--- GENERATED TOKENS ---")
    while True:
        tok = lexer.token()
        if not tok:
            break  
        print(f"Type: {tok.type:<12} Value: {str(tok.value):<15} Line: {tok.line:<5} LexPos: {tok.lexpos}")

if __name__ == "__main__":
    print("Enter your multiline C-like program (press Ctrl+D or Ctrl+Z then Enter to finish):")
    
    lines = []
    while True:
        try:
            line = input()
            lines.append(line)
        except EOFError:
            break
            
    input_program = "\n".join(lines)
    
    if input_program.strip():
        run_lexer_on_text(input_program)
    else:
        print("No input provided.")