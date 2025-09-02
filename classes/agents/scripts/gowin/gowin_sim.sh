source ${frm_path}/${script_path}/functions/common.sh

RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
ENDCOLOR="\e[0m"


prj_path="./prj/"
firmware_path="./firmware"
firmware_hex_path=$firmware_path/code/
gw_tcl_script=${frm_path}/${script_path}/gowin/gowin_sim.tcl
simlib=./simlib
simlib_tcl=$simlib/mentor

export comp_opt=$comp_opt
export simlib_tcl=$simlib_tcl
echo $simlib_tcl

read_file "$source_ips"
break_data "GOWIN:" ".v" "${file_paths[@]}"

for each_ip in ${ips_paths[@]}; do
    export comp_opt=$comp_opt" ip"
    echo -e ${GREEN}INFO: Checking $each_ip${ENDCOLOR}
done

vsim $run_opts -do $gw_tcl_script
rm -rf ./simlib

if [[ "on" == $coverage ]]; then
    firefox ./reports/coverage/covSummary.html	    
fi
rm transcript

