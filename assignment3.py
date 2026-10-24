def remove_c_comments(c_code: str):
    i = 0
    n = len(c_code)

    in_single_comment = False
    in_multi_comment = False
    in_string = False
    in_char = False

    current_line = 1
    line_buffers = {1: []}

    while i < n:
        char = c_code[i]
        next_char = c_code[i + 1] if i + 1 < n else ""

        if char == "\n":
            if in_single_comment:
                in_single_comment = False

            current_line += 1
            line_buffers[current_line] = []
            i += 1
            continue

        if in_single_comment:
            i += 1
            continue

        if in_multi_comment:
            if char == "*" and next_char == "/":
                in_multi_comment = False
                i += 2
            else:
                i += 1
            continue

        if in_string:
            line_buffers[current_line].append(char)
            if char == "\\":  # Handle escaped characters like \"
                if i + 1 < n:
                    line_buffers[current_line].append(c_code[i + 1])
                    i += 2
                    continue
            elif char == '"':
                in_string = False
            i += 1
            continue

        if in_char:
            line_buffers[current_line].append(char)
            if char == "\\":  # Handle escaped characters like '\''
                if i + 1 < n:
                    line_buffers[current_line].append(c_code[i + 1])
                    i += 2
                    continue
            elif char == "'":
                in_char = False
            i += 1
            continue

        if char == "/" and next_char == "/":
            in_single_comment = True
            i += 2
        elif char == "/" and next_char == "*":
            in_multi_comment = True
            i += 2
        elif char == '"':
            in_string = True
            line_buffers[current_line].append(char)
            i += 1
        elif char == "'":
            in_char = True
            line_buffers[current_line].append(char)
            i += 1
        else:
            line_buffers[current_line].append(char)
            i += 1

    output_lines = []
    line_numbers = []

    for line_num in sorted(line_buffers.keys()):
        line_content = "".join(line_buffers[line_num])
        if line_content.strip():
            output_lines.append(line_content)
            line_numbers.append(line_num)

    return "\n".join(output_lines), line_numbers

c_program = """int main()
{
// test program
printf("("hello world");
}"""

output_code, original_lines = remove_c_comments(c_program)

print("Output:")
print(output_code)
print("\nArray:")
print(" ".join(map(str, original_lines)))