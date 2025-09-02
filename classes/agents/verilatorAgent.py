# =============================================================================
# Project:        Logic on Rails
# File:           verilatorAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Verilator 
# =============================================================================

import sys
import subprocess
import inspect
import os

class VerilatorAgent():
    def __init__(self, args):
        self.script_filename = f'./_verilatorScript.tcl'
        self.log_filename = f'./_verilatorLog.txt'
        self.lint_result = f'./_verilatorLintResult.rpt'
        os.environ["verilator_script_name"] = self.script_filename
        os.environ["verilator_log_name"] = self.log_filename
        os.environ["verilator_lint_result"] = self.lint_result
        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.scripts_only = (os.getenv('scripts_only') == "on")
        self.args   = args
        
        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/verilator".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from verilatorcontroller import VerilatorController
        self.vrltorCtrl = VerilatorController()

        #LOG FILES
        self.args = args
        self.lintLogFile = f"{self.reports}/{self.lint_result}"

    def postLint(self):
        self.vrltorCtrl.postLintHandle()

    def runLint(self):
        subprocess.call(["/bin/bash", f"{self.folder}/one_lint.sh"])
        self.vrltorCtrl.createLintEnv()
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
        self.postLint()  
        self.vrltorCtrl.cleanEnv()
        self.vrltorCtrl.printLogs(self.lintLogFile)
        #to be deprecated
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.file}", self.args.tb])
