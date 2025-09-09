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
        self.path.qrc = os.getenv('cadence_qrc')
        self.path.cpf = os.getenv('cadence_cpf')

        self.path.oa_db = "" # <=
        self.path.cts = "" # <=
        self.path.iopad = "" # <=
        self.path.igds = "" # <=
        self.path.ogds = "" # <=
        self.path.db = "" f"{self.cnfg.prj}/INVS_DB/"


        self.path.rpt_time = f' {self.path.rprt}/{self.cnfg.module_name}.time.rpt'
        self.path.rpt_area = f' {self.path.rprt}/{self.cnfg.module_name}.area.rpt'
        self.path.rpt_power = f' {self.path.rprt}/{self.cnfg.module_name}.pwr.rpt'
        self.path.rpt_clocks = f' {self.path.rprt}/{self.cnfg.module_name}.clks.rpt'
        self.path.rpt_hierarchy = f' {self.path.rprt}/{self.cnfg.module_name}.hier.rpt'
        self.path.rpt_summary = f' {self.path.rprt}/{self.cnfg.module_name}.summary.rpt'


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

    def savePrj(self, f):
        f.write("\n\n#Save \n")
        if (self.en.ispc):
            f.write(f"write_db -common INVS -design {self.cnfg.module_name} >  {self.path.db} \n")
        else: 
            f.write(f"write_db >  {self.path.db} \n")
 
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



    ###############################
    ##      Route
    ##
    ################################ 

    def createSynthEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")

        self.logfile.close()

