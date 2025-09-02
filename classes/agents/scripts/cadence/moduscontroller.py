# =============================================================================
# Project:        Logic on Rails
# File:           moduscontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        15 aug 2025
# Description:    controller for Modus 
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

class ModusController():

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
        self.en.dbg = (os.getenv('cadence_lp_syn') == "on")
        self.en.dft = (os.getenv('cadence_dft_syn') == "on")
        self.en.scan = (os.getenv('cadence_scanc_syn') == "on")
        self.en.atpg = (os.getenv('cadence_atpg_syn') == "on")
        self.en.logic = True

        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.path.log = os.getenv('modus_log_name')
        self.path.f = os.getenv('modus_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.sdc = os.getenv('source_sdc')
        self.path.lib = os.getenv('cadence_lib')
        self.path.mds = f' {self.cnfg.prj}/MODUS'
        self.path.assignpin = f' CHANGE_PATH_HERE'
        self.path.atpg_v = f'{self.path.rprt}/{self.cnfg.module_name}.modus.v'
        self.path.atpg_wgl = f'{self.path.rprt}/{self.cnfg.module_name}.modus.wgl'
        self.path.fvecors = f'{self.path.rprt}/{self.cnfg.module_name}.modus.result.final'

        self.defs.synth = os.getenv('synth_def')
        self.defs.eda_tool = f"MODUS"

        self.cmd.testmode = f' FULLSCAN'

    def genCommandVars(self):
        self.altera_ip_libs = ""
        self.cmd.net = ""
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
    ##         Build Model
    ##
    ################################

    def loadDef(self, f):
        self.log_msg(f"LOG_INF: Generating BuildModel", "LOG_INF")
        self.cmd.defs += f"{self.defs.synth.replace('+define+','').replace('+',' ').strip()}" 
        self.cmd.defs = f" -definemacro {self.cmd.defs.replace(' ',',').strip()}" 

    def loadRtl(self, f):
        if self.manifests["netlist"]:
            for each_netlist in self.manifests["netlist"].split():
                self.cmd.net += f'each_netlist:'
        else:
            self.log_msg(f"LOG_CRT: Warning, no netlist provided", "LOG_CRT")
            f.write("#NO NETLIST PROVIDED \n")

    def loadBuildModel(self, f):
        self.log_msg(f"LOG_INF: Generating BuildModel", "LOG_INF")
        self.loadRtl(f)
        self.loadDef(f)
        f.write("\n\n#Build model \n")
        f.write(f'build_model -workdir {self.path.mds} -cell {self.cnfg.module_name} {self.cmd.defs} -designsource {self.cmd.net} -techlib {self.path.lib} \n')

    ###############################
    ##         Test Model
    ##
    ################################
    
    def loadTestModel(self, f):
        self.log_msg(f"LOG_INF: Generating TestModel", "LOG_INF")
        f.write("\n\n#Test model \n")
        f.write(f'build_testmode -workdir {self.path.mds} -testmode {self.cmd.testmode} -assignfile {self.path.assignpin}\n')
        f.write(f'verify_test_structures -testmode {self.cmd.testmode} \n')


    ###############################
    ##         Fault Model
    ##
    ################################
    
    def loadFaultModel(self, f):
        if self.en.scan:
            self.log_msg(f"LOG_INF: Generating Fault Model", "LOG_INF")
            f.write("\n\n#Fault Model \n")
            f.write(f'build_faultmodel -workdir {self.path.mds} -fullfault yes\n')
            f.write(f'read_sdc -sdc {self.path.sdc} -testmode {self.cmd.testmode}\n')
            

    ###############################
    ##         Built Scan Model
    ##
    ################################

    def loadScanTests(self, f):
        if self.en.scan:
            self.log_msg(f"LOG_INF: Generating Scan Tests", "LOG_INF")
            f.write("\n\n#Scan tests Model \n")
            f.write(f'create_scanchain_tests -workdir {self.path.mds} -testmode {self.cmd.testmode} -experiment scan\n')

    ###############################
    ##         Built Scan Model
    ##
    ################################

    def loadATPG(self, f):
        if self.en.atpg:
            self.log_msg(f"LOG_INF: Generating ATPG Tests", "LOG_INF")
            f.write("\n\n#ATRPG  Model \n")
            f.write(f'create_logic_tests -workdir {self.path.mds} -testmode {self.cmd.testmode} -experiment logic -effort high\n')
            f.write(f'commit_tests -testmode {self.cmd.testmode} -inexperiment logic\n')

    ###############################
    ##         Vector Creation
    ##
    ################################

    def loadWriteVectors(self, f):
        self.log_msg(f"LOG_INF: Generating Vectors", "LOG_INF")
        f.write("\n\n#Vectors \n")
        if self.en.atpg:
            f.write(f'write_vectors -testmode {self.cmd.testmode} -language wgl -outputfilename {self.path.atpg_wgl}\n')
            f.write(f'write_vectors -testmode {self.cmd.testmode} -language verilog -testrange 1:100 -outputfilename {self.path.atpg_v}\n')
        f.write(f'write_vectors -workdir {self.path.mds} -testmode {self.cmd.testmode} -inexperiment logic -language verilog -scanformat serial -outputfilename {self.path.fvecors}\n')

    ###############################
    ##         Vector Creation
    ##
    ################################

    def loadReports(self, f):
        f.write("\n\n#Reports \n")
        if self.en.scan:
            f.write(f'report_chain -summary\n')
        f.write(f'reports_fault -testmode {self.cmd.testmode}\n')
        f.write(f'report_model_statistics -workdir {self.path.mds}\n')

    ###############################
    ##         GUI Creation
    ##
    ################################

    def loadGui(self, f):
        if self.en.gui:
            self.log_msg(f"LOG_INF: Load GUI", "LOG_INF")
            f.write("gui_open\n")

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
    ##         Gen Scripts
    ##
    ################################

    def createModusEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadBuildModel(f)
        self.loadTestModel(f)
        self.loadFaultModel(f)
        self.loadScanTests(f)
        self.loadATPG(f)
        self.loadWriteVectors(f)
        self.loadReports(f)
        self.loadGui(f)
        


        self.logfile.close()


