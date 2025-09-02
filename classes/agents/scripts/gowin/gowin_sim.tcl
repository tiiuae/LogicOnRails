#file delete work
#file std_cell_lib

###################################
#FUNCTIONS
###################################
set frm_path $::env(frm_path)
set script_path $::env(script_path)
set GW_INSTALL_PATH $::env(GW_PATH)
set simlib $GW_INSTALL_PATH/IDE/simlib/gw1n/prim_sim.v
set source_path "${frm_path}/${script_path}/functions/source.tcl"

source $source_path

message ERROR "READY?"
message WARNING "SET"
message INFO "GO!"

###################################
#VARIABLES
###################################

#parse manifest files into list
set rtl_list [listFromFile $env(source_rtl)]
set inc_list [listFromFile $env(source_inc)]
set tb_list [listFromFile $env(source_tb)]
set ip_list [listFromFile ./manifests/manifest_ip.f]
set soft_list [listFromFile $env(source_soft)]
set netlist_list [listFromFile $env(source_netlist)]
set ext_lib_list [listFromFile $env(source_lib)]
set ext_ip_list [listFromFile $env(source_ext)]

message WARNING $env(comp_opt)

###################################
#NEW LIB
###################################
vlib work

##########################################################
# Compile the GOWIN Standard Cells to Library work
##########################################################
vlog -incr -work work "$simlib"

###################################
##UVM OPT
###################################

#UVM_PATH is an env variable and is not set in make file
if {$env(UVM_PATH) ne ""} {
    set uvm_inc_path +incdir+$env(UVM_PATH)
} else {
    set uvm_inc_path ""
}
set def_test "+define+DEFAULT_TEST=\"$env(default_test)\""

###################################
#COVERAGE OPT
###################################

#create libraries and define commands for coverage reports
switch -regexp -- $env(coverage) {
    "on" {
        set cov_comp_opt "-coveropt 3 +cover"
        set cov_sim_opt "-coverage -c -do \"coverage save -onexit -directive -codeAll $env(reports_dir)/$env(tb).ucdb\" "
    }
    default {
        set cov_comp_opt ""
        set cov_sim_opt ""
    }
}  

###################################
#EXT LIBS
###################################

if {$env(ext_modules) == "on" } {
    if {[llength $ext_lib_list]} {
        message INFO "INFO EXT : looking for external libraries to load from ext_lib manifest file" 
        set ext_libs "" 
        foreach ext_lib $ext_lib_list {	;
            if { [isNotComment $ext_lib] } {
                set gowin_ip [removeSubstring $ext_lib "GOWIN"]
                if {$gowin_ip != ""} {
                    set ext_libs_path $questa_ip
                    append ext_libs " -L $ext_libs_path"
                    message INFO "INFO EXT : added lib"
                }
            }             
        }
    } else {
        message WARNING "WARNING LIB-EMPTY : ext_modules is ON but there is no file to load in the ext_lib manifest" 
        set ext_libs ""    
    }
    if {[llength $ext_ip_list]} {
        message INFO "INFO EXT : generating libraries for .vp files"
        set processed_paths ""
        foreach ip_path $ext_ip_list {
            if { [isNotComment $ip_path] } {
                lappend processed_paths $ip_path
            }
        }
        message INFO "PATHS $processed_paths"
        if {[string length $processed_paths] != 0} {
            set unique_paths [getUnique $processed_paths]
            foreach unique_path $unique_paths {
                message INFO "INFO EXT : generating lib $unique_path"
                #set files [glob -dir $unique_path *.*]
                vlog -sv -work work $unique_path* 
            }        
        } else {
            message WARNING "WARNING EXT-EMPTY : ext_modules is ON but there is no file to load in the ext_ip manifest" 
        }
    }
} else {
    set ext_libs ""
}

###################################
#COMPILATION
###################################

#compile
switch -regexp -- $env(comp_opt) {
    "netlist" {
        set tb_modules ""
        foreach netlist_module $netlist_list {	;
            if { [isNotComment $netlist_module] } {
                if { [endsWith $netlist_module "vhd"] } {
                    message INFO "COMPILING $netlist_module"
                    vcom $netlist_module
                } else {
                    message INFO "COMPILING $netlist_module"
                    vlog -sv -work work $netlist_module
                }
                
            }
        }
        vlog -sv -work work ../prj/simulation/questa/$env(module_name).vo
        foreach tb_module $tb_list {	;
            if { [isNotComment $tb_module] } {
                append tb_modules " $tb_module"
            }
        }    
        set cmd "vlog $env(synth_def) $env(sim_def) $cov_comp_opt -sv -timescale 1ns/1ps -work work $tb_modules"
        eval $cmd            
    }
    "ip" { 
        set rtl_modules ""
        set inc_modules ""
        set tb_modules ""
        set ip_module ""

        foreach rtl_module $rtl_list {	;
            if { [isNotComment $rtl_module] } {
                if {[string match "*gowin.vp" $rtl_module]} {
                    set rtl_module [regsub "gowin.vp$" $rtl_module "sim.v"]
                    puts "Renamed file: $rtl_module"
                }
                append rtl_modules " $rtl_module"
            }
        }
        if { [isListEmpty $inc_list] == 0 } {
            foreach inc_module $inc_list {	;
                if { [isNotComment $inc_module] } {
                    append inc_modules " +incdir+$inc_module"
                }
            }
        }
        foreach tb_module $tb_list {	;
            if { [isNotComment $tb_module] } {
                message INFO $tb_module
                append tb_modules " $tb_module"
            }
        }
        if {[llength $ip_list]} {
            foreach gw_module $ip_list {	;
                if { [isNotComment $gw_module] } {
                    message INFO "$gw_module"        
                    set ip_module [removeSubstring $gw_module "GOWIN"] 
                    if {$ip_module != ""} {
                        append ip_modules " $ip_module"
                    }
                }
            }
        }
        set cmd "vlog $def_test $env(synth_def) $env(sim_def) $cov_comp_opt -sv -timescale 1ns/1ps -sv  $ip_modules $rtl_modules -sv $inc_modules $uvm_inc_path $tb_modules"
        eval $cmd        
    }
    default {
        vlog  -timescale 1ns/1ps -sv -work work -incr +define+DEFAULT_TEST=\"$env(default_test)\" $env(user_def) $env(sim_def) -F $env(source_rtl) -F $env(source_tb)  $uvm_inc_path
    }
}

if {$env(dpi_opt) ne ""} {
    if {[llength $soft_list]} {
        message INFO "INFO DPI : looking for dpi functions to load from software manifest file"            
        set soft_func ""
        foreach soft_module $soft_list {
            if { [isNotComment $soft_module] } {
                set env_var [lindex [split $soft_module "/"] end]
                set patch_env_var [replaceChar $env_var "." "_"]
                set ::env($patch_env_var) "$soft_module.exe " 
                if {[string first ".h" $soft_module] >= 0} {
                    append soft_func " $env(dpi_opt) $soft_module"
                } else {
                    append soft_func " $soft_module"
                }
                message INFO "INFO DPI : added dpi function $soft_module"
            }
        }
        set cmd "vlog -sv -work work $soft_func"
        eval $cmd
    } else {
        message ERROR "ERROR DPI-EMPTY : dpi_opt is ON but there is no file to load in the software manifest"
    }
}

###################################
#SIMULATE
###################################
#define simulation commands for IP use case
set sim_cmd "vsim -suppress 14408 -suppress 16154 -t 1ps +test=$env(default_test) $ext_libs  $env(tb) $def_test +define+QUESTA $env(synth_def) $env(access_opt) $cov_sim_opt " 
set TOP_LEVEL_NAME $env(tb)
eval $sim_cmd
view structure
view signals   

###################################
#WAVE
###################################

switch -regexp -- $env(run_opts) {
    "-gui"   { 
        log -r /* ; 
        do $env(wave);
        run -all
    }
    "-c"     {  
        run -all;
        switch -regexp -- $env(coverage) {
            "on" {  
                puts $env(reports_dir)/coverage
                coverage report -html -output $env(reports_dir)/coverage -annotate -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90
                coverage report -output $env(reports_dir)/coverage.txt -annotate -details -assert -directive -cvg -code bcefst
            }
        }
        exit 
    }
    default {
        if { [regexp {^-} $env(run_opts)] } {
            message ERROR "ERROR: Unknown vsim option '$env(questa_opts)' specified .\n"
            exit 
        }
    }
}


