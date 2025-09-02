###################################
#VARIABLES DECLARATION
###################################

set project_name $env(module_name)
set project_dir $env(prj_path)

###################################
#PROJECT FOLDER 
###################################

open_project $project_dir/${project_name}.gprj
open_run impl_1

###################################
#PROJECT SYNTH
###################################
set_option -bit_format bin
set_option -power_on_reset_monitor 1
set_option -bit_crc_check 1
set_option -bit_compress 0
set_option -bit_encrypt 0
set_option -bit_encrypt_key 00000000000000000000000000000000
set_option -bit_security 1
set_option -bit_incl_bsram_init 1
set_option -bg_programming off
#set_option -hotboot 1
#set_option -i2c_slave_addr 00
#set_option -secure_mode 0
#set_option -loading_rate default
#set_option -program_done_bypass 0
#set_option -wakeup_mode 0
#set_option -user_code default
#set_option -unused_pin default
#set_option -multi_boot 0
#set_option -multiboot_address_width 24
#set_option -multiboot_mode normal
## set_option -multiboot_spi_flash_address 00000000
#set_option -mspi_jump 0
#set_option -turn_off_bg 0


write_bitstream -force bitstream.bit

###################################
#SAVE AND CLOSE FILES
###################################

# Save the project
save_project $project_name

# Close the project
close_project
set folders [glob -nocomplain -directory . $env(module_name)*]
puts $folders
foreach folder $folders {
    file delete -force -- $folder
}

exit

