create_library_set -name wcl_slow -timing {
    <cells>
}

create_library_set -name wcl_fast -timing {
    <cells>
}

create_library_set -name wcl_typical -timing {
    <cells>
}

create_opcond -name op_cond_wcl_slow -process <process> -voltage <voltage_eg_1.8> -temperature <temp_eg_125> 
create opcond -name op_cond_wcl_fast -process <process> -voltage <voltage_eg_1.32> -temperature <temp_eg_125> 
create_opcond -name op_cond_wcl_typical -process <process> -voltage <voltage_eg_1.25> -temperature <voltage_eg_1.32>

create_timing_condition -name timing_cond_wcl_slow -opcond slow -library_sets {wcl_slow} 
create_timing_condition -name timing_cond_wcl_fast -opcond fast -library_sets {wcl_fast}
create_timing_condition -name timing_cond_wcl_typical -opcond typical -library_sets {wcl_typical}

create_rc_corner -name rc_corner -qrc_tech <qrcTechFile>

create_delay_corner -name delay_corner_wcl_slow -early_timing_condition timing_cond_wcl_slow \ 
    -late_timing_condition timing_cond_wcl_slow -early_rc_corner rc_corner                   \ 
    -late_rc_corper rc_corner

create_delay_corner -name delay_corner_wcl_fast -early_timing_condition timing_cond_wcl_fast \
    -late_timing_condition timing_cond_wcl_fast -early_rc_corner rc_corner                   \
    -late_rc_corner rc corner

create_delay_corner -name delay_corner_wcl_typical -early_timing_condition timing_cond_wcl_typical \ 
    -late_timing_condition timing_cond_wcl_typical -early_rc_corner rc_corner                      \
    -late_rc_corner rc corner

create_constraint_mode -name functional_wcl_slow -sdc_files {slow.sdc}
create_constraint_mode -name functional wcl fast -sdc_files {fast.sdc}
create_constraint_mode -name functional_wcl_typical -sdc_files {typical.sdc}

create_analysis view -name view_wcl_slow -constraint_mode functional_wcl_slow -delay_corner delay_corner_wcl_slow
create_analysis view -name view_wcl_fast -constraint_mode functional_wcl_fast -delay_corner delay_corner_wcl_fast
create_analysis view -name view_wcl_typical -constraint_mode functional_wcl_typical -delay_corner delay_corner_wcl_typical

set_analysis_view -setup {view_wcl_slow view_wcl_fast view wcl_typical}