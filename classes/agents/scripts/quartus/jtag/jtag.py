import argparse
import subprocess
import re
import os
import shutil

def change_template(source_file, destination_file):
    try:
        shutil.copy(source_file, destination_file)
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
    except Exception as e:
        print(f"An error occurred while copying and renaming the file: {e}")

def replace_in_file(file_path, curr_dir, replace_str):
    with open(file_path, 'r') as file:
        content = file.read()
    modified_content = content.replace(replace_str, f"{curr_dir}/{replace_str}")
    with open(file_path, 'w') as file:
        file.write(modified_content)

def list_jtag(args):
    result = subprocess.run(["jtagconfig", "--enum"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = result.stdout
    if (output == ""):
        print ("no altera jtag device found")

    else:
        blocks = re.split(r'\n\s*\n', output.strip())
        return blocks

def parse_file():
    parser = argparse.ArgumentParser(description='Process some options.')
    parser.add_argument('-l', default=""          , help='log, fetches data from jtag device ')
    parser.add_argument('-a', default=""          , help='assign, use an usb id to set config scripts ')
    parser.add_argument('-b', default=""          , help='action, c : configure - f : flashes ')
    parser.add_argument('-p', default=""          , help='path, sof file ')
    parser.add_argument('-c', default=""          , help='current, current directory ')
    args = parser.parse_args()
    return args
 
def config_files(args, template_file, target_file, usr_file, factory_file):
    subprocess.call(["/bin/bash", "./quartus/jtag/flash.sh", f"{args.c}", f"{args.p}"])
    change_template(template_file, target_file)
    replace_in_file(target_file, args.c, usr_file)
    replace_in_file(target_file, args.c, factory_file)
    subprocess.call(["/bin/bash", "./quartus/jtag/convert.sh"])  
    shutil.move('./quartus/jtag/DE10_agilex_flash.pof', args.c)
    os.remove(target_file)

def program_files(args, template_file, target_file, replace_str):
    change_template(template_file, target_file)
    replace_in_file(target_file, args.c, replace_str)
    subprocess.call(["/bin/bash", "./quartus/jtag/program.sh", args.a])  
    os.remove(target_file)
    
def main():

    template_file_cnfg = "./quartus/jtag/DE10_AG_Config_Template.pfg"
    target_file_cnfg = "./quartus/jtag/DE10_AG_Config.pfg"
    template_file_prgm = "./quartus/jtag/DE10_Agilex_FLASH_Program_Template.cdf"
    target_file_prgm = "./quartus/jtag/DE10_Agilex_FLASH_Program.cdf"    
    usr_file = "User_HW.sof"
    factory_file = "Factory_HW.sof"
    pof_file = "DE10_agilex_flash.pof"

    args = parse_file()
    jtag_chain = list_jtag(args)
    
    if (args.l == "on"):
        try:
            for each_chain in jtag_chain:
                print(each_chain)
        except:
            exit()
    if ("c" in args.b):
        if not args.p == "" and not os.path.isdir(args.p):
            config_files(args, template_file_cnfg, target_file_cnfg, usr_file, factory_file)
        else:
            print("invalid sof path, use -p option to select sof file")
    if ("f" in args.b):
        if args.a.isdigit():
            program_files(args, template_file_prgm, target_file_prgm, pof_file)
        else:
            print("please assign a cable, use -a option")

    

if __name__ == "__main__":
    main()

