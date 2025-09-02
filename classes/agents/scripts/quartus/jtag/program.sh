

QUARTUS_BIN=$QUARTUS_ROOTDIR/bin
cd ./quartus/jtag
$QUARTUS_BIN/jtagconfig --setparam $1 JtagClock 6M
$QUARTUS_BIN/quartus_pgm  -c $1 DE10_Agilex_FLASH_Program.cdf 
cd ../../
