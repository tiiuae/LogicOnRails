# =============================================================================
# Project:        Logic on Rails
# File:           tempuscontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        15 aug 2025
# Description:    controller for Tempus 
# =============================================================================

import subprocess
import os
import inspect
import shutil
from enum import IntEnum
from pathlib import Path

from types import SimpleNamespace #ok this is pretty cool, great work python devs :)

class LogLevel(IntEnum):
    LOG_INF = 0
    LOG_WRN = 1
    LOG_CRT = 2
    LOG_ERR = 3
    LOG_DBG = 4

GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"
CYAN = "\033[36m"
ENDCOLOR = "\033[0m"

class InnovusController():

    ###############################
    ##         CONSTRUCTOR
    ##
    ################################
    def __init__(self):
        self.en=SimpleNamespace()
        self.lvl=SimpleNamespace()
        self.msg=SimpleNamespace()
        self.path=SimpleNamespace()
        self.defs=SimpleNamespace()
        self.cnfg=SimpleNamespace()
        self.cmd=SimpleNamespace()
        self.manifests = self.genManifests()
        self.genConstants()

    ###############################
    ##         AUX
    ##
    ################################

    def msg_giveColor(self, msg, lvl):
        if (lvl == "LOG_INF"):
            return f"{GREEN}{msg}{ENDCOLOR}"
        elif (lvl == "LOG_WRN"):
            return f"{CYAN}{msg}{ENDCOLOR}"
        elif (lvl == "LOG_CRT"):
            return f"{YELLOW}{msg}{ENDCOLOR}"
        elif (lvl == "LOG_ERR"):
            return f"{RED}{msg}{ENDCOLOR}"
        elif (lvl == "LOG_DBG"):
            return f"{ENDCOLOR}{msg}{ENDCOLOR}"
        else:
            return f"{ENDCOLOR}{msg}{ENDCOLOR}"
        

    def log_msg(self, msg, lvl, wr_file=True):
        req_msg = self.msg_giveColor(msg, lvl)
        if (int(LogLevel[lvl]) >= int(self.lvl.msg) ):
            print(req_msg)
            if (wr_file):
                self.logfile.write(f"{req_msg}\n")

    def listFromFile(self, osvar: str):
        fpath = os.getenv(osvar)
        return [l.rstrip('\n') for l in open(fpath) if not l.lstrip().startswith('#')]

    def remove_files_in_dir(self, path: Path, suffix: str, exclude_substr: str):
        for p in path.iterdir():
            if p.is_file() and p.name.endswith(suffix) and exclude_substr not in p.name:
                p.unlink()

    ###############################
    ##         BUILD VARS
    ##
    ################################
    def genConstants(self):
        self.cnfg.vendor = os.getenv('vendor')
        self.cnfg.module_name = os.getenv('module_name')
        self.cnfg.prj = os.getenv('prj_path')
        self.cnfg.tb_top = os.getenv('tb')
        self.cnfg.usr_opt = os.getenv('cadence_sim_opt')

        self.en.gui = (os.getenv('gui') == "on")
        self.en.ext = (os.getenv('ext_modules') == "on")
        self.en.log = (os.getenv('log') == "on")
        self.en.acc = (os.getenv('access') == "on")
        self.en.keep = (os.getenv('keep') == "on")
        self.en.lp = (os.getenv('cadence_lp_syn') == "on")
        self.en.dbg = (os.getenv('cadence_lp_syn') == "on")
        self.en.dft = (os.getenv('cadence_dft_syn') == "on")
        self.en.phy = (os.getenv('cadence_phy_syn') == "on")
        self.en.ispc = (os.getenv('cadence_ispt_syn') == "on")
        self.en.scan = (os.getenv('cadence_scanc_syn') == "on")
        self.en.lec = (os.getenv('cadence_lec_syn') == "on")
        self.en.atpg = (os.getenv('cadence_atpg_syn') == "on")
        
        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.path.log = os.getenv('innovus_log_name')
        self.path.f = os.getenv('innovus_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.in_sdc = os.getenv('source_sdc')
        self.path.lib = os.getenv('cadence_lib')
        self.path.lef = os.getenv('cadence_lef')
        self.path.deff = os.getenv('cadence_def')
        self.path.saif = os.getenv('cadence_saif')
        self.path.cap = os.getenv('cadence_cap')
        self.path.gds2 = os.getenv('cadence_gds2')
        self.path.qrc = os.getenv('cadence_qrc')
        self.path.cpf = os.getenv('cadence_cpf')

        self.path.sdf = f' {self.cnfg.prj}/{self.cnfg.module_name}.sdf'
        self.path.io = f' {self.cnfg.prj}/{self.cnfg.module_name}.io'
        self.path.fp = f' {self.cnfg.prj}/{self.cnfg.module_name}.fp'
        self.path.prects_net = f' {self.cnfg.prj}/{self.cnfg.module_name}.prects.v'
        self.path.poscts_net = f' {self.cnfg.prj}/{self.cnfg.module_name}.poscts.v'
        self.path.deff = f' {self.cnfg.prj}/{self.cnfg.module_name}.def'
        self.path.spef = f' {self.cnfg.prj}/{self.cnfg.module_name}.spef'
        self.path.gds2_out = f' {self.cnfg.prj}/{self.cnfg.module_name}.gds'
        self.path.db = f' {self.cnfg.prj}/{self.cnfg.module_name}.db'
        self.path.fdeff = f' {self.cnfg.prj}/{self.cnfg.module_name}.final.def'

        self.path.cts_spec = f' {self.path.rprt}/{self.cnfg.module_name}.clock_tree_spec.rpt'
        self.path.cts_strc = f' {self.path.rprt}/{self.cnfg.module_name}.clock_tree_struct.rpt'
        self.path.metrics = f' {self.path.rprt}/{self.cnfg.module_name}.metrics.html'
        self.path.drc = f' {self.path.rprt}/{self.cnfg.module_name}.drc.rpt'
        self.path.connect = f' {self.path.rprt}/{self.cnfg.module_name}.connect.rpt'

        self.path.rpt_time = f' {self.path.rprt}/{self.cnfg.module_name}.time.rpt'
        self.path.rpt_area = f' {self.path.rprt}/{self.cnfg.module_name}.area.rpt'
        self.path.rpt_power = f' {self.path.rprt}/{self.cnfg.module_name}.pwr.rpt'
        self.path.rpt_clocks = f' {self.path.rprt}/{self.cnfg.module_name}.clks.rpt'
        self.path.rpt_hierarchy = f' {self.path.rprt}/{self.cnfg.module_name}.hier.rpt'
        self.path.rpt_summary = f' {self.path.rprt}/{self.cnfg.module_name}.summary.rpt'

    def genManifests(self):
        manifests = dict()
        manifests["rtl"] = self.listFromFile("source_rtl")
        manifests["tb"] = self.listFromFile("source_tb")
        manifests["soft"] = self.listFromFile("source_soft")
        manifests["inc"] = self.listFromFile("source_inc")
        manifests["ips"] = self.listFromFile("source_ips")
        manifests["comp_lib"] = self.listFromFile("source_lib")
        manifests["enc_lib"] = self.listFromFile("source_ext")
        manifests["netlist"] = self.listFromFile("source_netlist")
        return manifests

    ###############################
    ##      Reports
    ##
    ################################ 

    def loadReports(self, f):
        self.log_msg(f"LOG_INF: Reports Generation", "LOG_INF")
        f.write("\n\n#Reports \n")
        f.write(f"report_timing > {self.path.rpt_time} \n")
        f.write(f"report_area > {self.path.rpt_area} \n")
        f.write(f"report_power > {self.path.rpt_power} \n")
        f.write(f"report_clocks > {self.path.rpt_clocks} \n")
        f.write(f"report_hierarchy > {self.path.rpt_hierarchy} \n")
        f.write(f"report_summary > {self.path.rpt_summary} \n")

    ###############################
    ##      Close
    ##
    ################################
     
    def loadGUI(self, f):
        if (self.en.gui):
            f.write("\n\n#Gui \n")
            f.write(f"gui_show \n")
        else:
            f.write(f"quit \n")
    
    ###############################
    ##      POST SCRIPT
    ##
    ################################ 

    def cleanEnv(self):
        if os.path.exists(self.path.f): 
            if (self.en.log):
                shutil.move(self.path.f, f"{self.path.rprt}/{self.path.f}")
            else:
                if not self.en.keep : os.remove(self.path.f)
        if os.path.exists(self.path.log): 
            if (self.en.log):
                shutil.move(self.path.log, f"{self.path.rprt}/{self.path.log}")
            else:
                if not self.en.keep : os.remove(self.path.log)


    def printLogs(self):
        if (self.en.log):
            print(f"{GREEN}INFO:Displaying compilation {RED}ERRORS\n")
            os.system(f'grep "LOG_ERR" {self.path.rprt}/{self.path.log}')
            os.system(f'grep "ERROR" {self.path.rprt}/{self.path.f}')
            print(ENDCOLOR)

    ###############################
    ##      Initial Configs
    ##
    ################################

    def generateWarn(self, f): 
        self.log_msg(f"LOG_CRT: Script Generator, do not run automatically, use as template only", "LOG_CRT")
        f.write("\n\n#use as template only\n")

    def defaultConfig(self, f):
        f.write(f'set_db write_def_hierarchy_delimiter {{/}}\n')
        f.write(f'set_db delaycal_input_transition_delay {{0.1ps}}\n')
        f.write(f'set_db delaycal_input_transition_delay {{0.1ps}}\n')
        f.write(f'set_db floorplan_default_site {{<site_name>}}\n')
        f.write(f'set_db init_power_nets {{VDD}}"\n')
        f.write(f'set_db init_ground_nets {{VSS}}"\n')
        f.write(f'set_db design_process_node <node>"\n')
        f.write(f'set_db design_top_routing_layer <metal>\n')
        f.write(f'set_db design_bottom_routing_layer <metal>\n')
        
    def lowPowerConfig(self, f):
        if self.en.lp:
            f.write(f'set_db design_power_effort high"\n')
            f.write(f'set_db opt_leakage_to_dynamic_ratio 0.5"\n')

    def configEnv(self, f):
        self.log_msg(f"LOG_INF: Configuring Env", "LOG_INF")
        f.write("\n\n#Config Env\n")
        self.defaultConfig(f)
        self.lowPowerConfig(f)

    ###############################
    ##      Lef
    ##
    ################################ 

    def loadLef(self, f):
        if os.path.isfile(self.path.lef):
            f.write(f'read_physical -lef {self.path.lef}\n')
        elif os.path.isdir(self.path.lef):
            for filename in os.listdir(self.path.lef):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    f.write(f'read_physical -lef {self.path.lef}\n')
        else:
            self.log_msg(f"LOG_ERR: Innovus run, Specified lef is neither a file nor a path", "LOG_ERR")
            f.write(f'#ERROR, PHYSICAL FLOW AND NO LEF LOADED\n')

    ###############################
    ##      Netlist
    ##
    ################################ 

    def loadNetlist(self, f):
        if self.manifests["netlist"]:
            self.log_msg(f"LOG_INF: Loading your netlists", "LOG_INF")
            f.write("\n\n#Netlists \n")
            for each_net in self.manifests["netlist"]:
                f.write(f'read_netlist {each_net}\n')


    ###############################
    ##      Init Design
    ##
    ################################ 

    def loadInit(self, f):
        self.log_msg(f"LOG_INF: Init Design", "LOG_INF")
        f.write("\n\n#Init Design\n")
        f.write(f'init_design\n')

    ###############################
    ##      FloorPlan
    ##
    ################################ 

    def loadFP(self, f):
        self.log_msg(f"LOG_INF: Loading FloorPlan", "LOG_INF")
        f.write("\n\n#FloorPlan\n")
        f.write(f'create_floorplan -site <site> -core_size <size.a> <size.b> <size.c> <size.d> <size.e> <size.f> -match_to_site\n')

    def loadPins(self, f):
        self.log_msg(f"LOG_INF: Loading Pins", "LOG_INF")
        f.write("\n\n#Pins\n")
        f.write(f'set_db assign_pins_edit_in_batch true\n')
        f.write(f'edit_pin -fix_overlap 1 -pin_width <width> -unit micron -spread_direction clockwise -side Bottom -layer <layer> -spread_type center -spacing <spacing> -pin {{ <pin list space separated> }} \n')
        f.write(f'edit_pin -fix_overlap 1 -pin_width <width> -unit micron -spread_direction clockwise -side Bottom -layer <layer> -spread_type center -spacing <spacing> -pin {{ <pin list space separated> }} \n')

    def genIOFile(self, f):
        self.log_msg(f"LOG_INF: Generating IO File", "LOG_INF")
        f.write("\n\n#IO File\n")
        f.write(f'write_io_file -locations {self.path.io}\n')

    def loadConnections(self, f):
        self.log_msg(f"LOG_INF: Generating Power Connections", "LOG_INF")
        f.write("\n\n#Power Connections\n")
        f.write(f'connect_global_net VDD -type pg_pin -pin_base_name VDD -inst_base_name *\n')
        f.write(f'connect_global_net VSS -type pg_pin -pin_base_name VSS -inst_base_name *\n')
        f.write(f'connect_global_net VSS -type tie_lo -all\n')
        f.write(f'connect_global_net VDD -type tie_hi -all\n')

    def loadRings(self, f):
        self.log_msg(f"LOG_INF: Generating Power Ring", "LOG_INF")
        f.write("\n\n#Power Ring\n")
        f.write(f'set_db add_rings_target default\n') 
        f.write(f'set_db add_rings_extend_over_row 0  \n')
        f.write(f'set_db add_rings_ignore_rows 0  \n')
        f.write(f'set_db add_rings_avoid_short 0  \n')
        f.write(f'set_db add_rings_skip_shared_inner_ring none  \n')
        f.write(f'set_db add_rings_stacked_via_top_layer <Metal>  \n')
        f.write(f'set_db add_rings_stacked_via_bottom_layer <Metal>  \n')
        f.write(f'set_db add_rings_via_using_exact_crossover_size 1  \n')
        f.write(f'set_db add_rings_orthogonal_only true  \n')
        f.write(f'set_db add_rings_skip_via_on_pin {{  standardcell }} ; \n')
        f.write(f'set_db add_rings_skip_via_on_wire_shape {{  noshape }}\n')
        f.write(f'add_rings -nets {{VDD VSS}} -type core_rings -follow core -layer {{top <Metal> bottom <Metal> left <Metal> right <Metal>}} -width {{top <width> bottom <width> left <width> right <width>}} -spacing {{top <spacing> bottom <spacing> left <spacing> right <spacing>}} -offset {{top <offset> bottom offset> left offset> right offset>}} -center 0 -threshold 0 -jog_distance 0 -snap_wire_center_to_grid grid\n')

    def loadStripes(self, f):
        self.log_msg(f"LOG_INF: Generating Power Stripes", "LOG_INF")
        f.write("\n\n#Power Stripes\n")
        f.write(f'set_db add_stripes_ignore_block_check false  \n')
        f.write(f'set_db add_stripes_break_at none  \n')
        f.write(f'set_db add_stripes_route_over_rows_only false  \n')
        f.write(f'set_db add_stripes_rows_without_stripes_only false  \n')
        f.write(f'set_db add_stripes_stop_at_last_wire_for_area false  \n')
        f.write(f'set_db add_stripes_partial_set_through_domain false  \n')
        f.write(f'set_db add_stripes_ignore_non_default_domains false  \n')
        f.write(f'set_db add_stripes_spacing_type edge_to_edge  \n')
        f.write(f'set_db add_stripes_spacing_from_block 0 \n')
        f.write(f'set_db add_stripes_stripe_min_length stripe_width  \n')
        f.write(f'set_db add_stripes_stacked_via_top_layer <Metal>  \n')
        f.write(f'set_db add_stripes_stacked_via_bottom_layer <Metal>  \n')
        f.write(f'set_db add_stripes_via_using_exact_crossover_size false  \n')
        f.write(f'set_db add_stripes_split_vias false  \n')
        f.write(f'set_db add_stripes_orthogonal_only true  \n')
        f.write(f'set_db add_stripes_extend_to_closest_target ring\n')
        f.write(f'add_stripes -nets {{VDD VSS}} -layer <Metal> -direction <vertical/horizontal> -width <width> -spacing <spacing> -set_to_set_distance <distance> -extend_to design_boundary -start_from <left/right> -start_offset <offset> -switch_layer_over_obs false -max_same_layer_jog_length 2 -pad_core_ring_top_layer_limit <Metal> -pad_core_ring_bottom_layer_limit <Metal> -block_ring_top_layer_limit <Metal> -block_ring_bottom_layer_limit <Metal> -use_wire_group 0 -snap_wire_center_to_grid grid\n')

    def loadSRouting(self, f):
        self.log_msg(f"LOG_INF: Loading cell power routing", "LOG_INF")
        f.write("\n\n#cell power routing\n")
        f.write(f'route_special -connect {{core_pin floating_stripe}} -layer_change_range {{ <Metal> <Metal> }} -floating_stripe_target {{block_ring pad_ring ring stripe ring_pin block_pin followpin}} -allow_jogging 1 -crossover_via_layer_range {{ <Metal> <Metal> }} -nets {{ VDD VSS }} -allow_layer_change 1 -target_via_layer_range {{ <Metal> <Metal> }}\n')

    def loadPinPlan(self, f):
        self.loadPins(f)
        self.genIOFile(f)

    def loadPowerPlan(self, f):
        self.loadConnections(f)
        self.loadRings(f)
        self.loadStripes(f)
        self.loadSRouting(f)

    def loadFloorPlanInfo(self, f):
        self.loadFP(f)
        self.loadPinPlan(f)
        self.loadPowerPlan(f)

    ###############################
    ##      Placement
    ##
    ################################ 

    def loadPlacement(self, f):
        self.log_msg(f"LOG_INF: Loading placement info", "LOG_INF")
        f.write("\n\n#Placement\n")
        f.write(f'place_opt_design\n')
        f.write(f'pop_snapshot_stack\n')

    def savePlacement(self, f):
        self.log_msg(f"LOG_INF: Saving Placement", "LOG_INF")
        f.write("\n\n#Storing Placement Info\n")
        f.write(f'write_floorplan {self.path.fp}\n')
        f.write(f'create_snapshot -name pre_placeOpt -categories "design setup power"\n')
        f.write(f'write_netlist {self.path.prects_net}\n')
        f.write(f'write_def -floorplan -no_std_cells {self.path.deff}\n')

    def loadPlacementInfo(self, f):
        self.loadPlacement(f)
        self.savePlacement(f)

    ###############################
    ##      Route
    ##
    ################################ 

    def loadRouteRules(self, f):
        self.log_msg(f"LOG_INF: Generating routing rules", "LOG_INF")
        f.write("\n\n#Routing rules\n")
        f.write(f'create_route_type -name leaf_rule -top_preferred_layer <metal> -bottom_preferred_layer <metal>\n')
        f.write(f'create_route_type -name trunk_rule -top_preferred_layer <metal> -bottom_preferred_layer <metal>\n')  
        f.write(f'create_route_type -name top_rule -top_preferred_layer <metal> -bottom_preferred_layer <metal>\n')  
        f.write(f'set_db add_fillers_cells {{<fillers1> <fillers2>}}\n')

    def loadCTSRules(self, f):
        self.log_msg(f"LOG_INF: Generating CTS rules", "LOG_INF")
        f.write("\n\n#CTS rules\n")
        f.write(f'set_db cts_route_type_leaf  leaf_rule\n')
        f.write(f'set_db cts_route_type_trunk trunk_rule\n')
        f.write(f'set_db cts_route_type_top   top_rule\n')
        f.write(f'set_db cts_top_fanout_threshold <value>\n')
        f.write(f'set_db  cts_target_skew <skew>\n')

    def checkCTSSpec(self, f):
        self.log_msg(f"LOG_INF: Checking CTS Spec", "LOG_INF")
        f.write("\n\n#CTS Spec\n")
        f.write(f'create_clock_tree_spec -out_file {self.path.cts_spec}\n')
        f.write(f'check_design -type cts\n') 
        f.write(f'push_snapshot_stack\n')

    def genCTS(self, f):
        self.log_msg(f"LOG_INF: Loading CTS", "LOG_INF")
        f.write("\n\n#CTS\n")
        f.write(f'ccopt_design\n')

    def loadCTSOpt(self, f):
        self.log_msg(f"LOG_INF: Loading CTS Optimizations", "LOG_INF")
        f.write("\n\n#CTS OPT\n")
        f.write(f'set_interactive_constraint_modes [all_constraint_modes -active]\n')
        f.write(f'reset_clock_tree_latency [all_clocks]\n')
        f.write(f'set_propagated_clock [all_clocks]\n')
        f.write(f'set_interactive_constraint_modes []\n')
        f.write(f'opt_design -post_cts -report_dir {self.path.rprt}\n')
        f.write(f'time_design -post_cts -report_dir {self.path.rprt}\n')
        f.write(f'opt_design -post_cts -hold -report_dir  {self.path.rprt}\n')
        f.write(f'time_design -post_cts -hold -report_dir {self.path.rprt}\n')
        f.write(f'report_clock_tree_structure -show_sinks -out_file {self.path.cts_strc} \n') 

    def loadCTS(self, f): 
        self.loadCTSRules(f)
        self.checkCTSSpec(f)
        self.genCTS(f)
        self.loadCTSOpt(f)

    def configPostRoute(self, f):
        self.log_msg(f"LOG_INF: Post Route Config", "LOG_INF")
        f.write("\n\n#Post Route\n")
        f.write(f'set_db extract_rc_engine post_route\n')
        f.write(f'set_db extract_rc_effort_level low\n')
        f.write(f'opt_design -post_route -setup -hold -report_dir {self.path.rprt}\n')
        f.write(f'create_snapshot -name post_route -categories "design setup hold power route"\n')
        f.write(f'report_metric -out_file {self.path.metrics} -format html\n')

    def loadFillers(self, f):
        self.log_msg(f"LOG_INF: Loading Filler Cells", "LOG_INF")
        f.write("\n\n#Filler Cells\n")
        f.write(f'add_fillers\n')

    def loadRouteChecks(self, f):
        self.log_msg(f"LOG_INF: Load DRC Checks", "LOG_INF")
        f.write("\n\n#DRC Checks\n")
        f.write(f'check_drc -out_file {self.path.drc}\n')
        f.write(f'check_connectivity -ignore_soft_pg_connects -out_file {self.path.connect}\n')

    def loadRoute(self, f):
        self.log_msg(f"LOG_INF: Routing Design", "LOG_INF")
        f.write("\n\n#Routing\n")
        f.write(f'route_design\n')
        self.configPostRoute(f)
        self.loadFillers(f)
        self.loadRouteChecks(f)


    def loadRoutingInfo(self, f):
        self.loadRouteRules(f)
        self.loadCTS(f)
        self.loadRoute(f)

    ###############################
    ##      Parasitics
    ##
    ################################ 

    def loadParasitics(self, f):
        self.log_msg(f"LOG_INF: Generate Parasitics info", "LOG_INF")
        f.write("\n\n#Parasitics\n")
        f.write(f'set_db extract_rc_engine post_route\n')
        f.write(f'set_db extract_rc_effort_level low\n')
        f.write(f'set_db extract_rc_coupled true\n')
        f.write("\n\n#layermap file is not in yaml\n")
        f.write(f'set_db extract_rc_lef_tech_file_map <layermap.file>\n')
        f.write(f'extract_rc\n')
        f.write(f'write_parasitics -rc_corner <corner> -spef_file {self.path.spef}\n') 

    ###############################
    ##      Netlist
    ##
    ################################ 

    def loadFinalNetlist(self,f):
        self.log_msg(f"LOG_INF: Generate Final post CTS netlist", "LOG_INF")
        f.write("\n\n#CTS netlist\n")
        f.write(f'write_netlist -top_module_first {self.path.poscts_net}\n')

    ###############################
    ##      SDF
    ##
    ################################ 

    def loadFinalSDF(self,f):
        self.log_msg(f"LOG_INF: Generate Final SDF", "LOG_INF")
        f.write("\n\n#SDF\n")
        f.write(f'write_sdf -typical_view <viw> {self.path.sdf}\n')


    ###############################
    ##      Save Design
    ##
    ################################ 

    def loadGSDInfo(self, f):
        self.log_msg(f"LOG_INF: Generating GDS2", "LOG_INF")
        f.write("\n\n#GDS2\n")
        f.write(f'write_sdf -typical_view <viw> {self.path.sdf}\n')
        f.write(f'write_stream {self.path.gds2_out} -lib_name {{self.cnfg.module_name}} -map_file {{<map_file>}} -merge {{{self.path.gds2}}} -unit <unit> -mode all -die_area_as_boundary\n')

    def writeDb(self, f):
        self.log_msg(f"LOG_INF: Saving DB", "LOG_INF")
        f.write("\n\n#Saving DB\n")
        f.write(f'write_db {self.path.db}\n')

    def writeDeff(self, f):
        self.log_msg(f"LOG_INF: Saving Def", "LOG_INF")
        f.write("\n\n#Saving Def\n")
        f.write(f'write_def -netlist -routing {self.path.fdeff}\n')

    def saveDesign(self, f):
        self.loadGSDInfo(f)
        self.writeDb(f)
        self.writeDeff(f)

    ###############################
    ##      Route
    ##
    ################################ 

    def createRouteEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.generateWarn(f)
        self.configEnv(f)
        self.loadLef(f)
        self.loadNetlist(f)
        self.loadInit(f)
        self.loadFloorPlanInfo(f)
        self.loadPlacementInfo(f)
        self.loadRoutingInfo(f)
        self.loadParasitics(f)
        self.loadFinalNetlist(f)
        self.loadFinalSDF(f)
        self.saveDesign(f)
        self.loadGUI(f)
        self.logfile.close()

