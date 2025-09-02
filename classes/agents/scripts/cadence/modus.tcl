###################################
#VARIABLES DECLARATION
###################################
set frm_path $::env(frm_path)
set script_path $::env(script_path)

# Set manifest lists
set rtl_list [listFromFile ./manifests/manifest_rtl.f]
set tb_list [listFromFile ./manifests/manifest_tb.f]
set ip_list [listFromFile ./manifests/manifest_ip.f]
set ext_module_list [listFromFile ./manifests/manifest_ext_ip.f]

# Set project variables
set project_name $env(module_name)
set project_tbname $env(tb)
set project_dir $env(prj_path)/$project_name

# Set Synthesis constraints
set sdc_file $env(source_sdc)
set def_file $env(cadence_def)
set lef_file $env(cadence_lef)
set lib_file $env(cadence_lib)
set LP_syn $env(cadence_lp_syn)

set modus_work_dir "modus"/$project_dir/
set modus_test_mode "FULLSCAN"
set modus_assign_file $project_name.$modus_test_mode.pinassign

set faultmodel_en "off"
set atpg_en "off"
set scan_test_en "off"
set logic_test_en "off"


###################################
# BUILD
###################################
#-designsource $netlist_list can be a list of netlist or verilog. if separated by : rather then " " then they are compiled together (good for defines)
#-designsource if a .files file is inputed, it works like a .f a manifest
#-macros can be defined as -definemacro <macro> <macro>
#-cell is the name of the top module
build_model -workdir $modus_work_dir -cell $project_name -designsource $netlist_list -techlib $lib_file -designtop $project_name

#need to create a pin assignment file from .pin, need pin name, func, and polarity
build_testmode -workdir $modus_work_dir -testmode $modus_test_mode -assignfile $modus_assign_file

###################################
# VERIFY
###################################

verify_test_structures -workdir $modus_work_dir -testmode $modus_test_mode
report_test_structures -workdir $modus_work_dir -testmode $modus_test_mode

###################################
# FAULT MODEL FLOW
###################################

if {$faultmodel_en == "on"} {
    build_faultmodel -workdir $modus_work_dir -fullfault yes
    read_sdc -sdc $sdc_file -testmode $modus_test_mode
}

###################################
# SCAN MODEL FLOW
###################################

#create_sequential_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment scan
#create_bidge_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment scan
#create_iddq_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment scan


if {$scan_test_en == "on"} {
    create_scanchain_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment scan
}

###################################
# LOGIC MODEL FLOW
###################################
if { $atpg_en == "on"} {
    create_logic_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment logic -effort high
    commit_tests -testmode $modus_test_mode -inexperiment logic
    write_vectors -testmode $modus_test_mode -language wgl
    write_vectors -testmode $modus_test_mode -language verilog -testrange 1:100

}
#if {$scan_test_en == "on"} {
    #logic_test_en -workdir $modus_work_dir -testmode $modus_test_mode -experiment logic -effort high
    #create_logic_tests -workdir $modus_work_dir -testmode $modus_test_mode -experiment logic -effort high
#}
###################################
# REPORT 
###################################
if {$scan_test_en == "on"} {
    report_chain -summary
}
reports_fault -testmode $modus_test_mode
report_model_statistics -workdir $modus_work_dir

###################################
# OUTPUT
###################################

write_vectors -workdir $modus_work_dir -testmode $modus_test_mode -inexperiment logic -language verilog -scanformat serial -outputfilename $project_name.modus_test.result

if {$env(gui) == "on"}{
    gui_open
}

exit