###################################
#VARIABLES DECLARATION
###################################

set project_name $env(module_name)
set project_dir $env(prj_path)

###################################
#PROJECT FOLDER 
###################################

open_project $project_dir/${project_name}.gprj

###################################
#PROJECT PLACE AND ROUTE 
###################################
#source $project_name.tcl
set_option -clock_route_order 0
set_option -place_option 0
set_option -route_option 0
set_option -gen_text_timing_rpt 1
set_option -gen_verilog_sim_netlist 1
set_option -show_all_warn 1
set_option -timing_driven 1
#set_option -route_maxfan 23
set_option -timing_driven 1
set_option -replicate_resources 0
set_option -correct_hold_violation 1
set_option -show_init_in_vo 0
set_option -ireg_in_iob 1
set_option -oreg_in_iob 1
set_option -ioreg_in_iob 1
set_option -looplimit 2000
 
set_option -seu_handler 0
set_option -seu_handler_checksum 0
set_option -seu_handler_mode auto
set_option -stop_seu_handler false
set_option -error_detection false
set_option -error_detection_correction false
set_option -error_injection false
set_option -ext_cclk false
#set_option -ext_cclk_div 1
set_option -disable_io_insertion 0

run pnr

###################################
#SAVE AND CLOSE FILES
###################################

# Save the project
saveto $project_name.tcl
saveto $project_name

# Close the project
run close
set folders [glob -nocomplain -directory . $env(module_name)*]
puts $folders
foreach folder $folders {
    file delete -force -- $folder
}

exit

