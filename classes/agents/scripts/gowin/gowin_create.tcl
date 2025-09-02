###################################
#VARIABLES DECLARATION
###################################
set frm_path $::env(frm_path)
set script_path $::env(script_path)
set cwd [pwd]

set source_path "${frm_path}/${script_path}/functions/source.tcl"
source $source_path

set rtl_list [listFromFile ./manifests/manifest_rtl.f]
set tb_list [listFromFile ./manifests/manifest_tb.f]
set ip_list [listFromFile ./manifests/manifest_ip.f]
set ext_module_list [listFromFile ./manifests/manifest_ext_ip.f]
set path_list [listFromFile ./manifests/manifest_inc.f]
set cst_list  $env(gowin_cst)
set gvio_list $env(gowin_gvio) 
set gpa_list $env(gowin_gpa)
set gao_list $env(gowin_gao)
set gsc_list $env(gowin_gsc)

# Set project variables
set project_name $env(module_name)
set project_dir $env(prj_path)
set project_device $env(gowin_device)
set project_sdc $env(gowin_sdc)

#define parse
set index 0
set user_defines [string range $env(synth_def) 1 end]
set define_list [split $user_defines "+"]


###################################
#PROJECT FOLDER STRUCTURE
###################################

create_project -name $project_name -dir $project_dir -pn $project_device -device_version NA
file copy -force $cwd/$project_dir/$project_name/$project_name.gprj $cwd/$project_dir/.
cd ../
file delete -force $cwd/$project_dir/$project_name

set_option -top_module $project_name
set_option -verilog_std sysv2017

###################################
#PROJECT ADD DEFINES
###################################

#Define the list
 #Iterate through the list
foreach item $define_list {
    if {$index % 2 != 0} {
        set key_list [split $item "="]
        set key [lindex $key_list 0]
        set value [lindex $key_list 1]
        message INFO "adding define  $key $value"
        set_option -$key $value    
    }
    incr index
}

###################################
#PROJECT ADD PATH
###################################

if {[llength $path_list]} {
    foreach inc_path $path_list {	;
        if { [isNotComment $inc_path] } {
            message INFO "loading $inc_path\t"
            set_option -include_path ../$inc_path
        }
    }
}

###################################
#PROJECT ADD IP FILES
###################################

if {[llength $ip_list]} {
    foreach ip_module $ip_list {	;
        if { [isNotComment $ip_module] } {
            message INFO "loading $ip_module\t"        
            set gowin_ip [removeSubstring $ip_module "GOWIN"] 
            puts "$ip_module"
            if {$gowin_ip != ""} { 
                add_file ../$gowin_ip
            }
        }
    }
}


###################################
#PROJECT ADD RTL AND FILES
###################################

if {[llength $rtl_list]} {
    foreach rtl_module $rtl_list {	;
        if { [isNotComment $rtl_module] } {
            message INFO "loading $rtl_module\t"
            add_file ../$rtl_module
        }
    }
}

###################################
#PROJECT ADD EXT MODULE FILES
###################################

if {[llength $ext_module_list]} {
    foreach ext_module $ext_module_list {	;
        if { [isNotComment $ext_module] } {
            message INFO "loading $ext_module\t"
            add_file  ../$ext_module
        }
    }
}

 
###################################
#PROJECT ADD CONSTRAINTS
###################################

if {[file exists ../$project_sdc]} {
    puts "sdc $project_sdc"
    message INFO "loading $project_sdc\t"
    add_file -type sdc ../$project_sdc
        }
    

if {[file exists ../$cst_list]} {
    message INFO "loading $cst_list\t"
    add_file -type cst ../$cst_list
        }

if {[file exists ../$gvio_list]} {
    message INFO "loading $gvio_list\t"
    add_file -type gvio ../$gvio_list
        }

if {[file exists ../$gpa_list]} {
    message INFO "loading $gpa_list\t"
    add_file -type gpa ../$gpa_list
        }

if {[file exists ../$gao_list]} {
    message INFO "loading $gao_list\t"
    add_file -type gao ../$gao_list
        }

if {[file exists ../$gsc_list]} {
    message INFO "loading $gsc_list\t"
    add_file -type gsc ../$gsc_list
        }

###################################
#PROJECT PIN FILES
###################################

if {[file exists ../$cst_list]} {
    message WARNING "using existing cst file"
} else {
    set pin_list [parseFile ../$env(source_pins)]
	set cst_file [open ../$cst_list w]
	if {[llength $pin_list]} {
	    foreach pin_description $pin_list {	;
            set pin_name [lindex $pin_description 0]  
            set pin_standard [lindex $pin_description 1]
            set pin_location [lindex $pin_description 2]
            set pin_direction [lindex $pin_description 3]
            set pin_vendor [lindex $pin_description 4]
            set pin_vendor [string tolower $pin_vendor]
            if {$pin_vendor == "gowin"} {
                puts $cst_file "IO_LOC $pin_name $pin_location;"
                puts $cst_file "IO_PORT $pin_name IO_TYPE=$pin_standard;"
            }
            
        }
    }
    close $cst_file
    add_file ../$cst_list

} 


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

