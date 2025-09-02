#!/bin/bash
source ${frm_path}/${script_path}/functions/common.sh

PRJ_PATH=$1
report_file=$module_name.sta.rpt
sdc_rel_path=../$prj_constraint/$module_name.sdc

###################################
#RUN CMD
###################################

quartus_sta $quartus_sta_opt $PRJ_PATH --sdc $sdc_rel_path

###################################
#LOG
###################################

if [[ $log == "on" ]]; then
    cp $prj_path/$report_file $reports_path/
    echo -e "${GREEN}INFO:Displaying compilation ${LIGHT_BLUE}WARNING\n"
    grep "^Warning" $reports_path/$report_file
    echo -e "${GREEN}INFO:Displaying compilation ${YELLOW}CRITICAL WARNING\n"
    grep "^Critical Warning" $reports_path/$report_file
    echo -e "${GREEN}INFO:Displaying compilation ${RED}ERRORS\n"
    grep "^Error" $reports_path/$report_file
    echo -e ${ENDCOLOR}
fi

###################################
#GUI
###################################

if [[ $gui == "on" ]]; then
    quartus $prj_path/$module_name.qpf
fi