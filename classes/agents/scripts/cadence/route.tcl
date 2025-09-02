###################################
#VARIABLES DECLARATION
###################################
set frm_path $::env(frm_path)
set script_path $::env(script_path)

set source_path "${frm_path}/${script_path}/functions/source.tcl"
source $source_path

# Set project variables
set project_name $env(module_name)
set project_tbname $env(tb)
set project_dir $env(prj_path)/$project_name

# Set Synthesis constraints
set netlist_list [listFromFile ./manifests/manifest_netlist.f]
set sdc_file $env(source_sdc)
set def_file $env(cadence_def)
set lef_file $env(cadence_lef)
set lib_file $env(cadence_lib)
set LP_syn $env(cadence_lp_syn)

###################################
# MESSAGE
###################################

message INFO "User shall provide .v netlist and .sdc"
message INFO "User shall provide .gds layer map file"
message INFO "User shall provide .lib tech file"
message INFO "User shall provide .lef cell abstraction file"
message WARNING "User may provide floorplan .fp/def"
message WARNING "User may provide scandef .scandef file"
message WARNING "User may provide io plan file"
message WARNING "User may qrc(parasitic RC), captables(capacitance) or cpf (power intent)"


###################################
#INIT DESIGN   
###################################


if {[llength $netlist_list]} {
    message WARNING "→ Loading netlist"
    message NO_COLOR ""
    foreach netlist_module $netlist_list {	;
        if { [isNotComment $netlist_module] } {
            message INFO "loading $netlist_module ext modules"
            message NO_COLOR ""
            set_db init_read_netlist_files $netlist_module
            read_netlist $netlist_module
        }
    }
}

set_db init_lef_files $lef_file
read_physical -lef $lef_file

###################################
#INIT DESIGN
###################################

set_db init_ground_nets VSS
set_db init_power_nets VCC
init_design

###################################
#CREATE PROJECT    
###################################

if {[file exists "$project_name.place.db"]} {
    read_db $project_name.place.db
} else {
    write_db $project_name.place.db
}


###################################
#CREATE FLOORPLAN    
###################################

create_floorplan

###################################
#GUI    
###################################
if { $env(gui) == "on" }{
    gui_show
}