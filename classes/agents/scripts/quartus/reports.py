import argparse
import os
import subprocess
import sys  
import re  
import matplotlib.pyplot as plt    

def read_env_variable(variable_name):
    value = os.environ.get(variable_name)
    if value is None:
        print(f"Environment variable {variable_name} is not set.")
        return 0
    else:
        return value

def return_file(input_file):
    try:
        with open(input_file, 'r') as infile:
            lines = infile.readlines()
    except FileNotFoundError:
        print("Error: File not found.")
        exit()
    return lines  

def save_file(content, output_file):
    with open(output_file, 'w') as outfile:
        outfile.writelines(content)


def generate_report(input_file, output_file, target_text, ignore_string=None):  
    found_partition = False
    report_lines = []
    lines = return_file(input_file)
    for line in lines:
        if found_partition:
            if line.startswith('+') or line.startswith(';'):
                if ignore_string and ignore_string in line:
                    continue
                report_lines.append(line)
            else:
                break
        elif target_text in line:
            found_partition = True
            report_lines.append(line)

    if not found_partition:
        print("Error: Specified text not found in the file.")
        return 0
    save_file(report_lines, output_file)

###############VISUALIZATION

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False    

def parse_and_create_tree(lines):
    tree = []
    for line in lines:
        if not line.startswith(';'):
            continue  # Ignore lines not starting with ';'
        parts = line.strip().split(';')
        whitespace_count = len(parts[1]) - len(parts[1].lstrip())
        level = whitespace_count // 3
        parts = [part.strip() for part in parts[1:]]  # Remove extra white spaces
        parts.insert(0, level)  # Insert the level index
        cleaned_string = re.sub(r'\(.*?\)', '', parts[2]).strip()
        if is_number(cleaned_string): 
            parts[2] = float(cleaned_string) if cleaned_string else 0.0
        tree.append(parts)
    return tree

def sort_level(tree, level):
    return sorted([item for item in tree if item[0] == level], key=lambda x: x[1])

def print_level(sorted_level):
    for item in sorted_level:
        print(f"Level: {item[0]}, Items: {item[1]}, value: {item[2]}")

def plot_pie_chart(tree, level):
    # Extract values for the specified level
    values = [item[2] for item in tree if item[0] == level]
    labels = [item[1] for item in tree if item[0] == level]

    # Check if there are any values to plot
    if not values:
        print(f"No data found for level {level}")
        return

    # Plot the pie chart
    wedges, texts = plt.pie(values, startangle=140, labels=['']*len(labels))
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Create legend with ALM values
    legend_labels = [f"{label} ({value} ALM)" for label, value in zip(labels, values)]
    plt.legend(wedges, legend_labels, title="Items", loc="center left", bbox_to_anchor=(0.8, 0, 0.5, 1))

    plt.title(f'Proportion of Items at Level {level}')
    plt.show()

###############DICT

def create_dict_syn(target_file):
    target_text = {}
    target_text["syn_summary"]      = "; Partition \"root_partition\" Resource Utilization by Entity"
    target_text["fsm"]          = "; State Machine - Summary"
    target_text["register"]     = "; General Register Statistics for Partition \"root_partition\" "
    target_text["mux"]          = "; Multiplexer Restructuring Statistics (Restructuring Performed)"
    target_text["megafunction"] = "; Registers Packed Into Inferred Megafunctions"
    target_text["syn_netlist"]  = "; Post-Synthesis Netlist Statistics for Partition \"root_partition\" "
    target_text["resources"]    = "; Synthesis Resource Usage Summary for Partition \"root_partition\" "
    target_text["ram"]          = "; Synthesis RAM Summary for Partition \"root_partition\" "
    target_text["warnings"]     = f";  Warnings for ../rtl/{target_file}.sv  "
    return target_text

def create_dict_fit(target_file):
    target_text = {}
    target_text["summary"]      = "; Fitter Summary "
    target_text["settings"]     = "; Fitter Settings"
    target_text["netlist"]      = "; Fitter Netlist Optimizations"
    target_text["bank"]         = "; I/O Bank Usage"
    target_text["io_warning"]   = "; I/O Assignment Warnings"
    target_text["controll"]     = "; Control Signals"
    target_text["statistics"]   = "; Fitter Partition Statistics"
    target_text["usage"]        = "; Fitter Resource Usage Summary"
    target_text["utilization"]  = "; Fitter Resource Utilization by Entity"
    return target_text

def create_dict_sta(target_file):
    target_text = {}
    target_text["path"]         = "; SDC File Path "
    target_text["clocks"]       = "; Clocks"
    target_text["time"]         = "; Timing Closure Summary"
    target_text["frequency"]    = "; Fmax Summary"
    target_text["setup"]        = "; Setup Summary"
    target_text["hold"]         = "; Hold Summary "
    target_text["signoff"]      = "; Design Assistant (Signoff) Results "
    target_text["ignored"]      = "; Ignored Constraint"
    target_text["empty"]        = "; Empty Collection Filter ; SDC Command"
    return target_text

def main():
    report = sys.argv[1]
    target_file = sys.argv[2]
    gui = sys.argv[3]
    ignore = sys.argv[4] if (sys.argv[4] != "") else None
    level = int(sys.argv[5]) if int(sys.argv[5]) > 0 else 1 
    outfile = "delete.me"
    
    target_dict_syn = create_dict_syn(target_file)
    target_dict_fit = create_dict_fit(target_file)
    target_dict_sta = create_dict_sta(target_file)
    report_folder = "" if not os.path.isdir(f'{read_env_variable("prj_path")}/output_files') else "output_files/"
    if (sys.argv[1] in target_dict_syn):
        target_text = target_dict_syn[report]
        infile = f'{read_env_variable("prj_path")}/{report_folder}{target_file}.syn.rpt'

    elif (sys.argv[1] in target_dict_fit):
        target_text = target_dict_fit[report]    
        infile = f'{read_env_variable("prj_path")}/{report_folder}{target_file}.fit.rpt'
    else:
        target_text = target_dict_sta[report]    
        infile = f'{read_env_variable("prj_path")}/{report_folder}{target_file}.sta.rpt'
        
    generate_report(infile, outfile, target_text, ignore);
    if ("on" in gui):
        process = subprocess.Popen(['gedit', outfile])
        if ("utilization" in sys.argv[1]):
            lines = return_file(outfile)
            tree = parse_and_create_tree(lines)
            plot_pie_chart(tree,level)
        process.wait()
    else:
        subprocess.call(["cat", outfile])
        
    os.remove(outfile)

if __name__ == "__main__":
    main()
