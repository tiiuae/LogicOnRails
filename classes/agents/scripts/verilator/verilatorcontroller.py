# =============================================================================
# Project:        Logic on Rails
# File:           verilatorcontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    controller for Verilator 
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

class VerilatorController():

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
        self.verilator=SimpleNamespace()
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

        self.en.tb = (os.getenv('tb') == "on")
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
        self.lvl.msg = LogLevel[os.getenv('message_lvl')] if (os.getenv('message_lvl') != "") else 0 

        self.msg.cntnt = os.getenv('message_lvl')

        self.path.wave = os.getenv('wave')
        self.path.log = os.getenv('verilator_log_name')
        self.path.f = os.getenv('verilator_script_name')
        self.path.lint = os.getenv('verilator_lint_result')
        self.path.rprt = os.getenv('reports_path')

        self.verilator.opt = os.getenv('verilator_opt')

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        self.defs.tname = f"+define+DEFAULT_TEST=\"{os.getenv('default_test')}\""
        self.defs.eda_tool = f"+define+LINTING +define+VERILATOR_LINT"
        self.defs.msglvl = f"+define+MESSAGE_LEVEL={self.msg.cntnt}"

    def genCommandVars(self):
        self.altera_ip_libs = ""
        self.cmd.files = ""
        self.cmd.inc = ""
        self.cmd.defs = f"{self.defs.tname} {self.defs.eda_tool} {self.defs.msglvl} {os.getenv('synth_def').replace('+define+', ' +define+')} {os.getenv('sim_def').replace('+define+', ' +define+')}"

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
        manifests["bb"] = self.listFromFile("source_bb")
        return manifests
    
    ###############################
    ##      LOAD RTL
    ##
    ################################

    def loadFiles(self):
        self.log_msg(f"LOG_INF: Loading RTL files and BB", "LOG_INF", False)
        self.cmd.files = ""
        self.cmd.files += f"{' '.join(self.manifests['rtl'])} "
        self.cmd.files += f"{' '.join(self.manifests['bb'])} "
        self.cmd.files += f"{' '.join(self.manifests['tb'])} " if (self.en.tb) else ""
        self.cmd.files = ' '.join(t for t in self.cmd.files.split() if '.vhd' not in t.lower())

    def loadInc(self):
        if self.manifests["inc"]:
            self.log_msg(f"LOG_INF: Loading Includes", "LOG_INF")
            for each_inc in self.manifests["inc"]:
                self.cmd.inc += f" +incdir+{each_inc}"

    def loadUVM(self):
        if self.en.uvm:
            self.log_msg("LOG_WRN: UVM lint must have UVM_MACRO_PATH env variable set", "LOG_WRN")
            self.cmd.inc += f" +incdir+{os.getenv('UVM_MACRO_PATH')}"

    ###############################
    ##      REMOVE LINTOFFON
    ##
    ################################
    def toggle_prefix_between_markers(self, path, start, end, prefix, add):
        """
        Add or remove `prefix` at the start of each line strictly between lines
        containing `start` and `end` markers. Marker lines are never altered.
        One-pass streaming and atomic replace.
        """
        import os, tempfile
        fd, tmp = tempfile.mkstemp(text=True)
        if os.path.exists(path):
            with os.fdopen(fd, 'w', encoding='utf-8', newline='') as dst, \
                 open(path, 'r', encoding='utf-8', newline='') as src:
                in_blk = False
                for line in src:
                    s = (start in line)
                    e = (end in line)
                    if s:
                        in_blk = True
                    if in_blk and not (s or e):
                        if add and not line.startswith(prefix):
                            line = prefix + line
                        elif not add and line.startswith(prefix):
                            line = line[len(prefix):]
                    dst.write(line)
                    if e:
                        in_blk = False
            os.replace(tmp, path)    
        else:
            self.log_msg(f"LOG_ERR: File {path} does not exist", "LOG_ERR")

    
    def lint_off(self, file_name,
                 start_string="// framework lint_off",
                 end_string  ="// framework lint_on",
                 prefix      ="//"):
        """Comment-out lines between markers by adding `prefix` to each line."""
        self.toggle_prefix_between_markers(file_name, start_string, end_string, prefix, True)    
    

    def lint_on(self, file_name,
                start_string="// framework lint_off",
                end_string  ="// framework lint_on",
                prefix      ="//"):
        """Uncomment lines between markers by removing a single leading `prefix`."""
        self.toggle_prefix_between_markers(file_name, start_string, end_string, prefix, False) 

    
    def handleLintOnOff(self, func):
        self.log_msg(f"LOG_INF:Configuring lint off", "LOG_INF", False)
        for each_file in self.cmd.files.split():
                func(each_file)

    ###############################
    ##      LINT
    ##
    ################################ 

    def loadLint(self, f):
        self.log_msg(f"LOG_INF:Configuring linting command", "LOG_INF")
        f.write("\n\n#Linting\n")
        f.write(f"verilator {self.cmd.inc} --timing --error-limit 20 {self.cmd.defs} --lint-only {self.verilator.opt} {self.cmd.files} --top-module {self.cnfg.module_name} > {self.path.lint} 2>&1 \n")

    
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
        if os.path.exists(self.path.lint): 
            shutil.move(self.path.lint, f"{self.path.rprt}/{self.path.lint}")

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
                if trgtStr in line:
                    self.log_msg(self.msg_giveColor(line, lvl).replace("\n", ""), lvl, wr_file=False)

    def print_log_stateful(self, path,
                           warn_prefixes=("WARNING", "Warning", "%Warning"),
                           err_prefixes=("ERROR", "Error", "%Error"),
                           banner="- V e r i l a t i o n   R e p o r t"):
        # Enable ANSI on Windows if available
        try:
            import colorama
            colorama.just_fix_windows_console()
        except Exception:
            pass
        import sys
        RED, YEL, GRN, RST = "\x1b[31m", "\x1b[33m", "\x1b[32m", "\x1b[0m"
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            first = f.readline()
            if first == "":
                return
            # If banner present on first line → print everything green
            if banner in first:
                sys.stdout.write(GRN + first + RST)
                for line in f:
                    sys.stdout.write(GRN + line + RST)
                return
            # Otherwise: only red/yellow; non-matching lines keep previous color
            current = ""  # start with no color
            def emit(line):
                sys.stdout.write((current if current else "") + line + (RST if current else ""))
            # Handle first line
            if first.startswith(err_prefixes):
                current = RED
            elif first.startswith(warn_prefixes):
                current = YEL
            emit(first)
            # Stream remaining lines
            for line in f:
                if line.startswith(err_prefixes):
                    current = RED
                elif line.startswith(warn_prefixes):
                    current = YEL
                emit(line)



    def printLogs(self, rpt):
        if os.path.exists(rpt):
            self.print_log_stateful(rpt)
            #self.printLnIf(rpt, "LOG_WRN", "@W")
            #self.printLnIf(rpt, "LOG_CRT", "@N")
            #self.printLnIf(rpt, "LOG_ERR", "Error:")
        else:
            self.log_msg(f"LOG_ERR: Report path {rpt} does not exist", "LOG_ERR", wr_file=False)



    ###############################
    ##      MAIN
    ##
    ################################ 

    def createLintEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadFiles()
        self.loadInc()
        self.loadUVM()
        self.handleLintOnOff(self.lint_off)
        self.loadLint(f)
        self.logfile.close()
        
    def postLintHandle(self):
        self.loadFiles()
        self.handleLintOnOff(self.lint_on)

