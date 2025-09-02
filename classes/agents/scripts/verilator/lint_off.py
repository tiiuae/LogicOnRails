import sys

def lint_off(file_name, start_string="x", end_string="y", add_char="z"):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    start_line_found = False

    # Iterate through the lines and modify them as needed
    for i, line in enumerate(lines):
        if start_string in line:
            start_line_found = True
        
        if start_line_found:
            lines[i] = add_char + line
        
        if start_line_found and end_string in line:
            start_line_found = False

    # Write the modified lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)


def lint_on(file_name, start_string="x", end_string="y", remove_char="z"):
    with open(file_name, 'r') as file:
        lines = file.readlines()

    start_line_found = False

    # Iterate through the lines and modify them as needed
    for i, line in enumerate(lines):
        if start_string in line:
            start_line_found = True
        
        if start_line_found and line.startswith(remove_char):
            lines[i] = line[2:] # Remove the first character if it's the specified remove_char
        
        if start_line_found and end_string in line:
            start_line_found = False

    # Write the modified lines back to the file
    with open(file_name, 'w') as file:
        file.writelines(lines)


def main():
    file_name = sys.argv[1]
    start_string="// framework lint_off" 
    end_string="// framework lint_on" 
    add_char="//"
    if ("lint_off" in sys.argv[2]):
        lint_off(file_name, start_string, end_string, add_char)
    else:
        lint_on(file_name, start_string, end_string, add_char)

if __name__ == "__main__":
    main()

  
