###################################
#VARIABLES DECLARATION
###################################
set frm_path $::env(frm_path)
set script_path $::env(script_path)

set source_path "${frm_path}/${script_path}/functions/source.tcl"
source $source_path

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

set mmmc_en "off"
set physical_aware "off"
set scan_chain_en "off"
set atpg_en "off"


###################################
# MESSAGE
###################################

message INFO "User shall receive .v netlist and .sdc"
message WARNING "User may receive logic equivalence file .lec, ATPG and ScanDef file"

####################################
##LOAD LIB
####################################

set lib_dir [file dirname $lib_file]; 
set lib_file [file tail $lib_file]

set_db init_lib_search_path $lib_dir
read_libs $lib_file;

if {$physical_aware == "on"} {
    read_physical -lef $lef_file
    set_db cap_table_file $cap_file
    set_db qrc_tech_file $qrc_file
}

if {$mmmc_en == "on"}{
    read_mmmc $mmmc_file
}

####################################
##SCAN CHAIN PRE
####################################
if {$scan_chain_en == "on"} {
    set_db dft_scan_style muxed_scan
    set_db dft_prefix dft_
    define_shift_enable -name SE -active high -create_port SE
    check_dft_rules
}


####################################
##SYNTHESIZE
####################################
message WARNING "→ Generic Synthesis"
syn_generic
write_hdl > ${project_name}_gen.v

message WARNING "→ Mapping"
syn_map
write_hdl > ${project_name}_map.v

message WARNING "→ Optimizing"
syn_opt
write_hdl > ${project_name}_opt.v

write_db ${project_name}.db

####################################
##SCAN CHAIN POS
####################################
if {$scan_chain_en == "on"} {
    check_dft_rules
    #line below may need correction to fit top level name
    set_db design:${project_name} .dft_min_number_of_scan_chains 1 
    define_scan_chain -name top_chain -sdi scan_in -sdo scan_out -create_ports
    connect_scan_chains -auto_create_chains
    syn_opt -incremental
    write_hdl > ${project_name}_opt_inc.v
    report_scan_chain
    write_scandef > ${project_name}.scandef
    if {$atpg_en == "on"} {
        write_dft_atpg -library $lib_file
    }
}

####################################
##SDC SDF EXPORT
####################################
check_timing_intent

message WARNING "→ Exporting synth SDC"

write_sdc > synth.sdc
write_sdf -timescale ns -nonegchecks -recrem split -edges check_edge -setuphold split > ${project_name}.sdf

####################################
##REPORTS
####################################

report_area > report_area.txt
report_hierarchy > report_hierarchy.txt
report_timing > report_timing.txt
report_summary > report_summary.txt

####################################
##CUSTOM COMMAND
####################################

set custom_cmd $env(cadence_synth_opt)
eval $custom_cmd

####################################
##GUI
####################################

if { $env(gui) == "on" }{
    gui_show
}

quit