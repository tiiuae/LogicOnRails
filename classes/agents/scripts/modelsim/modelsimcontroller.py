# =============================================================================
# Project:        Logic on Rails
# File:           modelsimcontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    controller for Modelsim 
# =============================================================================

import subprocess
import os
import inspect
import shutil
import glob
from enum import IntEnum

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

class ModelSimController():

    ###############################
    ##         CONSTRUCTOR
    ##
    ################################
    def __init__(self):
        self.cnfg=SimpleNamespace()
        self.path=SimpleNamespace()
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
        

    def log_msg(self, msg, lvl):
        req_msg = self.msg_giveColor(msg, lvl)
        if (int(LogLevel[lvl]) >= int(self.msg_lvl) ):
            print(req_msg)
            self.logfile.write(f"{req_msg}\n")

    def listFromFile(self, osvar: str):
        fpath = os.getenv(osvar)
        return [l.rstrip('\n') for l in open(fpath) if not l.lstrip().startswith('#')]


    ###############################
    ##         BUILD VARS
    ##
    ################################
    def genConstants(self):
        self.vendor = os.getenv('vendor')
        self.cnfg.module_name = os.getenv('module_name')
        self.module_name = os.getenv('module_name')
        self.cov_en = (os.getenv('coverage') == "on")
        self.gui_en = (os.getenv('gui') == "on")
        self.soft_en = (os.getenv('dpi') == "on")
        self.uvm_en = (os.getenv('uvm') == "on")
        self.ext_en = (os.getenv('ext_modules') == "on")
        self.log_en = (os.getenv('log') == "on")
        self.keep_en = (os.getenv('keep') == "on")
        self.acc_lvl = os.getenv('access')
        self.msg_lvl = LogLevel[os.getenv('message_lvl')]
        self.msg_str = os.getenv('message_lvl')
        self.wave_path = os.getenv('wave')
        self.ext_usr_vlog_opt = os.getenv('modelsim_sim_vlog')
        self.ext_usr_vcom_opt = os.getenv('modelsim_sim_vcom')
        self.ext_usr_vopt_opt = os.getenv('modelsim_sim_vopt')
        self.ext_usr_vsim_opt = os.getenv('modelsim_sim_vsim')

        self.path.prj = f"{os.getenv('prj_path')}/{self.cnfg.module_name}"
        self.path.compnt = f'{self.path.prj}/component'
        self.path.work   = f'{self.path.compnt}/work'
        self.path.micrsm = f'{self.path.compnt}/Microsemi'
        self.path.actl   = f'{self.path.compnt}/Actel'

        self.log_filename = os.getenv('modelsim_log_name')
        self.gen_filename = os.getenv('modelsim_script_name')
        self.lint_filename = os.getenv('modelsim_lint_name')
        self.tb_top = os.getenv('tb')
        self.reports = os.getenv('reports_path')
        self.altera_ip_libs = "-L work -L work_lib -L altera_ver -L lpm_ver -L sgate_ver -L altera_mf_ver -L altera_lnsim_ver -L cyclone10gx_ver -L cyclone10gx_hssi_ver -L cyclone10gx_hip_ver -L tennm_ver -L tennm_hssi_ver -L tennm_hssi_e0_ver -L tennm_hssi_p0_ver "
        self.microsemi_ip_libs = " -L polarfire "

        self.def_testname = f"+define+DEFAULT_TEST=\"{os.getenv('default_test')}\""
        self.def_edatool = f"+define+SIMULATION +define+MODELSIM"
        self.def_msglvl = f"+define+MESSAGE_LEVEL={self.msg_str}"
        self.def_list = f" {self.def_testname} {self.def_edatool} {self.def_msglvl} {os.getenv('synth_def')} {os.getenv('sim_def')}"

    def genCommandVars(self):
        self.verilog_cmd = ""
        self.vhdl_cmd = ""        
        self.ip_cmd = ""
        self.inc_cmd = ""
        self.pli_cmd = ""
        self.dpi_cmd = ""
        self.acc_cmd = ""
        self.vpi_cmd = ""
        self.soft_cmd = ""
        self.cov_com = ""
        self.cov_sim = ""
        self.def_cmd = f"{self.def_testname} {self.def_edatool} {self.def_msglvl}"

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

    def configUVM(self):
        if(self.uvm_en):
            self.inc_cmd += f"+incdir+{os.getenv('UVM_PATH')} "

    def configAccess(self):
        if not (self.acc_lvl == "off"):
            self.acc_cmd = f" +acc"


    def configCov(self, offset_path:str):
        if(self.cov_en):
            self.cov_com = f' -coveropt 3 +cover'
            self.cov_sim = f' -coverage -c -do "coverage save -onexit -directive -codeAll {offset_path}{self.reports}/{self.tb_top}.ucdb"'

    ###############################
    ##    TOOL SPECIFIC CONFIG
    ##
    ################################

    #REVIEW, USE THE cxf FILE INSTEAD AND READ THE HDL_FILESET RATHER THEN  READ EVERYTHING
    def microsemiIP(self, f):
        if os.path.exists("presynth"):
            self.log_msg("LOG_CRT : presynth lib already exists, scripts WILL NOT recompile libero IPs", "LOG_CRT")
        else:
            comp_files = glob.glob(f"{self.path.work}/**/*.v*", recursive=True)
            comp_files += glob.glob(f"{self.path.micrsm}/**/*.v*", recursive=True)
            comp_files += glob.glob(f"{self.path.compnt}/**/*.v*", recursive=True)
            comp_files = [p for p in comp_files if ("/test/" not in p) and ("/Stimulus/" not in p) and ("coreparameters" not in p) and ("syn_comps.v" not in p)]
            if comp_files:
                f.write(f'\n\n#Microsemi IPs Simulation\n')
                for each_c in comp_files:
                    if (".vhd" in each_c):
                        f.write(f'vcom -2008 -explicit -work presynth {each_c}\n')
                    elif (".v" in each_c):
                        f.write(f'vlog -sv -work presynth {each_c}\n')
        if os.path.exists("presynth"):
            self.ip_cmd += f" -L presynth "

    def genEDAReq(self, f):
        if (self.vendor == "microsemi"):
            if (os.getenv('LIBERO_ROOT_DIR') != ""):
                f.write(f'\n\n#Microsemi Flow\n')
                f.write(f'vmap polarfire {os.getenv("LIBERO_ROOT_DIR")}/lib/modelsimpro/precompiled/vlog/polarfire\n')
                f.write(f'vmap polarFire {os.getenv("LIBERO_ROOT_DIR")}/lib/modelsimpro/precompiled/vlog/polarfire\n')
                self.pli_cmd += f' -pli {os.getenv("LIBERO_ROOT_DIR")}/lib/modelsimpro/pli/pf_crypto_lin_se64_pli.so'
                self.ip_cmd += self.microsemi_ip_libs
                self.microsemiIP(f)
            else:
                self.log_msg("LOG_ERR : yaml config for microsemi flow, but LIBERO_ROOT_DIR env variable is not defined", "LOG_ERR")
                self.log_msg("LOG_ERR : define variable as <libero install folder>/Libero/", "LOG_ERR")


    ###############################
    ##         FILE CONFIG
    ##
    ################################ 
        
    def setOnErr(self, f):
        if not (self.gui_en):
            f.write("\n\n#On Error Flow\n")
            f.write("onerror { quit -f 1 }\n")

    def selectDir(self, f):
        if (self.vendor == "altera"):
            if os.path.exists(os.getenv('simlib_tcl')):
                f.write("\n\n#Altera IP Flow\n")
                self.ip_cmd += self.altera_ip_libs
                f.write(f"cd {os.getenv('simlib_tcl')}\n")
                f.write("source msim_setup.tcl\n")
                f.write("dev_com\n")
                f.write("com\n")
                return "../../"
            else:
                return ""
        else:
            return ""


    ###############################
    ##         EXTERNAL
    ##
    ################################ 


    def loadExtCompiled(self, offset):
        if self.manifests["comp_lib"]:
            for each_compIp in self.manifests["comp_lib"]:
                self.log_msg(f"LOG_INF: generating external compiled ip {each_compIp}", "LOG_INF")
                each_compIp = each_compIp.replace("QUESTA:", "")
                if not (":" in each_compIp):
                    self.log_msg(f"LOG_INF: {each_compIp} added to ip list", "LOG_INF")
                    self.ip_cmd += f'-L {offset_path}{each_compIp} '
        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_lib manifest", "LOG_WRN")

    def loadExtRtl(self, offset, f):
        if self.manifests["enc_lib"]:
            f.write("\n\n#.VP Flow \n")
            for each_rtlIp in self.manifests["enc_lib"]:
                f.write(f"vlog {offset}{each_rtlIp}")
        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_ip manifest",  "LOG_WRN")


    def loadExt(self, offset_path, f):
        if (self.ext_en):
            self.loadExtCompiled(offset_path)
            self.loadExtRtl(offset_path, f)

    ###############################
    ##       RTL - vlog vcom
    ##
    ################################ 

    def loadIncludes(self, offset_path, f):
        if self.manifests["inc"]:
            for each_include in self.manifests["inc"]:
                self.inc_cmd += f' +incdir+{offset_path}{each_include}'

    def loadDesign(self, offset_path, f):
        if self.manifests["rtl"]:
            verilog_list = [f for f in self.manifests["rtl"] if f.endswith((".sv", ".v"))]
            vhd_list  = [f for f in self.manifests["rtl"] if f.endswith(".vhd")]
            for each_verilog in verilog_list:
                self.log_msg(f"LOG_INF: loading {each_verilog}", "LOG_INF")
                self.verilog_cmd += f' {offset_path}{each_verilog}'
            for each_vhdl in vhd_list:
                self.log_msg(f"LOG_INF: loading {each_vhdl}", "LOG_INF")
                self.vhdl_cmd += f' {offset_path}{each_vhdl}'

        if self.manifests["tb"]:
            verilog_list = [f for f in self.manifests["tb"] if f.endswith((".sv", ".v"))]
            vhd_list  = [f for f in self.manifests["tb"] if f.endswith(".vhd")]
            for each_verilog in verilog_list:
                self.log_msg(f"LOG_INF: loading {each_verilog}", "LOG_INF")
                self.verilog_cmd += f' {offset_path}{each_verilog}'
            for each_vhdl in vhd_list:
                self.log_msg(f"LOG_INF: loading {each_vhdl}", "LOG_INF")
                self.vhdl_cmd += f' {offset_path}{each_vhdl}'


    def loadRTL(self, offset_path, f):
        self.loadIncludes(offset_path, f)
        self.loadDesign(offset_path, f)
        if not (self.verilog_cmd == ""):
            f.write("\n\n#Verilog Flow\n")
            f.write(f'vlog -sv -timescale 1ns/1ps -sv {self.verilog_cmd} -sv {self.inc_cmd} {self.def_list} {self.cov_com} {self.ext_usr_vlog_opt}\n')
        else: 
            self.log_msg(f"LOG_WRN: no verilog files in the desing", "LOG_WRN")
        if not (self.vhdl_cmd == ""):
            f.write("\n\n#VHDL Flow\n")
            f.write(f'vcom {self.vhdl_cmd} {self.ext_usr_vcom_opt}')
        else:
            self.log_msg(f"LOG_WRN: no vhdl files in the desing", "LOG_WRN")

    ###############################
    ##      DPI
    ##
    ################################ 
 
    def loadDPI(self, offset_path, f):
        if (self.soft_en):
            if self.manifests["soft"]:
                for each_soft in self.manifests["soft"]:
                    each_dpif = each_soft.replace("DPI:", "")
                    if not (":" in each_dpif):
                        self.log_msg(f"LOG_INF: adding DPI functions {each_dpif}", "LOG_INF")
                        filename = os.path.basename(each_dpif)
                        filename = filename.replace(".", "_")
                        os.environ[filename]  = f'{offset_path}{each_dpif}.exe '   
                        if (".h" in each_dpif):
                            self.dpi_cmd += f' {os.getenv("dpi_opt")} {offset_path}{each_dpif}'
                        else:
                            self.dpi_cmd += f' {offset_path}{each_dpif}'
                if not (self.dpi_cmd == ""):
                    f.write("\n\n#DPI Flow\n")
                    f.write(f"vlog -sv {self.dpi_cmd} {self.ext_usr_vlog_opt}\n")
        else:
            self.log_msg("LOG_CRT: software run enabled in modelsim but no .c function in software manifest", "LOG_CRT")


    ###############################
    ##      VPI
    ##
    ################################ 

    def loadVPI(self, offset_path, f):
        if (self.soft_en):
            if self.manifests["soft"]:
                f.write("\n\n#VPI Flow\n")
                for each_soft in self.manifests["soft"]:
                    each_vpif = each_soft.replace("VPI:", "")
                    if not (":" in each_vpif):
                        self.log_msg("LOG_WRN: VPI code must have MODELSIM_PATH env variable set", "LOG_WRN")
                        f.write(f"gcc -m64 -fPIC -shared {offset_path}{each_vpif} -o {offset_path}{each_vpif}.so -I{os.getenv('MODELSIM_PATH')}/include\n")
                        self.vpi_cmd += f" -pli {offset_path}{each_vpif}.so"
                        


    ###############################
    ##      OPT
    ##
    ################################ 

    def loadOpt(self, f):
        self.log_msg("LOG_INF: generating vopt command", "LOG_INF")
        f.write("\n\n#Optimization Flow\n")
        f.write(f"vopt {self.acc_cmd} {self.tb_top} {self.ip_cmd} {self.def_list} +test={os.getenv('default_test')} {self.ext_usr_vopt_opt} -o tb_snapshot\n")

    ###############################
    ##      SIM
    ##
    ################################ 

    def loadSim(self, f):
        self.log_msg("LOG_INF: generating vsim command", "LOG_INF")
        f.write("\n\n#Simulation Flow\n")
        f.write(f"vsim -t 1ps tb_snapshot {self.cov_sim} {self.vpi_cmd} {self.pli_cmd} {self.ext_usr_vsim_opt}\n")
        f.write(f"set TOP_LEVEL_NAME {self.tb_top}\n")
        f.write(f"view structure\n")
        f.write(f"view signals\n")

    ###############################
    ##      RUN
    ##
    ################################ 

    def loadRun(self, offset_path,f):
        self.log_msg("LOG_INF: generating run and cov commands", "LOG_INF")
        f.write("\n\n#Run modelsim sim\n")
        if (self.gui_en):
            if (self.acc_lvl == "on"):
                f.write(f"log -r /*\n") 
            f.write(f"do {offset_path}{self.wave_path}\n")
            f.write(f"run -all\n")
        else:
            f.write(f"run -all\n")
            if (self.cov_en):
                f.write(f"coverage report -html -output {offset_path}{self.reports}/coverage -annotate -details -assert -directive -cvg -code bcefst -threshL 50 -threshH 90\n")
                f.write(f"coverage report -output {offset_path}{self.reports}/coverage.txt -annotate -details -assert -directive -cvg -code bcefst\n")
            f.write(f"exit\n")

    ###############################
    ##      POST SCRIPT
    ##
    ################################ 
    
    def cleanEnv(self):
        if os.path.exists("simlib") and not self.keep_en : shutil.rmtree("simlib")
        if os.path.exists("work") and not self.keep_en: shutil.rmtree("work")
        if os.path.exists("presynth") and not self.keep_en: shutil.rmtree("presynth")
        if os.path.exists("transcript"): 
            if (self.log_en):
                shutil.move("transcript", f"{self.reports}/{self.module_name}.modelsim.rpt")
            else:
               if not (self.keep_en): os.remove("transcript")
        if os.path.exists(self.gen_filename): 
            if (self.log_en):
                shutil.move(self.gen_filename, f"{self.reports}/{self.gen_filename}")
            else:
                if not (self.keep_en): os.remove(self.gen_filename)
        if os.path.exists(self.log_filename): 
            if (self.log_en):
                shutil.move(self.log_filename, f"{self.reports}/{self.log_filename}")
            else:
                if not (self.keep_en): os.remove(self.log_filename)

    def printLogs(self):
        if (self.log_en):
            print(f"{GREEN}INFO:Displaying compilation {YELLOW}CRITICAL WARNING\n")
            os.system(f'grep "** Warning:" {self.reports}/{self.module_name}.modelsim.rpt')
            print(f"{GREEN}INFO:Displaying compilation {RED}ERRORS\n")
            cmd = f'grep "** Error" {self.reports}/{self.module_name}.modelsim.rpt'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            errors = result.stdout
            cmd = f'grep "** Fatal" {self.reports}/{self.module_name}.modelsim.rpt'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            errors += result.stdout
            err_list = errors.split("\n")
            err_filtered = [line for line in err_list if "# Errors: 0" not in line]
            str_filtr = "\n".join(err_filtered) + "\n"
            print(str_filtr)

            print(ENDCOLOR)

    ###############################
    ##      MAIN
    ##
    ################################ 

    def createSimEnv(self):
        if os.path.exists(self.gen_filename): os.remove(self.gen_filename)
        f = open(self.gen_filename, "a")
        self.logfile = open(self.log_filename, "a")
        self.setOnErr(f)
        offset_path = self.selectDir(f)
        self.configUVM()
        self.configAccess()
        self.configCov(offset_path)
        self.genEDAReq(f)
        self.loadExt(offset_path, f)
        self.loadRTL(offset_path, f)
        self.loadDPI(offset_path, f)
        self.loadVPI(offset_path, f)
        self.loadOpt(f)
        self.loadSim(f)
        self.loadRun(offset_path, f)
        self.logfile.close()
        



