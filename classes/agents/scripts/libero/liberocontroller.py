# =============================================================================
# Project:        Logic on Rails
# File:           liberocontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        15 aug 2025
# Description:    controller for libero 
# =============================================================================

import subprocess
import os
import inspect
import shutil
import re
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

class  LiberoController():

    ###############################
    ##         CONSTRUCTOR
    ##
    ################################
    def __init__(self):
        self.en=SimpleNamespace()
        self.mcrsemi=SimpleNamespace()
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
        self.path.fprj = f"{self.path.prj}/{self.cnfg.module_name}.prjx"
        self.path.wave = os.getenv('wave')
        self.path.log = os.getenv('libero_log_name')
        self.path.f = os.getenv('libero_script_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.constr = os.getenv('prj_constraint')
        self.path.iopdc = f"{os.getenv('libero_iopdc')}"
        self.path.fppdc = f"{os.getenv('libero_fppdc')}"
        self.path.fpdc = f"{self.path.constr}/{os.getenv('libero_pdc_folder')}"
        self.path.sdc = os.getenv('source_sdc')
        self.path.pin = os.getenv('source_pins')
        self.path.fw = os.getenv('firmware_path')
        self.path.rpt_time = f"{self.path.rprt}/{self.cnfg.module_name}.time.rpt"
        self.path.bit = f"{self.path.prj}/{self.cnfg.module_name}.bit"

        self.mcrsemi.fam = os.getenv('libero_family')
        self.mcrsemi.die = os.getenv('libero_die')
        self.mcrsemi.pkg = os.getenv('libero_package')

        self.mcrsemi.opt_synt = os.getenv('libero_synth_opt')
        self.mcrsemi.opt_rout = os.getenv('libero_pr_opt')
        self.mcrsemi.opt_sim = os.getenv('libero_sim_opt')
        self.mcrsemi.opt_sta = os.getenv('libero_sta_opt')
        self.mcrsemi.opt_bit = os.getenv('libero_bit_bit')

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        self.defs.eda_tool = f" LIBERO "

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

    def createPrjEnv(self, f):
        self.log_msg(f"LOG_INF: Generate initial libro creation command", "LOG_INF")
        f.write("\n\n#Command Creation \n")
        f.write(f'new_project -name {self.cnfg.module_name} -location {self.path.prj} -project_description {{}} -block_mode 0 -standalone_peripheral_initialization 0 -instantiate_in_smartdesign 1 -ondemand_build_dh 1 -use_relative_path 0 -linked_files_root_dir_env {{}} -hdl verilog -family {self.mcrsemi.fam} -die {self.mcrsemi.die} -package {self.mcrsemi.pkg } -speed {{-1}} -die_voltage {{1.05}} -part_range {{IND}} -adv_options {{IO_DEFT_STD:LVCMOS 1.8V}} -adv_options {{RESTRICTPROBEPINS:1}} -adv_options {{RESTRICTSPIPINS:0}} -adv_options {{SYSTEM_CONTROLLER_SUSPEND_MODE:0}} -adv_options {{TEMPR:IND}} -adv_options {{VCCI_1.2_VOLTR:IND}} -adv_options {{VCCI_1.5_VOLTR:IND}} -adv_options {{VCCI_1.8_VOLTR:IND}} -adv_options {{VCCI_2.5_VOLTR:IND}} -adv_options {{VCCI_3.3_VOLTR:IND}} -adv_options {{VOLTR:IND}}\n') 

    ###############################
    ##      RTLS
    ##
    ################################ 

    def loadInc(self, f):
        if self.manifests["inc"]:
            self.log_msg(f"LOG_INF: Load Includes", "LOG_INF")
            f.write("\n\n#Include Paths \n")
            f.write(f'set_global_include_path_order -paths {{ {" ".join(self.manifests["inc"])} }}\n') 
           
    def loadRTL(self, f):
        self.log_msg(f"LOG_INF: load rtl files", "LOG_INF")
        self.cmd.rtl = " ".join(self.manifests["rtl"])
        f.write(f"\n\n#RTL files\n")
        for each_rtl in self.manifests["rtl"]:
            f.write(f"create_links -hdl_source {each_rtl}\n")
              
    def loadExt(self, f):
        if self.en.ext:
            if self.manifests["ext"]:
                self.log_msg(f"LOG_INF: load rtl files", "LOG_INF")
                self.cmd.rtl = " ".join(self.manifests["enc_lib"])
                f.write(f"\n\n#RTL files\n")
                for each_rtl in self.manifests["rtl"].split():
                    f.write(f"create_links -hdl_source {each_rtl}\n")
            else:
                self.log_msg(f"LOG_CRT: external ip flow enabled, but no files in manifest", "LOG_CRT")

    ###############################
    ##      Build Hier
    ##
    ################################

    def buildHier(self, f):
        f.write("\n\n#Update Hierarchy \n")
        f.write(f'build_design_hierarchy\n') 

    ###############################
    ##      Config MSS
    ##
    ################################


    def cnfgMSS(self, f):
        if self.en.uproc:
            if os.environ.get("ACTEL_UPROC_DIR", "") != "":
                libero_upro_dir = os.getenv('ACTEL_UPROC_DIR')
                if not os.path.isdir(self.path.fw):
                    self.log_msg(f"LOG_ERR: {self.path.fw} is not a folder", "LOG_ERR")
                    quit()
                folder_name = os.path.basename(self.path.fw)
                if not os.path.isfile(f"{self.path.fw}/{folder_name}.cfg"):
                    self.log_msg(f"LOG_ERR: {self.path.fw}/{folder_name}.cfg is not a file", "LOG_ERR")
                    quit()
                self.log_msg(f"LOG_INF: Running MSS flow", "LOG_INF")
                self.log_msg(f"LOG_WRN: MSS logic must be inside {self.path.fw}", "LOG_WRN")
                f.write("\n\n#MSS Flow - code below follows Libero self gen code\n")
                f.write(f"#MSS Flow - be sure you hav you mss logic inside {self.path.fw}\n")
                f.write(f'exec {libero_upro_dir} -GENERATE -CONFIGURATION_FILE:{self.path.fw}/{folder_name}.cfg -OUTPUT_DIR:{self.path.fw}/\n')
                f.write(f'import_mss_component -file "{self.path.fw}/{folder_name}.cxz"\n')       
            else:
                self.log_msg(f"LOG_ERR: when running uproc flow, user must define ACTEL_UPROC_DIR env var", "LOG_ERR")
                self.log_msg(f"LOG_CRT: maybe: <install path>/libero/<libero ver>/Libero/bin64/pfsoc_mss ?", "LOG_CRT")
                quit()

    ###############################
    ##      IPs
    ##
    ################################

    def downloadIPs(self, f):
        RE_VLNV = re.compile(r"core_vlnv\s*\{\s*([^}]*)\s*\}", re.IGNORECASE)
        LIB_TO_REPO = {
            "SystemBuilder": "SgCore",
            "DirectCore": "DirectCore",
            "Firmware": "Firmware",
        }
        def map_repo(vlnv: str):
             for lib, repo in LIB_TO_REPO.items():
                 if lib in vlnv:
                     return repo
             return None

        if self.manifests["ips"]: 
            ip_path = " ".join(v[len("MICROSEMI:"):] for v in self.manifests["ips"] if v.startswith("MICROSEMI:"))                
            if ip_path:
                self.log_msg(f"LOG_INF: load ip download", "LOG_INF")
                f.write(f"\n\n#IP Download\n")
                for each_ip in ip_path.split():
                    with open(each_ip, "r", encoding="utf-8", errors="ignore") as fh:
                        for line in fh:
                            if line.lstrip().startswith("create_and_configure_core"):
                                buffer = line
                                match = RE_VLNV.search(buffer)
                                while not match:
                                    nxt = fh.readline()
                                    if not nxt:
                                        break
                                    buffer += nxt
                                    match = RE_VLNV.search(buffer)
                                if match:
                                    ip_ver = match.group(1).strip()
                                    ip_repo = map_repo(ip_ver)
                                break
                    f.write(f"download_core -vlnv {{{ip_ver}}} -location {{www.microsemi.com/repositories/{ip_repo}}}\n")

    def loadIPs(self, f):
        if self.manifests["ips"]: 
            ip_path = " ".join(v[len("MICROSEMI:"):] for v in self.manifests["ips"] if v.startswith("MICROSEMI:"))                
            if ip_path:
                self.log_msg(f"LOG_INF: loading ips", "LOG_INF")
                f.write(f"\n\n#IP flow\n")
                for each_ip in ip_path.split():
                    if each_ip.endswith(".tcl"):
                        f.write(f"source {each_ip}\n")

    ###############################
    ##      Constraints
    ##
    ################################

    def loadSDC(self, f):
        self.log_msg(f"LOG_INF: load sdc", "LOG_INF")
        f.write("\n\n#Load SDC \n")
        f.write(f'create_links -sdc {self.path.sdc}\n') 

    def loadPDCFPFolder(self, f, path):
        if os.path.exists(path):
            f.write("\n\n#Load FP PDC \n")
            for filename in os.listdir(path):
                if filename.endswith(".pdc"):
                    self.cmd.fppdc += f"{path}/{filename} "
                    f.write(f'create_links -fp_pdc {path}/{filename}\n') 
        else:
            self.log_msg(f"LOG_ERR: error no fp folder exist in {path}", "LOG_ERR")
            quit()
    
    def loadPDCIOFolder(self, f, path):
        if os.path.exists(path):
            f.write("\n\n#Load IO PDC \n")
            for filename in os.listdir(path):
                if filename.endswith(".pdc"):
                    self.cmd.iopdc += f"{path}/{filename} "
                    f.write(f'create_links -io_pdc {path}/{filename}\n') 
        else:
            self.log_msg(f"LOG_ERR: error no io folder exist in {path}", "LOG_ERR")
            quit()

    def pdcOriderFlow(self, f):
        iofolder = f"{self.path.fpdc}/io/"
        fpfolder = f"{self.path.fpdc}/fp/"
        self.loadPDCFPFolder(f, fpfolder)
        self.loadPDCIOFolder(f, iofolder)

    def genFromPin(self, iopdc):
        if os.path.exists(self.path.pin):
            with open(self.path.pin, 'r', encoding='utf-8') as f:
                for ln in f:
                    ln = ln.strip()
                    if not ln or ln.startswith('#'):
                        continue
                    col = [p.strip() for p in ln.split(';')]
                    print(col)
                    if len(col) < 5:
                        self.log_msg(f"LOG_ERR: Error, pin file has less then 5 columns", "LOG_ERR")        
                        break
                    pname, pstd, ploc, pdir, pvendor = col[:5]
                    pstd = f"-io_std {pstd}" if not pstd else ""
                    pname = f"{{{pname}}}" if "[" in pname else f"{pname}"
                    pdir = "OUTPUT" if (pdir == "O") else "INPUT"
                    if pvendor.lower() == 'microsemi':
                        iopdc.write(f"set_io -pin_name {ploc} -port_name {pname} -fixed true {pstd} -DIRECTION {pdir}\n")
        else:
            self.log_msg(f"LOG_CRT: No PIN found while generating xdc", "LOG_CRT")        

    def genIOPDCFlow(self, f):
        if not os.path.isfile(self.path.iopdc):
            iopdc = open(self.path.iopdc, 'w', encoding='utf-8', newline='\n')
            self.genFromPin(iopdc)
        else:
            self.log_msg(f"LOG_INF: Using existing pdc file", "LOG_INF")
        self.log_msg(f"LOG_INF: Loading IOPDC", "LOG_INF")            
        self.cmd.iopdc += f"{self.path.iopdc}"
        f.write("\n\n#Load IO PDC\n")
        f.write(f'create_links -io_pdc  {self.path.iopdc}\n')

    def loadAssignFPPDC(self, f):
        if os.path.isfile(self.path.fppdc):
            self.cmd.fppdc += f"{self.path.fppdc}"
            f.write("\n\n#Load FP PDC\n")
            f.write(f'create_links -fp_pdc  {self.path.fppdc}\n')
        else:
            self.log_msg(f"LOG_CRT: No FP PDC loaded", "LOG_CRT")

    def loadPDC(self, f):
        self.log_msg(f"LOG_INF: load pdc io and fp", "LOG_INF")
        if self.en.pdcovr:
            self.pdcOriderFlow(f)
        else:
            self.genIOPDCFlow(f)
            self.loadAssignFPPDC(f)

    def loadConstraints(self, f):
        self.loadSDC(f)
        self.loadPDC(f)
    
    ###############################
    ##      Root
    ##
    ################################ 

    def loadRoot(self, f):
        self.log_msg(f"LOG_INF: loadin root file", "LOG_INF")
        f.write("\n\n#Load ROOT \n")
        f.write(f'set_root -module {self.cnfg.module_name}\n') 

    ###############################
    ##      TB
    ##
    ################################ 

    def loadTb(self, f):
        self.log_msg(f"LOG_INF: load tb files", "LOG_INF")
        f.write(f"\n\n#load tb files\n")
        self.cmd.tb = " ".join(self.manifests["tb"])
        for each_tb in self.cmd.tb.split():
            f.write(f"create_links -stimulus {each_tb}\n")
            if (each_tb == self.cnfg.tb_top):
                self.log_msg(f"LOG_INF: Setting TB Top", "LOG_INF")
                f.write(f"\n\n#Tb Top\n")
                f.write(f"organize_tool_files -tool {{SIM_PRESYNTH}} -file {{{each_tb}}} -module {{{self.cnfg.module_name}::work}} -input_type {stimulus}\n")
                f.write(f"organize_tool_files -tool {{SIM_POSTSYNTH}} -file {{{each_tb}}} -module {{{self.cnfg.module_name}::work}} -input_type {stimulus}\n")
                f.write(f"organize_tool_files -tool {{SIM_POSTLAYOUT}} -file {{{each_tb}}} -module {{{self.cnfg.module_name}::work}} -input_type {stimulus}\n")        

    ###############################
    ##      Constraint Manager
    ##
    ################################ 

    def loadConstrMng(self, f):
        self.log_msg(f"LOG_INF: Loading Constraint Manager settings", "LOG_INF")
        f.write(f"\n\n#Constraint Manager settings\n")
        f.write(f'run_tool -name {{CONSTRAINT_MANAGEMENT}}\n') 
        f.write(f'organize_tool_files -tool {{SYNTHESIZE}} -file {self.path.sdc}  -input_type {{constraint}} \n')
        f.write(f'organize_tool_files -tool {{PLACEROUTE}} -file {self.path.sdc} -file {self.cmd.iopdc} -file {self.cmd.fppdc} -input_type {{constraint}} \n')
        f.write(f'organize_tool_files -tool {{VERIFYTIMING}} -file {self.path.sdc} -input_type {{constraint}} \n')
        f.write(f'derive_constraints_sdc\n')
    
    ###############################
    ##      Defines
    ##
    ################################ 

    def loadDefs(self, f):
        self.log_msg(f"LOG_INF: configuring defines", "LOG_INF")
        syndef = f"{{SYNPLIFY_OPTIONS:"
        optstr = f"set_option -hdl_param -set SYNTHESIS;"
        append_cmd = ""
        self.cmd.defs += f" {self.defs.synth.replace('+define+','  ').replace('+',' ').strip()}"
        self.cmd.defs = self.cmd.defs
        f.write(f"\n\n#Generating defines\n")
        for each_define in self.cmd.defs.split():
            optstr += f'set_option -hdl_param -set {each_define};'
        syndef += optstr
        f.write(f'configure_tool -name {{SYNTHESIZE}} -params {{BLOCK_MODE:false}} -params {{CLOCK_GATE_ENABLE:false}} -params {{RETIMING:true}} -params {syndef}}}\n')

    ###############################
    ##      Save
    ##
    ################################

    def handleSave(self, f):
        self.log_msg(f"LOG_INF: Loading Save settings", "LOG_INF")
        f.write(f"\n\n#Save project\n")
        f.write(f'save_project\n') 
        f.write(f'close_project\n') 
        f.write(f'exit\n')

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
                    
    def printLogs(self, rpt):
        if (self.en.log):
            if os.path.exists(rpt):
                self.printLnIf(rpt, "LOG_WRN", "@W")
                self.printLnIf(rpt, "LOG_CRT", "@N")
                self.printLnIf(rpt, "LOG_ERR", "@E")
            else:
                self.log_msg(f"LOG_ERR: Report path {rpt} does not exist", "LOG_ERR", wr_file=False)


    ###############################
    ##      ACT
    ##
    ################################

    def loadPrj(self, f):
        self.log_msg(f"LOG_INF: Loading Save settings", "LOG_INF")
        f.write(f"\n\n#Open project\n")
        f.write(f'open_project {self.path.fprj}\n') 

    def configTool(self, f, act):
        conf_dic = {
            "SYNTHESIZE" : self.mcrsemi.opt_synt, 
            "PLACEROUTE" : self.mcrsemi.opt_rout,
            "VERIFYTIMING" : self.mcrsemi.opt_sta, 
            "GENERATEPROGRAMMINGDATA" : self.mcrsemi.opt_bit,    
        }
        if conf_dic[act]:
            self.log_msg(f"LOG_INF: Loading {act} settings", "LOG_INF")
            f.write(f"\n\n#CREATING SETTINGS FOR {act}\n")
            f.write(f'configure_tool -name {{{act}}} {conf_dic[act]} \n') 

    def loadRunTool(self, f, act):
        self.log_msg(f"LOG_INF: Loading {act}", "LOG_INF")
        f.write(f"\n\n#Running {act}\n")
        f.write(f'run_tool -name {act}\n') 


    ###############################
    ##      MAIN
    ##
    ################################ 

    def createPrj(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.createPrjEnv(f)
        self.loadInc(f)
        self.loadRTL(f)
        self.loadExt(f)
        self.buildHier(f)
        self.cnfgMSS(f)
        self.downloadIPs(f)
        self.loadIPs(f)    
        self.loadConstraints(f)  
        self.buildHier(f)
        self.loadRoot(f)
        self.loadTb(f)     
        self.loadConstrMng(f)   
        self.loadDefs(f)
        self.handleSave(f)      
        self.logfile.close()

    def createSynth(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadPrj(f)
        self.loadRunTool(f, "SYNTHESIZE")
        self.handleSave(f) 
        self.logfile.close()

    def createRoute(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadPrj(f)
        self.configTool(f, "PLACEROUTE")
        self.loadRunTool(f, "PLACEROUTE")
        self.handleSave(f) 
        self.logfile.close()

    def createSTA(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadPrj(f)
        self.loadRunTool(f, "VERIFYTIMING")
        self.handleSave(f) 
        self.logfile.close()

    def createBitStream(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.loadPrj(f)
        self.loadRunTool(f, "GENERATEPROGRAMMINGDATA")
        self.handleSave(f) 
        self.logfile.close()
