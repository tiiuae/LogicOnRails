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
#PROJECT SYNTH
###################################
source $project_name.tcl
set_option -print_all_synthesis_warning 1
run syn

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
