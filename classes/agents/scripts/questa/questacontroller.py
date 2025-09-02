# =============================================================================
# Project:        Logic on Rails
# File:           questacontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    controller for Questa 
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

class QuestaController():

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
        self.cnfg.tb_top = os.getenv('tb')
        self.cnfg.usr_opt = os.getenv('cadence_sim_opt')

        self.en.cov = (os.getenv('coverage') == "on")
        self.en.gui = (os.getenv('gui') == "on")
        self.en.uvm = (os.getenv('uvm') == "on")
        self.en.sw = (os.getenv('dpi') == "on")
        self.en.ext = (os.getenv('ext_modules') == "on")
        self.en.log = (os.getenv('log') == "on")
        self.en.acc = (os.getenv('access') == "on")
        self.en.keep = (os.getenv('keep') == "on")
        self.en.lint_tb = (self.cnfg.tb_top == "on")

        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.msg.cntnt = os.getenv('message_lvl')

        self.path.wave = os.getenv('wave')
        self.path.log = os.getenv('questa_log_name')
        self.path.f = os.getenv('questa_script_name')
        self.path.lint = os.getenv('questa_lint_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.cov = f"{self.path.rprt}/{self.cnfg.module_name}.ucdb"

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        
        self.defs.tname = f"+define+DEFAULT_TEST=\"{os.getenv('default_test')}\""
        self.defs.eda_tool = f"+define+SIMULATION +define+QUESTA"
        self.defs.msglvl = f"+define+MESSAGE_LEVEL={self.msg.cntnt}"

    def genCommandVars(self):
        self.altera_ip_libs = ""
        self.cmd.rtl = ""
        self.cmd.ext = ""
        self.cmd.tb = ""
        self.cmd.ip = ""
        self.cmd.acc = ""
        self.cmd.inc = ""
        self.cmd.pli = ""
        self.cmd.dpi = ""
        self.cmd.vpi = ""
        self.cmd.uvm = ""
        self.cmd.soft = ""
        self.cmd.cov = ""
        self.cmd.gui = ""
        self.cmd.wave = ""
        self.cmd.defs = f"{self.defs.tname} {self.defs.eda_tool} {self.defs.msglvl} {os.getenv('synth_def')} {os.getenv('sim_def')}"

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
    ##       Config 
    ##
    ################################ 

    def setOnErr(self, f):
        if not (self.en.gui):
            f.write("\n\n#On Error Flow\n")
            f.write("onerror { quit -f 1 }\n")


    def configAcc(self):
        if not (self.lvl.acc == "off"):
            self.cmd.acc += "+acc"
        if self.en.gui:
            self.cmd.gui += "-gui"

    def configCov(self):
        if(self.en.cov):
            self.cmd.cov = f' -coveropt 3 +cover -coverage -c -do "run -all; coverage save -onexit -directive -codeAll {self.path.cov}; quit -f"'


    ###############################
    ##       RTL 
    ##
    ################################ 

    def configInc(self):
        if self.manifests["inc"]:
            self.log_msg(f"LOG_INF: Adding include paths ", "LOG_INF")
            for each_include in self.manifests["inc"]:
                self.cmd.inc += f' +incdir+{each_include}'

    def configRTL(self):
        if self.manifests["rtl"]:
            self.log_msg(f"LOG_INF: loading rtl files ", "LOG_INF")
            for each_rtl in self.manifests["rtl"]:
                self.cmd.rtl += f" {each_rtl}"
        else:
            self.log_msg(f"LOG_CRT: No rtl file found in manifest ", "LOG_CRT")
        if self.manifests["tb"]:
            self.log_msg(f"LOG_INF: loading tb files ", "LOG_INF")
            for each_tb in self.manifests["tb"]:
                self.cmd.tb += f" {each_tb}"
        else:
            self.log_msg(f"LOG_CRT: No tb file found in manifest ", "LOG_CRT")

    ###############################
    ##      EXT
    ##
    ################################ 
    
    def loadExtCompiled(self):
        if self.manifests["comp_lib"]:
            for each_compIp in self.manifests["comp_lib"]:
                self.log_msg(f"LOG_INF: generating external compiled ip {each_compIp}", "LOG_INF")
                each_compIp = each_compIp.replace("QUESTA:", "")
                if not (":" in each_compIp):
                    self.log_msg(f"LOG_INF: {each_compIp} added to ip list", "LOG_INF")
                    self.cmd.ip += f'-L {offset_path}{each_compIp} '
        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_lib manifest", "LOG_WRN")

    def loadExtRtl(self):
        if self.manifests["enc_lib"]:
            for each_rtlIp in self.manifests["enc_lib"]:
                self.cmd.ext += f"{each_rtlIp} "
        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_ip manifest",  "LOG_WRN")

    def configExt(self):
        if (self.en.ext):
            self.loadExtCompiled()
            self.loadExtRtl()


    ###############################
    ##      DPI
    ##
    ################################ 

    def configDPI(self, f):
        if (self.en.sw):
            if self.manifests["soft"]:
                for each_soft in self.manifests["soft"]:
                    each_dpif = each_soft.replace("DPI:", "")
                    if not (":" in each_dpif):
                        self.log_msg(f"LOG_INF: adding DPI functions {each_dpif}", "LOG_INF")
                        filename = os.path.basename(each_dpif)
                        filename = filename.replace(".", "_")
                        os.environ[filename]  = f'{each_dpif}.exe '   
                        if (".h" in each_dpif):
                            self.cmd.dpi += f' {os.getenv("dpi_opt")} {each_dpif}'
                        else:
                            self.cmd.dpi += f' {each_dpif}'
                if not (self.cmd.dpi == ""):
                    f.write("\n\n#DPI Flow\n")
                    f.write(f"vlog -sv {self.cmd.dpi} {self.ext_usr_vlog_opt}\n")
        else:
            self.log_msg("LOG_CRT: software run enabled in modelsim but no .c function in software manifest", "LOG_CRT")


    ###############################
    ##      VPI
    ##
    ################################ 

    def configVPI(self, f):
        if (self.en.sw):
            if self.manifests["soft"]:
                f.write("\n\n#VPI Flow\n")
                for each_soft in self.manifests["soft"]:
                    each_vpif = each_soft.replace("VPI:", "")
                    if not (":" in each_vpif):
                        self.log_msg("LOG_WRN: VPI code must have MODELSIM_PATH/QUESTA_PATH env variable set", "LOG_WRN")
                        f.write(f"gcc -m64 -fPIC -shared {each_vpif} -o {each_vpif}.so -I{os.getenv('MODELSIM_PATH')}/include\n")
                        self.cmd.vpi += f" -pli {each_vpif}.so"


    ###############################
    ##      RUN
    ##
    ################################ 

    def configRun(self, f):
        simfiles = f"{self.cmd.rtl} {self.cmd.tb} {self.cmd.inc} {self.cmd.ext} {self.cmd.ip} {self.cmd.vpi} {self.cmd.dpi}"
        simopts = f"{self.cmd.acc} {self.cmd.gui}"
        self.log_msg(f"LOG_INF: Generating qrun command ", "LOG_INF")
        f.write("\n\n#Loading top level\n")
        f.write(f'set TOP_LEVEL_NAME {self.cnfg.tb_top}')
        f.write("\n\n#qrun = vlog/vcom + vopt + vsim \n")
        f.write(f'qrun -top {self.cnfg.tb_top} {simopts} {self.cmd.defs} {simfiles} +test={os.getenv("default_test")} {self.cmd.cov}\n')


    ###############################
    ##      GUI
    ##
    ################################ 

    def configGUI(self,f):
        self.log_msg("LOG_INF: generating run and cov commands", "LOG_INF")
        f.write("\n\n#Run modelsim sim\n")
        if (self.en.gui):
            if (self.lvl.acc == "on"):
                f.write(f"log -r /*\n") 
            f.write(f"do {self.path.wave}\n")
            f.write(f"run -all\n")
        else:
            if (self.en.cov):
                f.write(f"vcover report -html -output reports/coverage -annotate -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90 {self.path.cov}\n")
                f.write(f"vcover report -output reports/coverage.txt -annotate -details -assert -directive -cvg -code bcefst {self.path.cov}\n")

            f.write(f"exit\n")

    ###############################
    ##      POST
    ##
    ################################ 

    def cleanEnv(self):
        if os.path.exists("simlib") and not self.en.keep : shutil.rmtree("simlib")
        if os.path.exists("work") and not self.en.keep: shutil.rmtree("work")
        
        if os.path.exists("qrun.log"): 
            if (self.en.log):
                shutil.move("qrun.log", f"{self.path.rprt}/{self.cnfg.module_name}.qrun.log.rpt")
            else:
               if not (self.en.keep): os.remove("qrun.log")
        
        if os.path.exists("transcript"): 
            if (self.en.log):
                shutil.move("transcript", f"{self.path.rprt}/{self.cnfg.module_name}.transcript.rpt")
            else:
               if not (self.en.keep): os.remove("transcript")
        
        if os.path.exists(self.path.f): 
            if (self.en.log):
                shutil.move(self.path.f, f"{self.path.rprt}/{self.path.f}")
            else:
                if not (self.en.keep): os.remove(self.path.f)
        
        if os.path.exists(self.path.log): 
            if (self.en.log):
                shutil.move(self.path.log, f"{self.path.rprt}/{self.path.log}")
            else:
                if not (self.en.keep): os.remove(self.path.log)

    def printLogs(self):
        if (self.en.log):
            print(f"{GREEN}INFO:Displaying compilation {YELLOW}CRITICAL WARNING\n")
            os.system(f'grep "** Warning:" {self.path.rprt}/{self.cnfg.module_name}.transcript.rpt')
            print(f"{GREEN}INFO:Displaying compilation {RED}ERRORS\n")
            os.system(f'grep "** Error" {self.path.rprt}/{self.cnfg.module_name}.transcript.rpt')
            print(ENDCOLOR)


    ###############################
    ##      MAIN
    ##
    ################################ 

    def createSimEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.configAcc()
        self.configCov()
        self.setOnErr(f)
        self.configInc()
        self.configRTL()
        self.configExt()
        self.configDPI(f)
        self.configVPI(f)
        self.configRun(f)
        self.configGUI(f)
        self.logfile.close()
        

