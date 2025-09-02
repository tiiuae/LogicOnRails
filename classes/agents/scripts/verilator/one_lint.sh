#!/bin/bash
source ${frm_path}/${script_path}/functions/common.sh

inc_tb=$1
prj_def=`echo $synth_def | sed 's/+define+/ +define+/g'`
sim_def=`echo $sim_def | sed 's/+define+/ +define+/g'` 
pass=0

# Call the function for both files
declare -a file_paths=()
read_file "$source_rtl"
read_file "$source_bb"
if [[ $inc_tb == "on" ]]; then
    read_file "$source_tb"
fi
rtl_paths=("${file_paths[@]}")

python3 ${frm_path}/${script_path}/verilator/one_lint.py ${rtl_paths[@]}
