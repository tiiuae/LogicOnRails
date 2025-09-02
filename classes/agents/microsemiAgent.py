# =============================================================================
# Project:        Logic on Rails
# File:           alteraAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Microsemi 
# =============================================================================

import subprocess
import inspect
import os
import sys

class MicrosemiAgent():
    def __init__ (self, args):
        self.script_filename = f'./_liberoScript.tcl'
        self.log_filename = f'./_liberoLog.txt'
        os.environ["libero_script_name"] = self.script_filename
        os.environ["libero_log_name"] = self.log_filename

        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.args   = args
        self.scripts_only = (os.getenv('scripts_only') == "on")

        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/libero".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from liberocontroller import LiberoController
        self.liberoCtrl = LiberoController()

        #LOG FILES
        self.args = args
        self.creationLogFile = ""
        self.synthLogFile    = f"{self.args.path}/{self.args.module_name}/synthesis/synlog/{self.args.module_name}_compiler.srr"

        #TO BE REMOVED
        self.create = "create.tcl"
        self.synth = "synth.sh"
        self.implementation = "implementation.tcl"
        self.bitstream = "bitstream.tcl"
        self.sta = "sta.tcl"
        self.simfile = "sim.tcl"


    def runCreate(self):
        self.liberoCtrl.createPrj()
        if not (self.scripts_only):
            subprocess.call(["libero", f"SCRIPT:{self.script_filename}"])
        self.liberoCtrl.cleanEnv()
        self.liberoCtrl.printLogs(self.creationLogFile)
        #subprocess.call(["libero", f"SCRIPT:{self.folder}/{self.create}"])

    def runSynth(self):
        self.liberoCtrl.createSynth()
        if not (self.scripts_only):
            subprocess.call(["libero", f"SCRIPT:{self.script_filename}"])
        self.liberoCtrl.cleanEnv()
        print(self.synthLogFile)
        self.liberoCtrl.printLogs(self.synthLogFile)
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.synth}"])
    
    def runRoute(self):
        self.liberoCtrl.createRoute()
        if not (self.scripts_only):
            subprocess.call(["libero", f"SCRIPT:{self.script_filename}"])
        self.liberoCtrl.cleanEnv()
        self.liberoCtrl.printLogs()
        #subprocess.call(["libero", f"SCRIPT:{self.folder}/{self.implementation}"])

    def runBit(self):
        self.liberoCtrl.createBitStream()
        if not (self.scripts_only):
            subprocess.call(["libero", f"SCRIPT:{self.script_filename}"])
        self.liberoCtrl.cleanEnv()
        self.liberoCtrl.printLogs()
        #subprocess.call(["libero", f"SCRIPT:{self.folder}/{self.bitstream}"])
    
    def runSta(self):
        self.liberoCtrl.createSTA()
        if not (self.scripts_only):
            subprocess.call(["libero", f"SCRIPT:{self.script_filename}"])
        self.liberoCtrl.cleanEnv()
        self.liberoCtrl.printLogs()
        #subprocess.call(["libero", f"SCRIPT:{self.folder}/{self.sta}"])

    def runSim(self):
        print("TODO")
        #subprocess.call(["libero", f"SCRIPT:{self.folder}/{self.simfile}"])

    def runPrj(self):
        subprocess.call(["libero", f'{self.args.path}/{self.args.module_name}/{self.args.module_name}.prjx'])        