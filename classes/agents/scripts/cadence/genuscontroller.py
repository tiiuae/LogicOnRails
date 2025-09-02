# =============================================================================
# Project:        Logic on Rails
# File:           genuscontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        15 aug 2025
# Description:    controller for Genus 
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

class GenusController():

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
        self.genCommandVars()

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
        self.en.phy = (os.getenv('cadence_phy_syn') == "on")
        self.en.ispc = (os.getenv('cadence_ispt_syn') == "on")
        self.en.scan = (os.getenv('cadence_scanc_syn') == "on")
        self.en.lec = (os.getenv('cadence_lec_syn') == "on")
        self.en.atpg = (os.getenv('cadence_atpg_syn') == "on")
        
        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.path.log = os.getenv('genus_log_name')
        self.path.f = os.getenv('genus_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.in_sdc = os.getenv('source_sdc')
        self.path.lib = os.getenv('cadence_lib')
        self.path.lef = os.getenv('cadence_lef')
        self.path.deff = os.getenv('cadence_def')
        self.path.saif = os.getenv('cadence_saif')
        self.path.cap = os.getenv('cadence_cap')
        self.path.qrc = os.getenv('cadence_qrc')
        self.path.cpf = os.getenv('cadence_cpf')
        self.path.out_sdc = f"{self.cnfg.prj}/{self.cnfg.module_name}.genus.sdc"
        self.path.out_sdf = f"{self.cnfg.prj}/{self.cnfg.module_name}.genus.sdf"

        self.path.elab_snap = f' {self.path.rprt}/{self.cnfg.module_name}.elab.v'
        self.path.gen_snap = f' {self.path.rprt}/{self.cnfg.module_name}.gen.v'
        self.path.map_snap = f' {self.path.rprt}/{self.cnfg.module_name}.map.v'
        self.path.opt_snap = f' {self.path.rprt}/{self.cnfg.module_name}.opt.v'
        self.path.opt_inc_snap = f' {self.path.rprt}/{self.cnfg.module_name}.opt.dft.v'
        self.path.scandef = f' {self.path.rprt}/{self.cnfg.module_name}.scandef'

        self.path.time_intent = f' {self.path.rprt}/{self.cnfg.module_name}.timeintent.rpt'
        self.path.do_mlec = f' {self.path.rprt}/{self.cnfg.module_name}.lec.map.do'
        self.path.do_flec = f' {self.path.rprt}/{self.cnfg.module_name}.lec.opt.do'
        self.path.db = f' {self.cnfg.prj}/{self.cnfg.module_name}.db'
        self.path.invs = f' {self.cnfg.prj}/INVS'

        self.path.rpt_time = f' {self.path.rprt}/{self.cnfg.module_name}.time.rpt'
        self.path.rpt_area = f' {self.path.rprt}/{self.cnfg.module_name}.area.rpt'
        self.path.rpt_power = f' {self.path.rprt}/{self.cnfg.module_name}.pwr.rpt'
        self.path.rpt_clocks = f' {self.path.rprt}/{self.cnfg.module_name}.clks.rpt'
        self.path.rpt_hierarchy = f' {self.path.rprt}/{self.cnfg.module_name}.hier.rpt'
        self.path.rpt_summary = f' {self.path.rprt}/{self.cnfg.module_name}.summary.rpt'
        self.path.rpt_scan = f' {self.path.rprt}/{self.cnfg.module_name}.scanchain.rpt'
        self.path.rpt_dft_vltns = f' {self.path.rprt}/{self.cnfg.module_name}.dft_violations.rpt'
        self.path.rpt_dftpre = f' {self.path.rprt}/{self.cnfg.module_name}.dft_pre.rpt'
        self.path.rpt_dftprefix = f' {self.path.rprt}/{self.cnfg.module_name}.dft_pre_fix.rpt'
        self.path.rpt_dftpos = f' {self.path.rprt}/{self.cnfg.module_name}.dft_pos.rpt'

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        self.defs.eda_tool = f"-define SYNTHESIS -define GENUS"

        self.cmd.phy = "-physical" if (self.en.phy) else ""
        self.cmd.ispt = "-spatial" if (self.en.ispc) else ""

    def genCommandVars(self):
        self.altera_ip_libs = ""
        self.cmd.rtl = ""
        self.cmd.ext = ""
        self.cmd.tb = ""
        self.cmd.dsgn = ""
        self.cmd.ip = ""
        self.cmd.inc = ""
        self.cmd.pli = ""
        self.cmd.dpi = ""
        self.cmd.vpi = ""
        self.cmd.uvm = ""
        self.cmd.soft = ""
        self.cmd.cov = ""
        self.cmd.gui = ""
        self.cmd.wave = ""
        self.cmd.defs = f"{self.defs.eda_tool} "

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
    ##      Defines
    ##
    ################################ 

    def genDefines(self, f):
        self.log_msg(f"LOG_INF: Generating defines", "LOG_INF")
        self.cmd.defs += f" {self.defs.synth.replace('+define+',' -define ').replace('+',' ').strip()}"

    ###############################
    ##      Physical
    ##
    ################################ 

    def loadLef(self, f):
        if os.path.isfile(self.path.lef):
            f.write(f'read_physical -lef {self.path.lef}\n')
        elif os.path.isdir(self.path.lef):
            for filename in os.listdir(self.path.lef):
                full_path = os.path.join(folder_path, filename)
                if os.path.isfile(full_path):
                    f.write(f'read_physical -lef {full_path}\n')
        else:
            self.log_msg(f"LOG_ERR: Physical run, Specified lef is neither a lib nor a path", "LOG_ERR")
            f.write(f'#ERROR, PHYSICAL FLOW AND NO LEF LOADED\n')

    def loadQRC(self, f):
        if self.path.qrc:
            if os.path.isfile(self.path.qrc):
                f.write(f'set_db qrc_tech_file {self.path.qrc}\n')
            else:
                self.log_msg(f"LOG_ERR: Physical run, specified QRC is neither a file nor a path", "LOG_ERR")
                f.write(f'#ERROR, PHYSICAL QRC TABLE NOT LOADED\n')


    def loadCap(self, f):
        if self.path.cap:
            if os.path.isfile(self.path.cap):
                f.write(f'set_db cap_table_file {self.path.cap}\n')
            else:
                self.log_msg(f"LOG_ERR: Physical run, specified cap table is neither a file nor a path", "LOG_ERR")
                f.write(f'#ERROR, PHYSICAL CAP TABLE NOT LOADED\n')

    def loadPhysical(self, f):
        if (self.en.phy):
            self.log_msg(f"LOG_WRN: Physical Synthsis enabled", "LOG_WRN")
            f.write("\n\n#Power Rails \n")
            f.write(f'set_db init_power_nets  "VDD"\n')
            f.write(f'set_db init_ground_nets "VSS"\n')
            self.loadLef(f)
            self.loadQRC(f)
            self.loadCap(f)
            if (self.en.ispc):
                self.log_msg(f"LOG_CRT: You are running ISPATIAL Flow, be sure you have the correct license", "LOG_CRT")
                f.write(f'set_db opt_spatial_effort extreme\n')

    ###############################
    ##      Load Stuff
    ##
    ################################ 

    def loadLib(self, f):
        self.log_msg(f"LOG_INF: Load Library", "LOG_INF")
        f.write("\n\n#Libraries \n")
        if os.path.isfile(self.path.lib):
            f.write(f'read_libs {self.path.lib}\n')
        elif os.path.isdir(self.path.lib):
            f.write(f'set_db init_lib_search_path {self.path.lib}\n')
            for filename in os.listdir(self.path.lib):
                full_path = os.path.join({self.path.lib}, filename)
                if os.path.isfile(full_path):
                    f.write(f'read_libs {full_path}\n')
                    f.write(f'set_db invs_temp_dir {self.path.invs}\n')
        else:
            self.log_msg(f"LOG_ERR: Specified lib is neither a lib nor a path", "LOG_ERR")
            f.write(f'#ERROR, NO LIB LOADED\n')


    def loadDbgEnv(self, f):
        if (self.en.dbg):
            f.write("\n\n#Debug Init Options \n")
            f.write(f'set_db hdl_track_filename_row_col true\n')
            f.write(f'set_db information_level 4\n')
            f.write(f'set_db delete_unloaded_insts false\n')
            f.write(f'set_db auto_ungroup none\n')
        else:
            f.write(f'set_db auto_ungroup both\n')

    def loadLowPower(self, f):
        if (self.en.lp):
            f.write("\n\n#Low Power Options \n")
            f.write(f'set_db lp_insert_clock_gating true\n')
            f.write(f'set_db lp_insert_discrete_clock_gating_logic true #set to false if lib has CG cells\n')
            f.write(f'set_db design_power_effort high\n')
            f.write(f'set_db opt_leakage_to_dynamic_ratio 0.5 #user must define a value between 0 and 1\n')
            f.write(f'set_db opt_leakage_to_dynamic_ratio 0.5 #user must define a value between 0 and 1\n')
            f.write(f'set_db lp_clock_gating_max_flops 16 #change these values as you see fit, if error comment\n')
            f.write(f'set_db lp_clock_gating_min_flops 4  #change these values as you see fit, if error comment\n')

    def loadEffort(self, f):
        f.write("\n\n#Effort Information \n")
        f.write(f'set_db syn_map_effort high\n')
        f.write(f'set_db syn_generic_effort high\n')
        f.write(f'set_db syn_opt_effort high\n')

    def loadScan(self, f):
        if self.en.scan:
            f.write(f'set_db dft_scan_style muxed_scan\n')
            f.write(f'set_db dft_prefix dft_\n')


    def setEnv(self, f):
        self.loadLib(f)
        self.loadDbgEnv(f)
        self.loadPhysical(f)
        self.loadLowPower(f)
        self.loadScan(f)
        self.loadEffort(f)

    ###############################
    ##             RTL
    ##
    ################################ 
    
    def loadIncludes(self, f):
        self.log_msg(f"LOG_INF: Loading your Includes RTL paths", "LOG_INF")
        if self.manifests["inc"]:
            f.write("\n\n#Includes \n")
            f.write(f'set_db init_hdl_search_path {" ".join(self.manifests["inc"])}\n')

    
    def loadRTL(self, f):
        self.log_msg(f"LOG_INF: Loading your design RTL files", "LOG_INF")
        f.write("\n\n#RTL \n") 
        for each_rtl in self.manifests["rtl"]:
            lang_opt = ""
            if (".sv" in each_rtl):
                lang_opt = "-language sv"
            elif (".vhd" in each_rtl):
                lang_opt = "-language vhdl"
            f.write(f'read_hdl {self.cmd.defs} {lang_opt} {each_rtl}\n')

    def loadExt(self, f):
        if self.manifests["enc_lib"]:
            self.log_msg(f"LOG_INF: Loading your encrypted .vop files", "LOG_INF")
            f.write("\n\n#.VP files \n")
            for each_enc in self.manifests["enc_lib"]:
                f.write(f'read_hdl {each_enc}\n')

    def loadNetlist(self, f):
        if self.manifests["netlist"]:
            self.log_msg(f"LOG_INF: Loading your netlists", "LOG_INF")
            f.write("\n\n#Netlists \n")
            for each_net in self.manifests["netlist"]:
                f.write(f'read_netlist {each_net}\n')


    ###############################
    ##      Time SDC SDF
    ##
    ################################ 

    def readSDC(self, f):
        self.log_msg(f"LOG_INF: loading SDC file", "LOG_INF")
        f.write("\n\n#SDC \n")
        f.write(f'read_sdc -stop_on_errors {self.path.in_sdc}\n')

    def writeSDC(self, f):
        self.log_msg(f"LOG_INF: Writing netlist sdc", "LOG_INF")
        f.write("\n\n#Write Netlist's SDC \n")
        f.write(f'write_sdc > {self.path.out_sdc}\n')

    def writeSDF(self, f):
        self.log_msg(f"LOG_INF: Writing netlist sdf", "LOG_INF")
        f.write("\n\n#Write Netlist's SDF \n")
        f.write(f'write_sdf -timescale ns -nonegchecks -recrem split -edges check_edge -setuphold split > {self.path.out_sdf}\n')

    ###############################
    ##      Elab
    ##
    ################################ 

    def checkDesign(self, f):
        self.log_msg(f"LOG_INF: checking design consistance", "LOG_INF")
        f.write("\n\n#Check Design \n")
        f.write(f'check_design\n')
        f.write(f'check_design -unresolved\n')


    def elabDesign(self, f):
        self.log_msg(f"LOG_INF: Elab Design", "LOG_INF")
        f.write("\n\n#Elab and init \n")
        f.write(f'elaborate\n')
        self.checkDesign(f)
        f.write(f'write_hdl > {self.path.elab_snap}\n')
        f.write(f'init_design\n')

    ###############################
    ##      Timing Intent
    ##
    ################################ 

    def checkTimingIntent(self, f):
        f.write("\n\n#Check SDC \n")
        f.write(f'check_timing_intent > {self.path.time_intent}\n')

    ###############################
    ##      Pre Synthesis LP
    ##
    ################################ 

    def loadSaif(self, f):
        self.log_msg(f"LOG_WRN: Running LP Saif flow", "LOG_WRN")
        f.write("\n\n#Load Saif \n")
        if os.path.isfile(self.path.saif):
            f.write(f'read_saif {self.path.saif}\n')
        else:
            self.log_msg(f"LOG_ERR: LP SAIF run, but specified saif does not exist", "LOG_ERR")
            f.write(f'#ERROR, NO SAIF LOADED\n')

    def loadCPF(self, f):
        self.log_msg(f"LOG_WRN: Running LP CPF flow", "LOG_WRN")
        f.write("\n\n#Load CPF \n")
        if os.path.isfile(self.path.cpf):
            f.write(f'read_power_intent -cpf {self.path.cpf} -module {self.cnfg.module_name}\n')
            f.write(f'check_cpf\n')
            f.write(f'apply_power_intent\n')
            f.write(f'commit_power_intent\n')
            f.write(f'check_power_structure\n')
        else:
            self.log_msg(f"LOG_ERR: LP CPF run, but specified cpf does not exist", "LOG_ERR")
            f.write(f'#ERROR, NO CPF LOADED\n')

    def loadPreSynthLP(self, f):
        if self.path.saif:
            self.loadSaif(f)
        if self.path.cpf:
            self.loadCPF(f)

    ###############################
    ##      Pre Synthesis ispatial
    ##
    ################################ 

    def loadDef(self, f):
        self.log_msg(f"LOG_WRN: Running Ispatual def flow", "LOG_WRN")
        f.write("\n\n#Load DEF \n")
        if os.path.isfile(self.path.deff):
            f.write(f'read_def -fuzzy_match {self.path.deff}\n')
            f.write(f'check_floorplan\n')
        else:
            self.log_msg(f"LOG_ERR: ISPATUAL run, but specified def does not exist", "LOG_ERR")
            f.write(f'#ERROR, NO DEF LOADED\n')


    def loadCostGroup(self, f):
        f.write(f'#Note: Genus write both the all_registers and all_register var in its manual, it is important to verify which is the correct on\n')
        f.write(f'foreach view [get_db analysis_views -if {{.is_setup == true\}}] {{\n')
        f.write(f'    if {{[llength [all_registers]] > 0}} {{ \n')
        f.write(f'	define_cost_group -name I2C -design {self.cnfg.module_name}\n')
        f.write(f'	define_cost_group -name C2O -design {self.cnfg.module_name}\n')
        f.write(f'	define_cost_group -name C2C -design {self.cnfg.module_name}\n')
        f.write(f'	path_group -from [all_registers] -to [all_outputs] -group C2O -name C2O -view $view\n')
        f.write(f'	path_group -from [all_inputs]  -to [all_registers] -group I2C -name I2C -view $view\n')
        f.write(f'	path_group -from [all_registers] -to [all_registers] -group C2C -name C2C -view $view\n')
        f.write(f'    }}\n')
        f.write(f'    define_cost_group -name I2O -design {self.cnfg.module_name}\n')
        f.write(f'    path_group -from [all_inputs]  -to [all_outputs] -group I2O -name I2O -view $view\n')
        f.write(f'}}\n')

    def loadPreSynthIspatial(self, f):
        f.write("\n\n#ISPATIAL PreSynth Flow \n")
        f.write(f'report_ple\n')
        self.loadDef(f)

    ###############################
    ##      Scan Chain 
    ##
    ################################ 

    def loadScanChainPreSynth(self, f):
        #TODO : CHECK IF PIN ALREADY EXIST IN TOP LEVEL BEFORE SETTING -create_port
        f.write("\n\n#ScanChain PreSynth Flow \n")
        if self.en.ispc:
            f.write(f'dft_physical_aware_test_points true\n')
        f.write(f'#Note: you may use\n')
        f.write(f'#define_<shift/clock/test> -active high <name>\n')
        f.write(f'define_shift_enable -name SE -active high -create_port SE\n')
        f.write(f'define_test_mode -name TM -active high -create_port TM\n')
        f.write(f'define_test_clock -name TCLK -create_port TCLK\n')
        f.write("#the line below allows you to use shift registers in your design as scan chain\n")
        f.write(f'#define_shift_register_segment -start_flop Your.Design.LFSR[0] -end_flop Your.Design.LFSR[7]\n')
        f.write("#the line below allows you to use shadown login and bypass memories\n")
        f.write(f'#add_shadow_logic -auto\n')
        f.write(f'check_dft_rules > {self.path.rpt_dftpre}\n')
        f.write(f'fix_dft_violations -test_control TM -async_set -async_reset -clock\n')
        f.write(f'check_dft_rules > {self.path.rpt_dftprefix}\n')


    def loadScanChainPosSynth(self, f):
        f.write("\n\n#ScanChain PosSynth Flow \n")
        f.write("#the line below allows you to use shadown login and bypass specific memories\n")
        f.write(f'#add_shadow_logic -around [get_db insts *<your memory here>*] -mode share -test_control TM -test_clock_pin TCLK -balance\n')
        f.write(f'check_dft_rules > {self.path.rpt_dftpos}\n')
        f.write(f'syn_opt {self.cmd.ispt}\n')
        f.write(f'define_scan_chain -name top_chain -sdi TDI -sdo TDO -create_ports\n')
        f.write(f'set_db design:{self.cnfg.module_name} .dft_min_number_of_scan_chains 2\n')
        f.write(f'set_db design:{self.cnfg.module_name} .dft_mix_clock_edges_in_scan_chains true\n')
        f.write(f'connect_scan_chains -auto_create_chains -preview\n')
        f.write(f'connect_scan_chains -auto_create_chains\n')
        f.write(f'write_hdl > {self.path.opt_inc_snap}\n')
        f.write(f'report_scan_chain -summary\n')
        f.write(f'report_scan_registers -lockup\n')
        f.write(f'write_scandef > {self.path.scandef}\n')
        if (self.en.atpg):
            f.write("\n\n#ATPG Flow post synth \n")
            f.write(f'analyze_atpg_testability -library {self.path.lib}\n')
            f.write(f'write_dft_atpg -library {self.path.lib}\n')

    ###############################
    ##      Pre Synthesis 
    ##
    ################################ 

    def loadPreSynth(self, f):
        if (self.en.lp):
            self.loadPreSynthLP(f)
        if (self.en.ispc):
            self.loadPreSynthIspatial(f)
            self.loadCostGroup(f)
        if (self.en.scan):
            self.loadCostGroup(f)
            self.loadScanChainPreSynth(f)
 
    ###############################
    ##      Synthesis
    ##
    ################################ 

    def synGeneric(self, f):
        f.write(f'syn_generic {self.cmd.phy}\n')
        f.write(f'write_hdl > {self.path.gen_snap}\n')

    def synMap(self, f):
        f.write(f'syn_map {self.cmd.phy}\n')
        f.write(f'write_hdl > {self.path.map_snap}\n')

    def synOpt(self, f):
        if not self.en.scan:
            f.write(f'syn_opt {self.cmd.ispt}\n')
            f.write(f'write_hdl > {self.path.opt_snap}\n')

    def loadSynthesis(self, f):
        self.log_msg(f"LOG_INF: Synthesis Flow", "LOG_INF")
        f.write("\n\n#Synthesizing \n")
        self.synGeneric(f)
        self.synMap(f)
        self.loadMidLec(f)
        self.synOpt(f)

    ###############################
    ##      Pos Synthesis
    ##
    ################################ 

    def loadCGReports(self, f):
        f.write("\n\n#LP Report \n")
        f.write(f"report_clock_gates\n") 

    def loadPosSynth(self, f):
        if (self.en.lp):
            self.loadCGReports(f)
        if (self.en.scan):
            self.loadScanChainPosSynth(f)

    ###############################
    ##      LEC
    ##
    ################################ 

    def loadFinalLec(self, f):
        if self.en.lec:
            self.log_msg(f"LOG_INF: LEC configuration running", "LOG_INF")
            f.write("\n\n#LEC \n")
            f.write(f"write_do_lec -top {self.cnfg.module_name} -golden_design fv_map -revised_design fv_opt -flat -no_exit > {self.path.do_flec} \n")


    def loadMidLec(self, f):
        if self.en.lec:
            self.log_msg(f"LOG_INF: Generating mid Lec", "LOG_INF")
            f.write("\n\n#Post Map LEC \n")
            f.write(f"write_do_lec -top {self.cnfg.module_name} -golden_design rtl -revised_design fv_map -no_exit > {self.path.do_mlec} \n")


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
        if self.en.scan:
            f.write(f"report_scan_chains > {self.path.rpt_scan}\n")
            f.write(f"report_dft_violations > {self.path.rpt_dft_vltns}\n")

    ###############################
    ##      Close
    ##
    ################################

    def savePrj(self, f):
        f.write("\n\n#Save \n")
        if (self.en.ispc):
            f.write(f"write_db -common INVS -design {self.cnfg.module_name} {self.path.db} \n")
        else: 
            f.write(f"write_db -design {self.cnfg.module_name} {self.path.db} \n")
 
    def loadGUI(self, f):
        if (self.en.gui):
            f.write("\n\nGui \n")
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
    ##      Synth
    ##
    ################################ 

    def createSynthEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.genDefines(f)
        self.setEnv(f)
        self.loadIncludes(f)
        self.loadRTL(f)
        self.loadExt(f)
        self.loadNetlist(f)
        self.elabDesign(f)
        self.readSDC(f)
        self.checkTimingIntent(f)
        self.loadPreSynth(f)
        self.loadSynthesis(f)
        self.loadPosSynth(f)
        self.loadReports(f)
        self.loadFinalLec(f)
        self.writeSDC(f)
        self.writeSDF(f)
        self.savePrj(f)
        self.loadGUI(f)
        self.logfile.close()

