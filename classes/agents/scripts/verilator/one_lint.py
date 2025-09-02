import re
import sys

def check_signal_declaration(content, file_path):
    bit_signals = re.findall(r'\bbit\b\s+(\w+)', content)
    if bit_signals:
        print("Signals declared as 'bit':")
        for signal in bit_signals:
            print(f"  - {signal}")
    else:
        print("No signals declared as 'bit'.")

def check_always_block(content, file_path):
    YELLOW = "\033[93m"
    RESET = "\033[0m"    
    valid_always_blocks = ['always_comb', 'always_ff', 'always_latch']
    lines = content.splitlines()
    for i, line in enumerate(lines, start=1):
        always_match = re.search(r'\b(always_[a-zA-Z]+)\b|\balways\b\s*@', line)
        if always_match:
            block_type = always_match.group(0)
            if block_type in valid_always_blocks:
                pass
            elif block_type == 'always':  # Pure always block
                print(f"{YELLOW}ALWAYS{RESET}: 'always' - line {i}. should be 'always_ff', 'always_comb', or 'always_latch' - file {file_path}")
            else:
                print(f"{YELLOW}ALWAYS{RESET}: 'always' - line {i}. should be 'always_ff', 'always_comb', or 'always_latch' - file {file_path}")

def find_always_blocks(content):
    always_pattern = r'always_ff\s*@\([^)]+\)\s*begin'
    end_pattern = r'\bend\b'
    always_blocks = []
    start_positions = [m.start() for m in re.finditer(always_pattern, content)]
    for start in start_positions:
        depth = 0
        end_pos = start
        for match in re.finditer(r'\bbegin\b|\bend\b', content[start:]):
            if match.group() == 'begin':
                depth += 1
            elif match.group() == 'end':
                depth -= 1
            if depth == 0:
                end_pos = start + match.end()
                break
        always_blocks.append((content[start:end_pos], start))  # Include block and start position
    return always_blocks

def find_line_numbers(content, start_idx, signals):
    lines = content[:start_idx].splitlines()  # All lines before the start of the always block
    line_offset = len(lines)  # Start counting lines from here
    block_lines = content[start_idx:].splitlines()
    line_numbers = {}
    for signal in signals:
        for idx, line in enumerate(block_lines, start=line_offset + 1):
            if signal in line:
                line_numbers[signal] = idx
                break
    return line_numbers

def check_blocking_assignments(content, file_path):
    YELLOW = "\033[93m"
    RESET = "\033[0m"    
    blocking_assignments = re.findall(r'^(?!for\b)\w+\s*=\s*', content, re.MULTILINE)
    #blocking_assignments = re.findall(r'(\w+)\s*= ', content)
    lines = content.splitlines()
    line_numbers = {}
    for signal in blocking_assignments:
        for idx, line in enumerate(lines, start=1):
            if re.search(rf'\b{signal}\s*=', line):
                line_numbers[signal] = idx
                break
    for signal in blocking_assignments:
        if not signal.startswith(('w_', 'o_','s_','m_','v_','e_', 'if_')):
            if (signal.islower()): 
                print(f"{YELLOW}NONBLK_NM{RESET}: {signal} - line {line_numbers[signal]} : should start with 'w_' - file {file_path}")

def parse_systemverilog(file_paths):
    YELLOW = "\033[93m"
    RESET = "\033[0m"    
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            content = f.read()
        if ("one_lint_off" in content):
            continue
        always_blocks = find_always_blocks(content)
        for idx, (block, start_idx) in enumerate(always_blocks):
            assignments = re.findall(r'(\w+)\s*<=', block)
            line_numbers = find_line_numbers(content, start_idx, assignments)
            for signal in assignments:
                if not signal.startswith(('r_', 's_', 'c_', 'e_')):
                    print(f"{YELLOW}RGST_NM{RESET}: {signal} - line {line_numbers[signal]} : should start with 'r_', 's_', or 'c_' - file {file_path}")
        check_blocking_assignments(content, file_path)
        check_always_block(content, file_path)


if __name__ == "__main__":
    file_paths = sys.argv[1:]
    parse_systemverilog(file_paths)


