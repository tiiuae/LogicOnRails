
# XM-Sim Command File
# TOOL:	xmsim(64)	21.03-s015
#
#
# You can restore this configuration with:
#
#      xrun -v200x -sysv_ext +.v -access +rwc -64bit -input restore.tcl -define SIMULATION -timescale 1ns/1ps -uvmhome /home/fathimath/cadence/installs/XCELIUM2103/tools/methodology/UVM/CDNS-1.1d -reflib ./xcelium/libraries_ip/altera_iopll_1931 -reflib ./xcelium/libraries_ip/altera_lnsim_ver -reflib ./xcelium/libraries_ip/altera_mf_ver -reflib ./xcelium/libraries_ip/altera_s10_user_rst_clkgate_1941 -reflib ./xcelium/libraries_ip/altera_ver -reflib ./xcelium/libraries_ip/async_fifo -reflib ./xcelium/libraries_ip/fifo_1920 -reflib ./xcelium/libraries_ip/lpm_ver -reflib ./xcelium/libraries_ip/memory -reflib ./xcelium/libraries_ip/pcie_ed_resetIP -reflib ./xcelium/libraries_ip/pll_i500_o100 -reflib ./xcelium/libraries_ip/ram_2port_2021 -reflib ./xcelium/libraries_ip/sgate_ver -reflib ./xcelium/libraries_ip/single_clock_fifo -reflib ./xcelium/libraries_ip/tennm_hssi_e0_ver -reflib ./xcelium/libraries_ip/tennm_hssi_p0_ver -reflib ./xcelium/libraries_ip/tennm_hssi_ver -reflib ./xcelium/libraries_ip/tennm_ver -reflib ../ips/tii_sim_lib/kyber_xcelium/rtllib/ -reflib ./xcelium/libraries_tb +UVM_VERBOSITY=UVM_LOW -top tb_top
#

set tcl_prompt1 {puts -nonewline "xcelium> "}
set tcl_prompt2 {puts -nonewline "> "}
set vlog_format %h
set vhdl_format %v
set real_precision 6
set display_unit auto
set time_unit module
set heap_garbage_size -200
set heap_garbage_time 0
set assert_report_level note
set assert_stop_level error
set autoscope yes
set assert_1164_warnings yes
set pack_assert_off {}
set severity_pack_assert_off {note warning}
set assert_output_stop_level failed
set tcl_debug_level 0
set relax_path_name 1
set vhdl_vcdmap XX01ZX01X
set intovf_severity_level ERROR
set probe_screen_format 0
set rangecnst_severity_level ERROR
set textio_severity_level ERROR
set vital_timing_checks_on 1
set vlog_code_show_force 0
set assert_count_attempts 1
set tcl_all64 false
set tcl_runerror_exit false
set assert_report_incompletes 0
set show_force 1
set force_reset_by_reinvoke 0
set tcl_relaxed_literal 0
set probe_exclude_patterns {}
set probe_packed_limit 4k
set probe_unpacked_limit 16k
set assert_internal_msg no
set svseed 1
set assert_reporting_mode 0
set vcd_compact_mode 0

puts $env(wave)
simvision -input $env(wave).svcf
