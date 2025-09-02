

# =============================================================================
# Project:        Logic on Rails
# File:           alteraAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Altera 
# =============================================================================
import subprocess
import inspect
import os
import sys

class AlteraAgent():
    def __init__ (self, args):
        self.script_filename = f'./_quartusScript.tcl'
        self.log_filename = f'./_quartusLog.txt'
        os.environ["quartus_script_name"] = self.script_filename
        os.environ["quartus_log_name"] = self.log_filename

        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.args   = args
        self.scripts_only = (os.getenv('scripts_only') == "on")

        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/quartus".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from quartuscontroller import QuartusController
        self.quartusCtrl = QuartusController()

        self.create = "quartus_create.sh"
        self.synth = "quartus_syn.sh"
        self.fit = "quartus_implementation.sh"
        self.sta = "quartus_sta.sh"
        self.bit = "quartus_asm"
        self.eda = "quartus_eda"
        self.jtag = "jtag/jtag.py"
        self.reports = "reports.py"
        self.prjPath = self.args.path+"/"+self.args.module_name
        self.bit_opt = os.environ["quartus_sta_bit"]

    def runCreate(self):
        self.quartusCtrl.createPrj()
        if not (self.scripts_only):
            subprocess.call(["quartus_sh", "-t", f"{self.script_filename}"])
        self.quartusCtrl.cleanEnv()
        self.quartusCtrl.printLogs()
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.create}"])

    def runSynth(self):
        self.quartusCtrl.synthPrj()
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
        self.quartusCtrl.cleanEnv()
        self.quartusCtrl.printLogs()
        #subprocess.call([f"{self.folder}/{self.synth}", self.prjPath])

    def runRoute(self):
        self.quartusCtrl.routePrj()
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
        self.quartusCtrl.cleanEnv()
        self.quartusCtrl.printLogs()
        #subprocess.call([f"{self.folder}/{self.fit}", self.prjPath])

    def runSta(self):
        self.quartusCtrl.staPrj()
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
        self.quartusCtrl.cleanEnv()
        self.quartusCtrl.printLogs()
        #subprocess.call([f"{self.folder}/{self.sta}", self.prjPath])

    def runBit(self):
        subprocess.call([self.bit,self.bit_opt, self.prjPath])        

    def runNetlist(self):
        subprocess.call([self.eda, "--simulation", "--tool=modelsim_oem", "--format=vhdl", self.prjPath])

    def runJtag(self):
        curr_dir = os.getcwd()
        subprocess.call(["python3", f"{self.folder}/{self.jtag}",  "-a", self.args.access, "-p", self.args.path, "-b", self.args.action, "-l", self.args.log, "-c",  curr_dir])

    def runReport(self):
        subprocess.call(["python3", f"{self.folder}/{self.reports}",  self.args.report, self.args.module_name , self.args.gui ,self.args.ignore, self.args.level])


    def runPrj(self):
        subprocess.call(["quartus", f'{self.args.path}/{self.args.module_name}.qpf'])        