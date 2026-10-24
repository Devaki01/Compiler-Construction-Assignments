import re

# Task 2: Add Additional Operators & Task 3: Add Error Handling
KEYWORDS = {
    'auto', 'break', 'case', 'char', 'const', 'continue', 'default', 'do',
    'double', 'else', 'enum', 'extern', 'float', 'for', 'goto', 'if',
    'int', 'long', 'register', 'return', 'short', 'signed', 'sizeof', 'static',
    'struct', 'switch', 'typedef', 'union', 'unsigned', 'void', 'volatile', 'while'
}

OPERATORS_SET = {
    '+', '-', '*', '/', '%', '=', '==', '!=', '<', '>', '<=', '>=',
    '&&', '||', '!', '&', '|', '^', '~', '<<', '>>', '++', '--',
    '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '->', '?', ':',
    ';', ',', '.', '(', ')', '{', '}', '[', ']'
}

# Sort operators by length descending so longer operators match first (e.g., '+=' before '+')
sorted_ops = sorted(OPERATORS_SET, key=len, reverse=True)
op_pattern = '|'.join(re.escape(op) for op in sorted_ops)

# Pre-compile regular expressions outside the loop for optimal performance
TOKEN_PATTERNS = [
    ('COMMENT', re.compile(r'//[^\n]*|/\*[\s\S]*?\*/')),
    ('WHITESPACE', re.compile(r'\s+')),
    ('NUMBER', re.compile(r'\b\d+(?:\.\d+)?\b')),
    ('IDENT_KEYWORD', re.compile(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b')),
    ('OPERATOR', re.compile(op_pattern))
]

def analyze_c_code(source_code):
    counts = {
        'Keywords': 0,
        'Identifiers': 0,
        'Operators': 0,
        'Numbers': 0,
        'Total Tokens': 0
    }
    warnings = []
    
    if not source_code or not source_code.strip():
        warnings.append("Warning: Input source code is empty.")
        return counts, warnings

    pos = 0
    length = len(source_code)

    while pos < length:
        matched = False
        for token_type, regex in TOKEN_PATTERNS:
            match = regex.match(source_code, pos)
            
            if match:
                matched_text = match.group(0)
                matched = True
                pos = match.end()
                
                if token_type in ('COMMENT', 'WHITESPACE'):
                    break
                elif token_type == 'NUMBER':
                    counts['Numbers'] += 1
                    counts['Total Tokens'] += 1
                elif token_type == 'OPERATOR':
                    counts['Operators'] += 1
                    counts['Total Tokens'] += 1
                elif token_type == 'IDENT_KEYWORD':
                    if matched_text in KEYWORDS:
                        counts['Keywords'] += 1
                    else:
                        counts['Identifiers'] += 1
                    counts['Total Tokens'] += 1
                break

        if not matched:
            unknown_char = source_code[pos]
            warnings.append(f"Warning: Unknown token '{unknown_char}' at position {pos}")
            pos += 1

    return counts, warnings


def display_results(counts, warnings=None):
    if warnings:
        print("Warnings/Errors:")
        for w in warnings:
            print(f"  {w}")
        print()

    print("Lexical Analysis Results:")
    print(f"Keywords: {counts['Keywords']}")
    print(f"Identifiers: {counts['Identifiers']}")
    print(f"Operators: {counts['Operators']}")
    print(f"Numbers: {counts['Numbers']}")
    print(f"Total Tokens: {counts['Total Tokens']}\n")


# Test Cases Execution
test_cases = [
    # Test Case 1: Standard Main Function
    """
    int main() {
        int count = 10;
        return 0;
    }
    """,
    
    # Test Case 2: Compound Operators & Arithmetic
    """
    void update() {
        x += 5;
        ptr->value = ~x ? y : z;
    }
    """,
    
    # Test Case 3: Comments & Floating-Point Numbers
    """
    // Calculation loop
    float radius = 3.14;
    /* Multi-line
       Comment */
    while (radius > 0) {
        radius -= 0.5;
    }
    """,
    
    # Test Case 4: Complex Conditionals
    """
    if (a >= 10 && b != 0) {
        c = (a % 2 == 0) ? 1 : 0;
    }
    """,
    
    # Test Case 5: Error Handling with Invalid Characters
    """
    int value = 100 @;
    $invalid_symbol = 5;
    """
]

for idx, code in enumerate(test_cases, 1):
    print(f"--- Test Case {idx} ---")
    counts, warnings = analyze_c_code(code)
    display_results(counts, warnings)

     