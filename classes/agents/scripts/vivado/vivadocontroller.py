# =============================================================================
# Project:        Logic on Rails
# File:           vivadocontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    controller for Vivado 
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

class  VivadoController():

    ###############################
    ##         CONSTRUCTOR
    ##
    ################################
    def __init__(self):
        self.en=SimpleNamespace()
        self.xlnx=SimpleNamespace()
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
    ##         BUILD VARS
    ##
    ################################
    def genConstants(self):

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

        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.msg.cntnt = os.getenv('message_lvl')

        self.path.prj = os.getenv('prj_path')
        self.path.fprj = f"{self.path.prj}/{self.cnfg.module_name}.xpr"
        self.path.wave = os.getenv('wave')
        self.path.log = os.getenv('vivado_log_name')
        self.path.f = os.getenv('vivado_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.xdc = os.getenv('vivado_xdc')
        self.path.sdc = os.getenv('source_sdc')
        self.path.pin = os.getenv('source_pins')
        self.path.rpt_time = f"{self.path.rprt}/{self.cnfg.module_name}.time.rpt"
        self.path.bit = f"{self.path.prj}/{self.cnfg.module_name}.bit"

        self.xlnx.dev = os.getenv('vivado_device')
        self.xlnx.opt_synt = os.getenv('vivado_synth_opt')
        self.xlnx.opt_rout = os.getenv('vivado_pr_opt')
        self.xlnx.opt_sim = os.getenv('vivado_sim_opt')
        self.xlnx.opt_sta = os.getenv('vivado_sta_opt')
        self.xlnx.opt_bit = os.getenv('vivado_bit_bit')

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        self.defs.tname = f" DEFAULT_TEST=\\\"{os.getenv('default_test')}\\\""
        self.defs.eda_tool = f" VIVADO "
        self.defs.msglvl = f" MESSAGE_LEVEL={self.msg.cntnt}"

    def genCommandVars(self):
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
        self.cmd.acc = ""
        self.cmd.wave = ""
        self.cmd.defs = f"{self.defs.tname} {self.defs.eda_tool} {self.defs.msglvl}"

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


    ##################################################################
    ##      Create
    ##
    ################################################################## 
    
    def createPrjEnv(self, f):
        self.log_msg(f"LOG_INF: Generating initial vivado creation command", "LOG_INF")
        f.write("\n\n#Command Creation \n")
        f.write(f"create_project -part {self.xlnx.dev} {self.cnfg.module_name} {self.path.prj} \n")

    ###############################
    ##      EXT
    ##
    ################################ 

    def loadExt(self, f):
        if (self.en.ext):
            self.log_msg(f"LOG_INF: load ext vp files", "LOG_INF")
            self.cmd.ext = " ".join(self.manifests["enc_lib"])
            f.write(f"\n\n#load ext files\n")
            f.write(f"add_files -norecurse {self.cmd.ext}\n")


    ###############################
    ##      RTL
    ##
    ################################ 

    def loadRTL(self, f):
        self.log_msg(f"LOG_INF: load rtl files", "LOG_INF")
        self.cmd.rtl = " ".join(self.manifests["rtl"])
        f.write(f"\n\n#load rtl files\n")
        f.write(f"add_files -norecurse {self.cmd.rtl}\n")
        f.write(f"set obj [get_filesets sources_1]\n")

    ###############################
    ##      Defines
    ##
    ################################ 
    
    def loadDefs(self, f):
        self.log_msg(f"LOG_INF: configuring defines", "LOG_INF")
        self.cmd.defs += f" {self.defs.synth.replace('+define+','  ').replace('+',' ').strip()}"
        self.cmd.defs = self.cmd.defs.split()
        f.write(f"\n\n#Generating defines\n")
        for each_define in self.cmd.defs:
            f.write(f'set_property -name "verilog_define" -value {each_define} -objects $obj\n')


    def setTop(self, f):
        self.log_msg(f"LOG_INF: set top level", "LOG_INF")
        f.write(f"\n\n#Set toplevel\n")
        f.write(f'set_property -name "top" -value {self.cnfg.module_name} -objects $obj\n')

    ###############################
    ##      load IPS
    ##
    ################################ 

    def loadIPs(self, f):
        if self.manifests["ips"]: 
            ip_path = " ".join(v[len("XILINX:"):] for v in self.manifests["ips"] if v.startswith("XILINX:"))                
            if ip_path:
                self.log_msg(f"LOG_INF: loading ips", "LOG_INF")
                f.write(f"\n\n#IP flow\n")
                for each_ip in ip_path.split():
                    if each_ip.endswith(".tcl"):
                        f.write(f"source {each_ip}\n")
                    elif each_ip.endswith(".xci"):
                        f.write(f'read_ip "{each_ip}.xci"\n')
                        f.write(f'generate_target all [ get_files "{each_ip}.xci" ]"\n')

    ###############################
    ##      TB
    ##
    ################################ 

    def loadTb(self, f):
        self.log_msg(f"LOG_INF: load tb files", "LOG_INF")
        self.cmd.tb = " ".join(self.manifests["tb"])
        f.write(f"\n\n#load tb files\n")
        f.write(f"add_files -fileset sim_1 {self.cmd.tb}\n")
        f.write(f"set_property top {self.cnfg.tb_top} [current_fileset -simset]\n")
        f.write(f"update_compile_order -fileset sources_1\n")

    ###############################
    ##      XDC
    ##
    ################################ 
    
    def genXDC(self, x):
        if os.path.exists(self.path.pin):
            with open(self.path.pin, 'r', encoding='utf-8') as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith('#'):
                        continue
                    col = [p.strip() for p in ln.split(';')]
                    if len(col) < 5:
                        self.log_msg(f"LOG_ERR: Error, pin file has less then 5 columns", "LOG_ERR")        
                        break
                    pname, pstd, ploc, pdir, pvendor = col[:5]
                    if pvendor.lower() == 'xilinx':
                        x.write(f"set_property PACKAGE_PIN {ploc} [get_ports {{{pname}}}]\n")
                        x.write(f"set_property IOSTANDARD {pstd} [get_ports {{{pname}}}]\n")
        else:
            self.log_msg(f"LOG_CRT: No PIN found while generating xdc", "LOG_CRT")        

    def appendSDC(self, x):
        try:
            with open(self.path.sdc, 'r', encoding='utf-8') as s:
                x.write("\n# ---- SDC content ----\n")
                x.write(s.read())
        except FileNotFoundError:
            self.log_msg(f"LOG_CRT: No SDC found while generating xdc", "LOG_CRT")        
            x.write("\n# (No SDC file found to append.)\n")


    def loadXDC(self, f):
        self.log_msg(f"LOG_INF: load xdc file", "LOG_INF")
        if os.path.exists(self.path.xdc):
            self.log_msg(f"LOG_WRN: running with existing xdc", "LOG_WRN")        
        else:
            x = open(self.path.xdc, 'w', encoding='utf-8', newline='\n')
            self.genXDC(x)
            self.appendSDC(x)
            x.close()
        self.cmd.tb = " ".join(self.manifests["tb"])
        f.write(f"\n\n#XDC files\n")
        f.write(f"read_xdc {self.path.xdc}\n")


    ######################################################################################
    ##      SIM
    ##
    ######################################################################################

    def loadDPI(self, f):
        if self.en.sw:
            dpi_code = " ".join(v[len("DPI:"):] for v in self.manifests["soft"] if v.startswith("DPI:"))
            dpi_c = [f for f in dpi_c if f.endswith(".c")]
            self.log_msg(f"LOG_INF: Loading DPI", "LOG_INF")
            f.write(f"\n\n#DPI Flow\n")
            f.write(f"exec xsc {dpi_c}\n")


    def loadAcc(self, f):
        if self.en.acc:
            self.cmd.acc += f"all"

    def loadLaunchSim(self, f):
        sim_def = f" {self.defs.sim.replace('+define+','  ').replace('+',' ').strip()}"
        self.log_msg(f"LOG_INF: Generating Sim Commands", "LOG_INF")
        f.write(f"\n\n#Running Sim\n")
        f.write(f"set sim_fs [get_filesets sim_1]\n")
        for each_def in sim_def.split():
            f.write(f'set_property -name "verilog_define" -valu {each_def} -objects $sim_fs\n')
        f.write(f"update_compile_order -fileset $sim_fs\n")
        f.write(f"launch_simulation\n")
        if (self.en.gui):
            f.write(f"open_wave_config {self.path.wave}\n")
            f.write(f"start_gui\n")

    def loadSim(self, f):
        self.loadAcc(f)
        self.loadDPI(f)
        self.loadLaunchSim(f)


    ###############################
    ##      PRJ HANDLE
    ##
    ################################ 

    def handleClose(self, f):
        self.log_msg(f"LOG_INF: final adjusts", "LOG_INF")
        f.write(f"\n\n#Save prj\n")
        f.write(f"close_project\n")

    ###############################
    ##      POST SCRIPT
    ##
    ################################ 

    def cleanEnv(self):
        if os.path.exists("vivado.log"): 
            if (self.en.log):
                shutil.move("vivado.log", f"{self.path.rprt}/vivado.log")
            else:
                if not self.en.keep : os.remove("vivado.log")
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
    
    def printLnIf(self, trgtFile, lvl, trgtStr):
        if (int(LogLevel[lvl]) >= int(self.lvl.msg) ):            
            if (lvl == "LOG_WRN"):
                    self.log_msg(f"LOG_WRN: SHOWING WARNINGS", "LOG_WRN", wr_file=False)
            elif (lvl == "LOG_CRT"):
                    self.log_msg(f"LOG_CRT: SHOWING CRITICAL WARNINGS", "LOG_CRT", wr_file=False)
            elif (lvl == "LOG_ERR"):
                    self.log_msg(f"LOG_ERR: SHOWING ERRORS", "LOG_ERR", wr_file=False)
            f = open(trgtFile, "r")
            for line in f:
                if line.startswith(trgtStr):
                    self.log_msg(self.msg_giveColor(line, lvl).replace("\n", ""), lvl, wr_file=False)
                    
    def printLogs(self, rpt):
        if (self.en.log):
            if os.path.exists(rpt):
                self.printLnIf(rpt, "LOG_WRN", "WARNING:")
                self.printLnIf(rpt, "LOG_CRT", "CRITICAL WARNING:")
                self.printLnIf(rpt, "LOG_ERR", "ERROR:")
            else:
                self.log_msg(f"LOG_ERR: Report path {rpt} does not exist", "LOG_ERR", wr_file=False)

    ###############################
    ##      OPEN CLOSE
    ##
    ################################ 

    def openPrj(self, f):
        self.log_msg(f"LOG_INF: Open Project", "LOG_INF")
        f.write(f"\n\n#Open Project\n")
        f.write(f"open_project {self.path.fprj}\n")


    ###############################
    ##      SYNTH ROUTE STA BIT
    ##
    ################################

    def loadSynth(self, f):
        self.log_msg(f"LOG_INF: Load Synthesis  on synth_1", "LOG_INF")
        f.write(f"\n\n#Synthesize \n")
        f.write(f"reset_run synth_1\n")
        f.write(f"launch_runs {self.xlnx.opt_synt} synth_1\n")
        f.write(f"wait_on_run synth_1\n")
    
    def loadPlaceRoute(self, f):
        self.log_msg(f"LOG_INF: Load PR on impl_1", "LOG_INF")
        f.write(f"\n\n#Place and Route\n")
        f.write(f"reset_run impl_1\n")
        f.write(f"launch_runs {self.xlnx.opt_rout} impl_1\n")
        f.write(f"wait_on_run impl_1\n")

    def loadSTA(self, f):
        self.log_msg(f"LOG_INF: Load STA", "LOG_INF")
        f.write(f"\n\n#Synthesize\n")
        f.write(f"open_run impl_1\n")
        f.write(f"report_timing_summary {self.xlnx.opt_sta} -file {self.path.rpt_time}\n")

    def loadBitStream(self, f):
        self.log_msg(f"LOG_INF: Load STA", "LOG_INF")
        f.write(f"\n\n#Synthesize\n")
        f.write(f"open_run impl_1\n")
        f.write(f"write_bitstream {self.xlnx.opt_bit} -force {self.path.bit}\n")

    ###############################
    ##      MAIN
    ##
    ################################ 

    def createPrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.createPrjEnv(f)
        self.loadRTL(f)
        self.loadExt(f)
        self.loadDefs(f)
        self.setTop(f)      
        self.loadIPs(f)    
        self.loadTb(f)        
        self.loadXDC(f)  
        self.handleClose(f)      
        self.logfile.close()

    def createSynth(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.openPrj(f)
        self.loadSynth(f)
        self.handleClose(f)
        self.logfile.close()

    def createPlaceRoute(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.openPrj(f)
        self.loadPlaceRoute(f)
        self.handleClose(f)
        self.logfile.close()

    def createSim(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.openPrj(f)
        self.loadSim(f)
        self.logfile.close()


    def createSTA(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.openPrj(f)
        self.loadSTA(f)
        self.handleClose(f)
        self.logfile.close()

    def createBitStream(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.openPrj(f)
        self.loadBitStream(f)
        self.handleClose(f)
        self.logfile.close()
