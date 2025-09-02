# =============================================================================
# Project:        Logic on Rails
# File:           modelsimAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Modelsim 
# =============================================================================

import subprocess
import os
import inspect
import sys


class ModelSimAgent():
    def __init__(self, args):
        self.script_filename = f'./_modelSimScript.tcl'
        self.log_filename = f'./_modelSimLog.txt'
        self.lint_filename = f'./_modelSimLint.tcl'
        os.environ["modelsim_script_name"] = self.script_filename
        os.environ["modelsim_log_name"] = self.log_filename
        os.environ["modelsim_lint_name"] = self.lint_filename
        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.scripts_only = (os.getenv('scripts_only') == "on")
        self.args   = args
        
        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/modelsim".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from modelsimcontroller import ModelSimController
        self.mdsimCtrl = ModelSimController()

        #sim opt
        if (self.args.gui == "on"):
            self.gui_opt = "-gui"
        else:
            self.gui_opt = "-c"

        #do be deprecated
        self.simfile = "modelsim.sh"


    def preBuild(self):
        if (self.vendor == "altera"):
            simlib = "./simlib"
            os.environ["simlib_tcl"] = f'{simlib}/mentor'
            if self.mdsimCtrl.manifests["ips"] and any("ALTERA:" in s for s in self.mdsimCtrl.manifests["ips"]):
                subprocess.call(["ip-setup-simulation", f"--quartus-project=./{self.args.path}/{self.args.module_name}", f"--output-directory={simlib}/", "--use-relative-paths", "--compile-to-work"])

    def postBuild(self):
        if (self.args.coverage == "on"):
            subprocess.call(["firefox", f"{self.reports}/coverage/covSummary.html"])


    def runSim(self):
        self.preBuild()
        self.mdsimCtrl.createSimEnv()    
        if not (self.scripts_only):
            subprocess.call(["vsim", self.gui_opt, "-do", self.script_filename])
        self.mdsimCtrl.cleanEnv()
        self.mdsimCtrl.printLogs()
        self.postBuild()

        #to be deprecated
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.simfile}"])

