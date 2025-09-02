ixclkgen -input clk.qel -output clk.sv

vlan //verilog file
vhan //vhdl file

vlan clk.sv //verify and comile gen clk

hdlice // synth tb and hdl


emulatorConfiguration -add {file Palladium.et3confg} {boards 0.0+0.1} //required the Palladium.et3confg file to match exatcly with hired rack before emulation starts

precompileOption -add ignoreEmptyCells
precompileOption -add ignoreMultiDrv

.////////////////////////////////
ice flow
compile
vavhdl -work lib2 file3.vhd file4.vhd
vavlog -work lib1 file1.v file2.v
vavlog -work lib1 -sv file1.sv file2.sv
vaelab $top
or
hdlImport (for vavhdl,vavlog), and hdlSynthesize (for vaelab).


linkRefLib $lib

refLib $lib1 $lib2

//provid top
design $top <CELL>

///////////////////////
running emulation

test_server