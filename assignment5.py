import re

TYPE_SIZES = {
    'int': 4,
    'float': 4,
    'double': 8,
    'char': 1,
    'short': 2,
    'long': 8
}

def generate_symbol_table(c_code, start_address=1000):
    symbol_table = []
    symbol_names = set()
    memory_array = []
    current_address = start_address

    lines = c_code.splitlines()
    in_multiline_comment = False

    decl_pattern = re.compile(r'\b(int|float|double|char|short|long)\s+([^;]+);')

    for line_no, line in enumerate(lines, start=1):
        clean_line = re.sub(r'//.*', '', line)

        if '/*' in clean_line and '*/' in clean_line:
            clean_line = re.sub(r'/\*.*?\*/', '', clean_line)
        elif '/*' in clean_line:
            in_multiline_comment = True
            clean_line = re.sub(r'/\*.*', '', clean_line)
        elif '*/' in clean_line and in_multiline_comment:
            in_multiline_comment = False
            clean_line = re.sub(r'.*?\*/', '', clean_line)
        elif in_multiline_comment:
            continue

        matches = decl_pattern.findall(clean_line)
        for data_type, vars_str in matches:
            variables = vars_str.split(',')
            for var in variables:
                var_name = var.split('=')[0].strip()
                var_name = re.sub(r'\[.*?\]', '', var_name)
                var_name = var_name.lstrip('*').strip()

                if var_name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', var_name):
                    if var_name not in symbol_names:
                        symbol_names.add(var_name)
                        bytes_used = TYPE_SIZES.get(data_type, 4)
                        mem_location = current_address

                        entry = {
                            'name': var_name,
                            'type': data_type,
                            'line': line_no,
                            'address': mem_location,
                            'bytes': bytes_used
                        }
                        symbol_table.append(entry)

                        memory_array.append({
                            'address': mem_location,
                            'symbol': var_name,
                            'type': data_type,
                            'bytes': bytes_used
                        })

                        current_address += bytes_used

    return symbol_table, memory_array


def display_tables(symbol_table, memory_array):
    print("=" * 75)
    print(f"{'SYMBOL NAME':<15} {'DATA TYPE':<12} {'LINE NO':<10} {'MEMORY LOC':<15} {'BYTES USED':<10}")
    print("=" * 75)
    for s in symbol_table:
        print(f"{s['name']:<15} {s['type']:<12} {s['line']:<10} {hex(s['address']):<15} {s['bytes']:<10}")
    print("=" * 75)

    print("\nSIMULATED MEMORY ARRAY:")
    print("-" * 50)
    print(f"{'INDEX':<8} {'ADDRESS':<12} {'SYMBOL':<15} {'SIZE (BYTES)':<10}")
    print("-" * 50)
    for idx, mem in enumerate(memory_array):
        print(f"[{idx}]{'':<4} {hex(mem['address']):<12} {mem['symbol']:<15} {mem['bytes']:<10}")
    print("-" * 50)

if __name__ == '__main__':
    sample_c_program = """
    #include <stdio.stdio>

    int main() {
        // Variable declarations
        int count = 10, total;
        float rate = 5.5;
        char flag = 'A';
        double distance;

        /* Multiline comment
           int ignored_var = 100; 
        */

        total = count * 2;
        return 0;
    }
    """

    table, memory = generate_symbol_table(sample_c_program)
    display_tables(table, memory)