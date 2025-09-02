# =============================================================================
# Project:        Logic on Rails
# File:           questaAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Questa 
# =============================================================================
import subprocess
import os
import inspect
import sys


class QuestaAgent():
    def __init__(self, args):
        self.script_filename = f'./_questaSimScript.tcl'
        self.log_filename = f'./_questaSimLog.txt'
        self.lint_filename = f'./_questaSimLint.tcl'
        os.environ["questa_script_name"] = self.script_filename
        os.environ["questa_log_name"] = self.log_filename
        os.environ["questa_lint_name"] = self.lint_filename
        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.scripts_only = (os.getenv('scripts_only') == "on")
        self.args   = args
        
        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/questa".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from questacontroller import QuestaController
        self.questaCtrl = QuestaController()

        #sim opt
        if (self.args.gui == "on"):
            self.gui_opt = "-gui"
        else:
            self.gui_opt = "-c"

        self.simfile = "questa.tcl"

    def postBuild(self):
        if (self.args.coverage == "on"):
            subprocess.call(["firefox", f"{self.reports}/coverage/covSummary.html"])

    def runSim(self):
        self.questaCtrl.createSimEnv()    
        if not (self.scripts_only):
            subprocess.call(["vsim", self.gui_opt, "-do", self.script_filename])
        self.questaCtrl.cleanEnv()
        self.questaCtrl.printLogs()
        self.postBuild()

        #subprocess.call(["vsim", "-c", "-do", f"{self.folder}/{self.simfile}"])