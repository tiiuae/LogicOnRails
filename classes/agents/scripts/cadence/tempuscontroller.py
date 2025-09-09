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

class TempusController():

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
        self.en.cov = (os.getenv('coverage') == "on")
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

        self.path.log = os.getenv('tempus_log_name')
        self.path.f = os.getenv('tempus_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.in_sdc = os.getenv('source_sdc')
        self.path.lib = os.getenv('cadence_lib')
        self.path.lef = os.getenv('cadence_lef')
        self.path.deff = os.getenv('cadence_def')
        self.path.saif = os.getenv('cadence_saif')
        self.path.cap = os.getenv('cadence_cap')
        self.path.spef = os.getenv('cadence_spef')
        self.path.qrc = os.getenv('cadence_qrc')
        self.path.cpf = os.getenv('cadence_cpf')

        self.path.db = "" f"{self.cnfg.prj}/INVS_DB/"

        self.path.rpt_time = f' {self.path.rprt}/{self.cnfg.module_name}.time.rpt'
        self.path.rpt_cov = f' {self.path.rprt}/{self.cnfg.module_name}.cov.rpt'
        self.path.rpt_para = f' {self.path.rprt}/{self.cnfg.module_name}.para.rpt'
        self.path.rpt_clk = f' {self.path.rprt}/{self.cnfg.module_name}.clk.rpt'
        self.path.rpt_inactives = f' {self.path.rprt}/{self.cnfg.module_name}.inactives.rpt'
        self.path.rpt_summary = f' {self.path.rprt}/{self.cnfg.module_name}.summary.rpt'
        self.path.rpt_gbaMax = f' {self.path.rprt}/{self.cnfg.module_name}.gbaMax.rpt'
        self.path.rpt_gbaMin = f' {self.path.rprt}/{self.cnfg.module_name}.gbaMin.rpt'



    def genCommandVars(self):
        self.altera_ip_libs = ""
        self.cmd.dsgn = ""
        self.cmd.ip = ""
        self.cmd.inc = ""
        self.cmd.gui = ""

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
    ##      Env Conf
    ##
    ################################

    def configEnv(self, f):
        self.log_msg(f"LOG_INF: Config environment", "LOG_INF")
        f.write(f"\n\n#Config Environment\n")
        f.write(f'set_multi_cpu_usage -local_cpu 1\n')
        f.write(f'set_table_style -no_frame_fix_width -nosplit\n')
        f.write(f'set_db timing_report_group_based_mode true\n')
        f.write(f'set_db timing_analysis_cppr both\n')

    ###############################
    ##      Read Libs
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

    def loadLef(self, f):
        if self.en.phy:
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

    def loadDesign(self, f):
        self.loadNetlist(f)

    ###############################
    ##      Init Design
    ##
    ################################ 

    def loadInitDesign(self, f):
        self.log_msg(f"LOG_INF: Init Design", "LOG_INF")
        f.write("\n\n#Init and init \n")
        f.write(f'init_design\n')

    ###############################
    ##      SPEF
    ##
    ################################ 

    def loadSPEF(self, f):
        if os.path.isfile(self.path.spef):
            self.log_msg(f"LOG_INF: Load SPEF", "LOG_INF")
            f.write("\n\n#SPEF \n")
            f.write(f'read_spef {self.path.spef}\n')
        else:
            self.log_msg(f"LOG_WRN: No SPEF file specified", "LOG_WRN")
            f.write("\n\n#ERROR no spef file specified \n")


    ###############################
    ##      SDC
    ##
    ################################ 

    def loadSDC(self, f):
        self.log_msg(f"LOG_INF: loading SDC file", "LOG_INF")
        f.write("\n\n#SDC \n")
        f.write(f'read_sdc -stop_on_errors {self.path.in_sdc}\n')


    ###############################
    ##      Reports
    ##
    ################################ 

    def loadTimingRprt(self,f):
        f.write(f'report_timing > {self.path.rpt_time}\n')

    def loadParasiticRprt(self,f):
        f.write(f'report_annotated_parasitics > {self.path.rpt_para}\n')

    def loadClkRprt(self,f):
        f.write(f'report_clocks > {self.path.rpt_clk}\n')

    def loadSummaryRprt(self,f):
        f.write(f'report_analysis_summary > {self.path.rpt_summary}\n')

    def loadInactvRprt(self,f):
        f.write(f'report_inactive_arcs > {self.path.rpt_inactives}\n')

    def loadGBAMaxRprt(self,f):
        f.write(f'report_timing -late   -max_paths 1 -nworst 1 -path_type full_clock -split_delay > {self.path.rpt_gbaMax}\n')

    def loadGBAMinRprt(self,f):
        f.write(f'report_timing -early  -max_paths 1 -nworst 1 -path_type full_clock -split_delay > {self.path.rpt_gbaMin}\n')

    def loadGBARprt(self,f):
        self.loadGBAMaxRprt(f)
        self.loadGBAMinRprt(f)

    def loadCovRprt(self,f):
        if self.en.cov:
            self.log_msg(f"LOG_INF: Generating coverage report", "LOG_INF")
            f.write("\n\n#Coverage Reports \n")
            f.write(f'report_analysis_coverage > {self.path.rpt_cov}\n')

    def loadRprt(self, f):
        self.log_msg(f"LOG_INF: Generating reports", "LOG_INF")
        f.write("\n\n#Reports \n")
        self.loadTimingRprt(f)
        self.loadParasiticRprt(f)
        self.loadClkRprt(f)
        self.loadSummaryRprt(f)
        self.loadInactvRprt(f)
        self.loadGBARprt(f)
        self.loadCovRprt(f)


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
    ##      Route
    ##
    ################################ 

    def createSTAEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.configEnv(f)
        self.loadLib(f)
        self.loadDesign(f)
        self.loadInitDesign(f)
        self.loadSPEF(f)
        self.loadSDC(f)
        self.loadRprt(f)
        self.loadGUI(f)
        self.logfile.close()

