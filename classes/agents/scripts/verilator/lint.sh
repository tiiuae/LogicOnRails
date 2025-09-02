#!/bin/bash
source ${frm_path}/${script_path}/functions/common.sh

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
ENDCOLOR="\e[0m"


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
#skip vhdl files for verilor linting
filtered_paths=()

for path in "${rtl_paths[@]}"; do
    if [[ "$path" != *".vhd"* ]]; then
        filtered_paths+=("$path")
    fi
done
rtl_paths=("${filtered_paths[@]}")

#remove lint_off
for each_file in ${file_paths[@]}; do
    python3 ${frm_path}/${script_path}/verilator/lint_off.py $each_file lint_off
done

declare -a file_paths=()
read_file "$source_inc"

for each_file in ${file_paths[@]}; do
    inc_paths=$inc_paths" +incdir+$each_file"
done
if [[ $uvm == "on" ]]; then
    inc_paths=$inc_paths" +incdir+$UVM_MACRO_PATH"
fi

if [[ $log == "on" ]]; then
    echo "verilator $inc_paths --timing --error-limit 20 $prj_def $sim_def --lint-only ${verilator_warn_options} ${rtl_paths[@]} --top-module ${module_name}" > ./verilator/verilator.log
fi
verilator $inc_paths --timing --error-limit 20 $prj_def $sim_def --lint-only "${verilator_warn_options[@]}" "${rtl_paths[@]}" --top-module "${module_name}" 2>&1 | while IFS= read -r line; do
    if [[ "$line" =~ ^%Error ]]; then
        echo -e "${RED}${line}${ENDCOLOR}"
    elif [[ "$line" =~ ^%Warning ]]; then
        echo -e "${YELLOW}${line}${ENDCOLOR}"
    elif [[ "$line" =~ "V e r i l a t i o n" ]]; then
        echo -e "${GREEN}${line}"
    else
        echo "$line"
    fi
done

exit_status=$?

for each_file in ${rtl_paths[@]}; do
    python3 ${frm_path}/${script_path}/verilator/lint_off.py $each_file lint_on
done

exit $exit_status

