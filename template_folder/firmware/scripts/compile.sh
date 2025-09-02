firmware_name="${firmware_name:-firmware}"
target_path="../code/"
pwd
nios2-app-generate-makefile --bsp-dir $target_path/${firmware_name}_bsp --app-dir $target_path/ --src-dir $target_path/${firmware_name}
cd $target_path
make all
make mem_init_generate
mv 	./mem_init/firmware.hex .
rm -rf ./mem_init/ ./obj hello_world.elf hello_world.objdump hello_world.map Makefile
