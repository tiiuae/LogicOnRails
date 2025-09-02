# =============================================================================
# Project:        Logic on Rails
# File:           quartuscontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        15 aug 2025
# Description:    controller for quartus 
# =============================================================================

import subprocess
import os
import inspect
import shutil
import csv
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

class  QuartusController():

    ###############################
    ##         CONSTRUCTOR
    ##
    ################################
    def __init__(self):
        self.en=SimpleNamespace()
        self.quartus=SimpleNamespace()
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
        self.en.uproc = (os.getenv('uproc') == "on")
        self.en.ext = (os.getenv('ext_modules') == "on")
        self.en.log = (os.getenv('log') == "on")
        self.en.acc = (os.getenv('access') == "on")
        self.en.keep = (os.getenv('keep') == "on")
        self.en.pdcovr = (os.getenv('libero_pdc_oride') == "on")

        self.lvl.acc = os.getenv('access')
        self.lvl.msg = LogLevel[os.getenv('message_lvl')]

        self.msg.cntnt = os.getenv('message_lvl')

        self.path.prj = f"{os.getenv('prj_path')}/{self.cnfg.module_name}"
        self.path.fprj = f"{self.path.prj}/{self.cnfg.module_name}.qsf"
        self.path.log = os.getenv('quartus_log_name')
        self.path.f = os.getenv('quartus_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.constr = os.getenv('prj_constraint')
        self.path.sdc = os.getenv('source_sdc')
        self.path.pin = os.getenv('source_pins')
        self.path.qextcnf = os.getenv('quartus_config')
        self.path.partition = os.getenv('quartus_part')
        self.path.sigtap = os.getenv('quartus_stp')

        self.quartus.fam = os.getenv('quartus_family')
        self.quartus.ver = os.getenv('quartus_version')
        self.quartus.dev = os.getenv('quartus_device')

        self.quartus.opt_synt = os.getenv('quartus_synth_opt')
        self.quartus.opt_rout = os.getenv('quartus_pr_opt')
        self.quartus.opt_sim = os.getenv('quartus_sim_opt')
        self.quartus.opt_sta = os.getenv('quartus_sta_opt')
        self.quartus.opt_bit = os.getenv('quartus_bit_bit')

        self.defs.synth = os.getenv('synth_def')
        self.defs.eda_tool = f" QUARTUS "
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
        self.cmd.fppdc = ""
        self.cmd.iopdc = ""
        self.cmd.defs = f"{self.defs.synth} {self.defs.eda_tool} {self.defs.msglvl}"

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

    ###############################
    ##      CREATE PRJ
    ##
    ################################ 

    def loadPrjInfo(self, f):
        self.log_msg(f"LOG_INF: creating project", "LOG_INF")
        f.write(f"\n\n#generate project\n")
        f.write(f"project_new {self.path.prj}\n")
        f.write(f"set_global_assignment -name ORIGINAL_QUARTUS_VERSION {self.quartus.ver}\n")
        f.write(f"set_global_assignment -name DEVICE {self.quartus.dev}\n")
        f.write(f"set_global_assignment -name FAMILY {self.quartus.fam}\n")

    ###############################
    ##      CREATE DEFS
    ##
    ################################ 

    def loadDef(self, f):
        self.log_msg(f"LOG_INF: load defines", "LOG_INF")
        self.cmd.defs = self.cmd.defs.replace("+define+", "").replace("+", "").strip()
        if self.cmd.defs:
            f.write(f"\n\n#generate project\n")
            for each_def in self.cmd.defs.split():
                f.write(f'set_global_assignment -name VERILOG_MACRO "{each_def}"\n')
    
    ###############################
    ##      CREATE INC
    ##
    ################################ 

    def loadInc(self, f):
        if self.manifests["inc"]:
            self.log_msg(f"LOG_INF: load includes", "LOG_INF")
            f.write(f"\n\n#search for includes\n")
            for each_inc in self.manifests["inc"]:
                f.write(f'set_global_assignment -name SEARCH_PATH ../{each_inc}\n')


    ###############################
    ##      LOAD RTL
    ##
    ################################ 

    def loadRTL(self, f):
        if self.manifests["rtl"]:
            self.log_msg(f"LOG_INF: loading rtl", "LOG_INF")
            f.write(f"\n\n#load rtl\n")
            for each_rtl in self.manifests["rtl"]:
                if (".sv" in each_rtl):
                    ftype = f"SYSTEMVERILOG_FILE"
                elif (".v" in each_rtl):
                    ftype = f"VERILOG_FILE"
                else:
                    ftype = f"VHDL_FILE"
                f.write(f'set_global_assignment -name {ftype} ../{each_rtl}\n')
        else:
            self.log_msg(f"LOG_CRT: no rtl defined in rtl manifest", "LOG_CRT")

    def loadEXT(self, f):
        if self.en.ext:
            if self.manifests["enc_lib"]:
                self.log_msg(f"LOG_INF: loading external files", "LOG_INF")
                f.write(f"\n\n#load ext\n")
                for each_ext in self.manifests["enc_lib"]:
                    if (".vp" in each_ext):
                        ftype = f"SYSTEMVERILOG_FILE"
                    elif (".v" in each_ext):
                        ftype = f"VERILOG_FILE"
                    else:
                        ftype = f"SYSTEMVERILOG_FILE"
                    f.write(f'set_global_assignment -name {ftype} ../{each_ext}\n')
            else:
                self.log_msg(f"LOG_CRT: no rtl defined in ext manifest", "LOG_CRT")

    ###############################
    ##      IP
    ##
    ################################ 

    def loadIP (self, f):
        if self.manifests["ips"]:
            ip_path = " ".join(v[len("ALTERA:"):] for v in self.manifests["ips"] if v.startswith("ALTERA:"))
            if ip_path:
                self.log_msg(f"LOG_INF: loading ips", "LOG_INF")
                f.write(f"\n\n#IP flow\n")
                for each_ip in ip_path.split():
                    if each_ip.endswith(".qsys"):
                        f.write(f"set_global_assignment -name QSYS_FILE ../{each_ip}\n")
                    else:
                        f.write(f"set_global_assignment -name IP_FILE ../{each_ip}\n")

    ###############################
    ##      MAIN
    ##
    ################################ 

    def loadExtCnfg(self, f):
        if os.path.exists(self.path.qextcnf):
            self.log_msg(f"LOG_INF: loading external configs", "LOG_INF")
            with open(self.path.qextcnf, 'r') as file:
                content = file.read()
                f.write(f"\n\n#external configuration\n")
                f.write(content)
        else:
            self.log_msg(f"LOG_CRT: no extra configuration file for quartus in constraint path", "LOG_CRT")

    ###############################
    ##      SDC
    ##
    ################################

    def loadSDC(self, f):
        self.log_msg(f"LOG_INF: loading sdc file", "LOG_INF")
        f.write(f"\n\n#SDC file\n")
        f.write(f"set_global_assignment -name SDC_FILE ../{self.path.sdc}")

    ###############################
    ##      SIGNAL TAP
    ##
    ################################

    def loadSigTap(self, f):
        if os.path.exists(self.path.sigtap):
            self.log_msg(f"LOG_INF: loading signaltap file", "LOG_INF")
            f.write(f"\n\n#SignalTap file\n")
            f.write(f"set_global_assignment -name ENABLE_SIGNALTAP ON\n")
            f.write(f"set_global_assignment -name USE_SIGNALTAP_FILE ../{self.path.sigtap}\n")
            f.write(f"set_global_assignment -name SIGNALTAP_FILE ../{self.path.sigtap}\n")
        else:
            self.log_msg(f"LOG_WRN: no signal tap file", "LOG_WRN")

    ###############################
    ##      PARTITION
    ##
    ################################ 

    def loadPartition(self, f):
        if os.path.exists(self.path.partition):
            self.log_msg(f"LOG_INF: loading logic partition csv style file", "LOG_INF")
            self.log_msg(f"LOG_WRN: partitions must follow the name partition nam .qdb/syn.qdb/pr.qdb", "LOG_WRN")
            f.write(f"\n\n#Logic Partition file\n")
            with open(self.path.partition, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                for row in csv_reader:
                    if not row or row[0].startswith('#'):
                        continue   
                    if ("altera" in row[3].lower()):
                        part_name = row[0]
                        part_hier = row[1].replace(".", "|")
                        part_entity = row[2]
                        part_dump_path = row[8]   
                        f.write(f"set_instance_assignment -name PARTITION {part_name} -to {part_hier} -entity {part_entity}\n")
                        if ("true" in row[4].lower()):
                            part_load_path = row[5]
                            f.write(f"set_instance_assignment -name QDB_FILE_PARTITION {part_load_path}/{part_name}.qdb -to {part_hier} -entity {part_entity}\n")
                        if ("true" in row[6].lower()):
                            f.write(f"set_instance_assignment -name EXPORT_PARTITION_SNAPSHOT_SYNTHESIZED {part_dump_path}/{part_name}.syn.qdb -to {part_hier} -entity {part_entity}\n")
                        if ("true" in row[7].lower()):
                            f.write(f"set_instance_assignment -name EXPORT_PARTITION_SNAPSHOT_SYNTHESIZED {part_dump_path}/{part_name}.pr.qdb -to {part_hier} -entity {part_entity}\n")
        else:
            self.log_msg(f"LOG_WRN: no logic partition csv style file", "LOG_WRN")

    ###############################
    ##      PIN
    ##
    ################################

    def loadPin(self, f):
        all_pins=""
        pin_template="#=================TEMPLATE======================================\n\n"
        if os.path.exists(self.path.pin):
            with open(self.path.pin, newline='') as csvfile:
                csv_reader = csv.reader(csvfile, delimiter=';')
                rows = [row for row in csv_reader]
            rows_sorted = sorted(rows, key=lambda x: x[-1])
            all_pins = all_pins + pin_template.replace("TEMPLATE",rows_sorted[0][-1])
            for i, row in enumerate(rows_sorted):
                if (i > 0):
                    if (rows_sorted[i][-1] != rows_sorted[i-1][-1]):
                        all_pins = all_pins + pin_template.replace("TEMPLATE",rows_sorted[i][-1])
                if (row[4].lower() == "altera"):
                    pin_name = row[0]
                    pin_standard = row[1]
                    pin_location = row[2]
                    pin_direction = row[3] 
                    all_pins = all_pins + f"set_instance_assignment -name IO_STANDARD \"{pin_standard}\" -to {pin_name}\n"
            all_pins = all_pins + pin_template.replace("TEMPLATE",rows_sorted[0][-1])
            for i, row in enumerate(rows_sorted):
                if (i > 0):
                    if (rows_sorted[i][-1] != rows_sorted[i-1][-1]):
                        all_pins = all_pins + pin_template.replace("TEMPLATE",rows_sorted[i][-1])
                if (row[4].lower() == "altera"):
                    pin_name = row[0]
                    pin_standard = row[1]
                    pin_location = row[2]
                    pin_direction = row[3] 
                    all_pins = all_pins + f"set_location_assignment {pin_location} -to {pin_name}\n"
            self.log_msg(f"LOG_INF: loading pin information", "LOG_INF")
            f.write(f"\n\n#Pin information\n")
            f.write(all_pins)
        else:
            self.log_msg(f"LOG_WRN: no .pin definition file", "LOG_WRN")

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
            print(f"{GREEN}INFO:Displaying compilation {YELLOW}CRITICAL WARNING\n")
            os.system(f'grep "WARNING:" {self.path.rprt}/vivado.log')
            print(f"{GREEN}INFO:Displaying compilation {RED}ERRORS\n")
            os.system(f'grep "*ERROR:" {self.path.rprt}/vivado.log')
            print(ENDCOLOR)

    ###############################
    ##      Actions
    ##
    ################################ 

    def loadGUI(self, f):
        if self.en.gui:
            f.write(f"\n\n#GUI\n")
            f.write(f"quartus {self.path.prj}\n")

    def loadSynth(self, f):
        self.log_msg(f"LOG_INF: loading synth command", "LOG_INF")
        f.write(f"\n\n#Synth\n")
        f.write(f"quartus_syn {self.quartus.opt_synt} {self.path.prj}\n")
        self.loadGUI(f)

    def loadRoute(self, f):
        self.log_msg(f"LOG_INF: loading route command", "LOG_INF")
        f.write(f"\n\n#Route\n")
        f.write(f"quartus_fit {self.quartus.opt_rout} {self.path.prj}\n")
        self.loadGUI(f)

    def loadSTA(self, f):
        self.log_msg(f"LOG_INF: loading STA command", "LOG_INF")
        f.write(f"\n\n#STA\n")
        f.write(f"quartus_sta {self.quartus.opt_sta} {self.path.prj} --sdc {self.path.sdc}\n")
        self.loadGUI(f)
    


    ###############################
    ##      MAIN
    ##
    ################################ 

    def createPrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadPrjInfo(f)
        self.loadDef(f)
        self.loadInc(f)
        self.loadRTL(f)
        self.loadEXT(f)
        self.loadIP(f)
        self.loadExtCnfg(f)
        self.loadSDC(f)
        self.loadSigTap(f)
        self.loadPartition(f)
        self.loadPin(f)
        self.logfile.close()

    def synthPrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadSynth(f)
        self.logfile.close()

    def routePrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadRoute(f)
        self.logfile.close()

    def staPrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadSTA(f)
        self.logfile.close()
