# =============================================================================
# Project:        Logic on Rails
# File:           xceliumcontroller
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    controller for Xcelium 
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

class XceliumController():

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
        self.path.log = os.getenv('xcelium_log_name')
        self.path.f = os.getenv('xcelium_script_name')
        self.path.lint = os.getenv('xcelium_lint_name')
        self.path.rprt = os.getenv('reports_path')
        self.path.covroot = "cov_work/"
        self.path.cov =f'{self.path.covroot}/scope/test'
        self.path.xrun = os.getenv('xrun_dir')
        self.path.xrun_scrpt = os.getenv('xrun_script_dir')
        self.path.xrun_logs = f'{self.path.xrun}/logs'
        self.path.xrun_libs = f'{self.path.xrun_scrpt}/libraries'
        self.path.xrun_ips = f'{self.path.xrun}/libraries_ip'
        self.path.xrun_tb = f'{self.path.xrun}/libraries_tb'
        self.path.xrun_ext = f'{self.path.xrun}/libraries_extr'

        self.cmd.xrun_shared = f"-v200x -plusperf -newperf -access +rwc -64bit -sysv_ext +.v -timescale 1ns/1ps"
        self.cmd.xrun_comp_opt = f" -compile -rwelab {self.cmd.xrun_shared}"
        self.cmd.xrun_sim_opt = f" {self.cmd.xrun_shared}" 

        self.defs.synth = os.getenv('synth_def')
        self.defs.sim = os.getenv('sim_def')
        self.defs.tname = f"-define DEFAULT_TEST=\\\"{os.getenv('default_test')}\\\""
        self.defs.eda_tool = f"-define SIMULATION -define XCELIUM"
        self.defs.msglvl = f"-define MESSAGE_LEVEL={self.msg.cntnt}"

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
    ##         CONFIG VARS
    ##
    ################################ 

    def configUVM(self):
        if(self.en.uvm):
            self.log_msg(f"LOG_WRN: when running the uvm flow, $UVMHOME env var must be set", "LOG_INF")
            self.cmd.defs +=f'-uvmhome {os.getenv("UVMHOME")}'
            self.cmd.defs += f' +UVM_TESTNAME={os.getenv("default_test")} +UVM_VERBOSITY=UVM_LOW'

    def configCov(self):
        if(self.en.cov):
            self.log_msg(f"LOG_INF: configuring coverage vars, coverage flow enabled", "LOG_INF")
            cov_fullpath = f"{self.path.xrun}/{self.path.covroot}"
            if os.path.exists(cov_fullpath): os.remove(cov_fullpath)
            self.cmd.cov += " -coverage all -covoverwrite"

    def configDefines(self):
        self.log_msg(f"LOG_INF: configuring defines", "LOG_INF")
        self.cmd.defs += f" {self.defs.synth.replace('+define+',' -define ').replace('+',' ').strip()}"
        self.cmd.defs += f" {self.defs.sim.replace('+define+',' -define ').replace('+',' ').strip()}"

    def configWave(self):
            self.log_msg(f"LOG_INF: configuring wave file", "LOG_INF")
            filename = os.path.basename(self.path.wave)            
            probe_en_str=f"probe -shm -all\n"
            with open(self.path.wave, "r") as f:
                lines = f.readlines()            
            if lines:
                lines[-1] = lines[-1].replace(f"simvision -input {filename}.svcf", "simvision -input $env(wave).svcf")
            with open(self.path.wave, "w") as f:
                f.writelines(lines)
            
            if(self.en.acc):
                with open(self.path.wave, "r+") as f:
                    content = f.read()
                    if probe_en_str not in content:
                        if not content.endswith("\n"):
                            f.write("\n")
                        f.write(probe_en_str)

    def configGui(self):
        if (self.en.gui):
            self.log_msg(f"LOG_INF: Configured to run on the gui Flow on Xcelium", "LOG_INF")
            self.cmd.gui = "-gui"
            self.cmd.wave = "-input $wave"     
            self.configWave()

    ###############################
    ##         IPS
    ##
    ################################

    def quartusIPgen(self):
        if not os.path.isdir(self.path.xrun_ips):
            self.log_msg(f"LOG_WRN: Execuring xcelium_setup.sh generated from quartus inside {self.path.xrun_scrpt}", "LOG_WRN")
            subprocess.run(
                ['bash', '-lc', f'export INCA_64BIT; export CDS_AUTO_64BIT=ALL; source xcelium_setup.sh; SKIP_ELAB=1 SKIP_SIM=1'],
                cwd=self.path.xrun_scrpt, check=True
            )
            self.log_msg(f"LOG_INF: moving hdl var and cds files", "LOG_INF")
            shutil.move(self.path.xrun_libs, self.path.xrun_ips)
            shutil.move(f"{self.path.xrun_scrpt}/hdl.var", f"{self.path.xrun}")
            cds_txt = Path(f"{self.path.xrun_scrpt}/cds.lib").read_text()
            cds_txt = cds_txt.replace('libraries', 'libraries_ip')
            Path(f'{self.path.xrun}/cds.lib').write_text(cds_txt)
            path_visit = [f for f in os.listdir(self.path.xrun_ips) if Path(f'{self.path.xrun_ips}/{f}').is_dir()]
            self.log_msg(f"LOG_INF: deleting redundant pak files", "LOG_INF")
        folders = [p.name for p in Path(f"{self.path.xrun_ips}").iterdir() if p.is_dir() and p.name != "work"]
        return folders

    def genIPs(self, f):
        self.log_msg(f"LOG_INF: Checking for vendor specific ips", "LOG_INF")
        if(self.cnfg.vendor == "altera"):
            if self.manifests["ips"] and any("ALTERA:" in s for s in self.manifests["ips"]):
                self.log_msg(f"LOG_WRN: Altera IPs found, starting Altera flow", "LOG_WRN")
                self.log_msg(f"LOG_WRN: User must have set the QUARTUS_ROOTDIR env var to run ip flow", "LOG_WRN")
                quartus_ips = self.quartusIPgen()
                os.environ["QUARTUS_INSTALL_DIR"] = os.getenv('QUARTUS_ROOTDIR')
                for each_ip in quartus_ips:
                    self.cmd.ip += f" -reflib {self.path.xrun_ips}/{each_ip}"

    ###############################
    ##         EXTERNAL
    ##
    ################################ 

    def loadExtCompiled(self):
        if self.manifests["comp_lib"]:
            for each_compIp in self.manifests["comp_lib"]:
                self.log_msg(f"LOG_INF: generating external compiled ip {each_compIp}", "LOG_INF")
                each_compIp = each_compIp.replace("XCELIUM:", "")
                if not (":" in each_compIp):
                    self.log_msg(f"LOG_INF: {each_compIp} added to ip list", "LOG_INF")
                    self.cmd.ext += f' -reflib {each_compIp} '
        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_lib manifest", "LOG_WRN")

    def loadExtRtl(self, f):
        if self.manifests["enc_lib"]:
            f.write("\n\n#.VP Flow \n")
            dir_list = sorted({Path(f"{os.path.dirname(p)}/").as_posix() for p in self.manifests["enc_lib"]})
            f.write(f"curr_dir=`pwd`\n")
            idx = 0
            for each_dir in dir_list:
                f.write(f"cd {each_dir}\n")
                f.write(f'xrun -v200x -timescale 1ns/1ps -64bit -compile -rwelab -makelib "ext_{idx}" * \n')
                f.write(f'mv ./xcelium.d/ext_{idx} $curr_dir/{self.path.xrun_ext}\n')
                f.write(f'rm -rf ./xcelium.d/ xrun.history xrun.log\n')
                f.write(f'cd $curr_dir\n')
                self.cmd.ext += f" -reflib {self.path.xrun_ext}/ext_{idx}"
                idx += 1

        else:
            self.log_msg(f"LOG_WRN: ext_modules is ON but there is no file to load in the ext_ip manifest",  "LOG_WRN")


    def compExt(self, f):
        if (self.en.ext):
            if os.path.exists(self.path.xrun_ext): 
                shutil.rmtree(self.path.xrun_ext)
                os.makedirs(self.path.xrun_ext)
            self.loadExtCompiled()
            self.loadExtRtl(f)


    ###############################
    ##       RTL 
    ##
    ################################ 
    
    def configInc(self):
        self.log_msg(f"LOG_INF: Checking include paths", "LOG_INF")
        for each_inc in self.manifests["inc"]:
            self.cmd.inc += f" -incdir {each_inc}"


    def compRTL(self, f):
        if os.path.exists(self.path.xrun_tb): shutil.rmtree(self.path.xrun_tb)
        self.log_msg(f"LOG_INF: Generating xrun compilaion run - required for altera compatibility", "LOG_INF")
        self.cmd.rtl = " ".join(self.manifests["rtl"])
        self.cmd.tb = " ".join(self.manifests["tb"])
        self.cmd.dsgn += f" -reflib {self.path.xrun_tb}" 
        f.write(f"\n\n#XRUN compilation run\n")
        f.write(f'xrun  {self.cmd.xrun_comp_opt} -makelib {self.path.xrun_tb} {self.cmd.rtl} {self.cmd.tb} {self.cmd.inc} {self.cmd.defs}  | tee {self.path.rprt}/{self.cnfg.vendor}.xrun_comp.rpt \n')



    ###############################
    ##      DPI
    ##
    ################################ 

    def compDPI(self, f):
        altera_dpi = ""
        if (self.en.sw):
            if self.manifests["soft"]:
                dpi_code = " ".join(v[len("DPI:"):] for v in self.manifests["soft"] if v.startswith("DPI:"))
                if dpi_code:
                    if (self.cnfg.vendor == "altera"):
                        self.log_msg(f"LOG_WRN: Generating dpi in quartus flow, be sure to have QUARTUS_INSTALL_DIR env var set", "LOG_WRN")
                        altera_dpi = "$QUARTUS_INSTALL_DIR/eda/sim_lib/simsf_dpi.cpp"
                    f.write("\n\n#.DPI Flow \n")
                    f.write(f"gcc -fPIC -g -shared -o libdpi.so -I/`ncroot`/tools/inca/include {dpi_code} {altera_dpi}\n")
                    for each_dpi in dpi_code.split():
                        file_name = os.path.basename(each_dpi) 
                        sanitizedVarName = file_name.replace('.', '_')
                        f.write(f'export {sanitizedVarName}="{each_dpi}.exe "\n')
                        os.environ["sanitizedVarName"] = f"{each_dpi}.exe "
        else:
            if (self.cnfg.vendor == "altera"):
                if altera_dpi:
                    f.write("\n\n#.Altera IP requirement\n")
                    f.write(f"gcc -fPIC -g -shared -o libdpi.so -I/`ncroot`/tools/inca/include {altera_dpi}\n")


 

    ###############################
    ##      VPI
    ##
    ################################ 

    def compVPI(self, f):
        if (self.en.sw):
            if self.manifests["soft"]:
                vpi_code = " ".join(v[len("VPI:"):] for v in self.manifests["soft"] if v.startswith("VPI:"))                
                if vpi_code:
                    self.log_msg(f"LOG_INF: Generating vpi data, vpi register function must be under xcelium_reg_vpi", "LOG_INF")
                    f.write("\n\n#.VPI Flow \n")
                    for each_vpi in vpi_code.split():
                        with open(each_vpi) as fprime:
                            vpi_fname = "".join(line for line in fprime if "$" in line)
                            f.write(f'gcc -Wl,--export-dynamic -std=gnu99 -fPIC -m64 -shared -I/`ncroot`/tools.lnx86/inca/include {each_vpi} -o {each_vpi}.so\n')
                            self.cmd.vpi += f" -loadvpi ./{each_vpi}.so:xcelium_reg_vpi"


    ###############################
    ##      SIM
    ##
    ################################ 

    def runSim(self, f):
        self.log_msg(f"LOG_INF: Generating xrun simulation data", "LOG_INF")
        f.write("\n\n#Simulation Flow \n")
        f.write(f"xrun {self.cmd.vpi} {self.cmd.xrun_sim_opt} -top {self.cnfg.tb_top} {self.cmd.dsgn} {self.cmd.ip} {self.cmd.ext} {self.cmd.defs} {self.cmd.gui} {self.cmd.wave} {self.cmd.cov}\n")


    ###############################
    ##      PRE SCRIPT
    ##
    ################################ 

    def checkEnv(self):
        os.makedirs(self.path.xrun_logs, exist_ok=True)
        os.makedirs(self.path.xrun_ext, exist_ok=True)

    def genVer(self, f):
        self.log_msg(f"LOG_WRN: Creating the version information for X64 bit Linux", "LOG_WRN")
        f.write("\n\n#Xcelium 64bits\n")
        f.write("export INCA_64BIT\nexport CDS_AUTO_64BIT=ALL\n")

    ###############################
    ##      POST SCRIPT
    ##
    ################################ 

    def cleanEnv(self):
        if os.path.exists("./xcelium.d") and not self.en.keep: shutil.rmtree("./xcelium.d")
        if os.path.exists("xcelium.shm") and not self.en.keep: shutil.rmtree("xcelium.shm")
        if os.path.exists("libdpi.so") and not self.en.keep: os.remove("libdpi.so")
        if os.path.exists("xrun.key") and not self.en.keep: os.remove("xrun.key")
        if os.path.exists("waves.shm") and not self.en.keep: os.remove("waves.shm")
        if os.path.exists("xrun.history") and not self.en.keep: os.remove("xrun.history")
        if os.path.exists("xrun.log") and not self.en.keep: os.remove("xrun.log")
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
            os.system(f'grep "*W" {self.path.rprt}/{self.cnfg.vendor}.xrun_comp.rpt')
            print(f"{GREEN}INFO:Displaying compilation {RED}ERRORS\n")
            os.system(f'grep "*E" {self.path.rprt}/{self.cnfg.vendor}.xrun_comp.rpt')
            print(ENDCOLOR)

    ###############################
    ##      Hal Lint
    ##
    ################################ 

    def configHalLinter(self, f):
        self.cmd.rtl = " ".join(self.manifests["rtl"])
        self.cmd.tb = " ".join(self.manifests["tb"]) if (self.en.lint_tb) else ""
        self.log_msg(f"LOG_INF: Generating Linting Command", "LOG_INF")
        f.write("\n\n#Linting\n")
        f.write(f"xrun -hal -lint_only -disable_sem2009 -top {self.cnfg.module_name} {self.cmd.inc} {self.cmd.tb} {self.cmd.rtl} \n")

    ###############################
    ##      Modus
    ##
    ################################ 

    def configModusSim(self, f):
        self.log_msg(f"LOG_WRN: Running Modus Flow, use default test yaml opt to set .verilog test file", "LOG_WRN")
        modus_v = f'-v {" ".join(self.manifests["rtl"])}'
        modus_access = f"+access +rwc +xmstatus +xm64bit "
        modus_failset += f"+HEARTBEAT +FAILSET  "
        modus_timescale = f"+xmtimescale+1ns/1ps +xmoverride_timescale +xmseq_udp_delay+2ps "
        modus_fileset = f"+libext+.v+.V+.z+.Z.gz "
        modus_opt = f"{modus_access} +TESTFILE1={os.getenv('default_test')} {modus_failset} {modus_timescale} {modus_fileset} {modus_v}"
        f.write("\n\n#Modus Flow \n")
        f.write(f"xrun {modus_opt}\n")

    ###############################
    ##      MAIN
    ##
    ################################ 

    def createSimEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.configUVM()
        self.configDefines()
        self.configGui()
        self.configCov()
        self.configInc()
        self.checkEnv()
        self.genVer(f)
        self.genIPs(f)
        self.compRTL(f)
        self.compExt(f)
        self.compDPI(f)
        self.compVPI(f)
        self.runSim(f)
        self.logfile.close()
        
    def createModusEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.configDefines()
        self.configGui()
        self.configModusSim(f)
        self.logfile.close()

    def createLintEnv(self):
        if os.path.exists(self.path.f): os.remove(self.path.f)
        f = open(self.path.f, "a")
        self.logfile = open(self.path.log, "a")
        self.configDefines()
        self.configInc()
        self.configHalLinter(f)
        self.logfile.close()

