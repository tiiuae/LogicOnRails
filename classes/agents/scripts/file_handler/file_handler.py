
# =============================================================================
# Project:        Logic on Rails
# File:           file_handler
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    Generate Files 
# =============================================================================

import shutil
import os

def copy_file(source_path, destination_path, ignore_list):
    YELLOW = "\033[93m"
    GREEN = "\033[92m"
    RESET = "\033[0m"    

    if not os.path.isfile(source_path):
        raise FileNotFoundError(f"Source file not found: {source_path}")
    
    dest_dir = os.path.dirname(destination_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    if ("n" in ignore_list):
        removed_substring = destination_path.rsplit('_eg', 1)
        destination_path = ''.join(removed_substring)        
    
    if os.path.isfile(destination_path):
        print(f"{YELLOW}File already exists{RESET}")
    else:
        shutil.copy2(source_path, destination_path)
        print(f"{GREEN}SystemVerilog File created{RESET}")


def main():
    frm_path = os.getenv('frm_path')
    script_path = os.getenv('script_path')
    module_name = os.getenv('module_name')
    ignore_list = os.getenv('ignore')
    
    src_file = f"{frm_path}/{script_path}/file_handler/module_eg.sv"
    dst_file = os.path.join(os.getcwd(), f"{module_name}_eg.sv")
    copy_file(src_file, dst_file, ignore_list)
    
if __name__ == "__main__":
    main()
