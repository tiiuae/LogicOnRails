onerror {resume}
quietly WaveActivateNextPane {} 0
add wave -noupdate /sum_tb/dut/sw/i_clk
add wave -noupdate /sum_tb/dut/sw/i_rst_n
add wave -noupdate /sum_tb/dut/sw/i_data
add wave -noupdate /sum_tb/dut/sw/o_data
add wave -noupdate /sum_tb/dut/sw/r_data
add wave -noupdate /sum_tb/dut/i_clk
add wave -noupdate /sum_tb/dut/i_rst_n
add wave -noupdate /sum_tb/dut/i_sw
add wave -noupdate /sum_tb/dut/o_led
add wave -noupdate /sum_tb/dut/r_sync
add wave -noupdate /sum_tb/dut/w_data
TreeUpdate [SetDefaultTree]
WaveRestoreCursors {{Cursor 1} {0 ps} 0}
quietly wave cursor active 0
configure wave -namecolwidth 150
configure wave -valuecolwidth 100
configure wave -justifyvalue left
configure wave -signalnamewidth 0
configure wave -snapdistance 10
configure wave -datasetprefix 0
configure wave -rowmargin 4
configure wave -childrowmargin 2
configure wave -gridoffset 0
configure wave -gridperiod 1
configure wave -griddelta 40
configure wave -timeline 0
configure wave -timelineunits ps
update
WaveRestoreZoom {0 ps} {7628 ps}
