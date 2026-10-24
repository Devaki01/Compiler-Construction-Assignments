import sys
import ply.lex as lex
import ply.yacc as yacc

# --- 1. LEXER (ply.lex) ---

tokens = ('NUMBER', 'PLUS', 'MINUS', 'MULTIPLY', 'DIVIDE')

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'

# Regular expression rule with action for numbers (supports ints and floats)


def t_NUMBER(t):
  r'\d+(\.\d+)?'
  try:
    # Convert to float first, then check if it can be represented as an integer
    fval = float(t.value)
    if fval.is_integer():
      t.value = int(fval)
    else:
      t.value = fval
  except ValueError:
    print(f'Numerical value error: {t.value}')
    t.value = 0
  return t


# Ignored characters (spaces and tabs)
t_ignore = ' \t'

# Tracks whether an illegal character was seen while tokenizing the
# current line, so the parser result (built on a silently-skipped
# token stream) isn't printed as if it were valid.
lex_has_error = False


# Error handling rule for lexer
def t_error(t):
  global lex_has_error
  lex_has_error = True
  print(f"Illegal character '{t.value[0]}'")
  t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# --- 2. PARSER (ply.yacc) ---

# Grammar rules and semantic actions for postfix evaluation


def p_calc(p):
  '''calc : expression'''
  p[0] = p[1]


def p_expression_binop(p):
  '''expression : expression expression PLUS
                | expression expression MINUS
                | expression expression MULTIPLY
                | expression expression DIVIDE'''
  if p[3] == '+':
    p[0] = p[1] + p[2]
  elif p[3] == '-':
    p[0] = p[1] - p[2]
  elif p[3] == '*':
    p[0] = p[1] * p[2]
  elif p[3] == '/':
    if p[2] == 0:
      print('Error: Division by zero!')
      p[0] = 0
    else:
      p[0] = p[1] / p[2]


def p_expression_number(p):
  '''expression : NUMBER'''
  p[0] = p[1]


# Error rule for syntax errors


def p_error(p):
  if p:
    print(f"Syntax error at token '{p.value}'")
  else:
    print('Syntax error at end of input')


# Build the parser
parser = yacc.yacc()

# --- 3. MAIN INTERACTIVE EXECUTION ---
if __name__ == '__main__':
  print('==================================================')
  print('      PLY POSTFIX EXPRESSION EVALUATOR            ')
  print('==================================================')
  print("Enter postfix expressions (e.g., '3 4 + 2 *' or '5.5 2.0 *')")
  print("Type 'exit' or 'quit' to stop.\n")

  while True:
    try:
      s = input('postfix> ')
    except EOFError:
      break
    except KeyboardInterrupt:
      print()  # move past the '^C' the terminal echoes
      break
    if not s:
      continue
    if s.strip().lower() in ['exit', 'quit']:
      break

    lex_has_error = False
    result = parser.parse(s)
    if lex_has_error:
      # Input contained characters the lexer had to skip; the result
      # (if any) was computed from an incomplete token stream, so
      # don't present it as a valid answer.
      continue
    if result is not None:
      print(f'Result = {result}\n')