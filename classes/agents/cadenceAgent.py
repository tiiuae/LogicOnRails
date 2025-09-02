# =============================================================================
# Project:        Logic on Rails
# File:           cadenceAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    Top level class - Cadence 
# =============================================================================

import subprocess
import inspect
import os
import sys

class CadenceAgent():
    def __init__ (self, args):
        self.gscript_filename = f'./_genusScript.tcl'
        self.glog_filename = f'./_genusLog.txt'
        self.mscript_filename = f'./_modusScript.tcl'
        self.mlog_filename = f'./_modusLog.txt'
        os.environ["genus_script_name"] = self.gscript_filename
        os.environ["genus_log_name"] = self.glog_filename
        os.environ["modus_script_name"] = self.mscript_filename
        os.environ["modus_log_name"] = self.mlog_filename

        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.args   = args
        self.scripts_only = (os.getenv('scripts_only') == "on")

        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/cadence".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)

        from genuscontroller import GenusController
        from moduscontroller import ModusController
        self.genusCtrl = GenusController()
        self.modusCtrl = ModusController()

        self.create = "create.tcl"
        self.synth = "synth.tcl"
        self.route = "route.tcl"
        self.prj = "prj.tcl"

    def runCreate(self):
        print(f"Cadence controller does not support creation")

    def runSynth(self):
        self.genusCtrl.createSynthEnv()
        if not (self.scripts_only):
            subprocess.call(["genus", f"-f {self.folder}/{self.create}"])
        self.genusCtrl.cleanEnv()
        self.genusCtrl.printLogs()

    def runBit(self):
        self.modusCtrl.createModusEnv()
        if not (self.scripts_only):
            subprocess.call(["modus", f"-file {self.folder}/{self.create}"])
        self.modusCtrl.cleanEnv()
        self.modusCtrl.printLogs()

    def runRoute(self):
        subprocess.call(["innovus", f"-stylus -files {self.folder}/{self.route}"])


    def runPrj(self):
        subprocess.call(["genus", f"-f {self.folder}/{self.prj}"])
