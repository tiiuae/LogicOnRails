# =============================================================================
# Project:        Logic on Rails
# File:           xilinxAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Top level class - Xilinx 
# =============================================================================
import subprocess
import inspect
import os
import sys

class XilinxAgent():
    def __init__ (self, args):
        self.script_filename = f'./_vivadoScript.tcl'
        self.log_filename = f'./_vivadoLog.txt'
        os.environ["vivado_script_name"] = self.script_filename
        os.environ["vivado_log_name"] = self.log_filename

        self.vendor = os.getenv('vendor')
        self.reports = os.getenv('reports_path')
        self.scripts_only = (os.getenv('scripts_only') == "on")

        #import controller class
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/vivado".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from vivadocontroller import VivadoController
        self.vivadoCtrl = VivadoController()

        #LOG FILES
        self.args = args
        self.creationLogFile = f"{self.reports}/vivado.log"
        self.synthLogFile    = f"{self.args.path}/{self.args.module_name}.runs/synth_1/runme.log"
        self.routeLogFile    = f"{self.args.path}/{self.args.module_name}.runs/impl_1/runme.log"
        self.staLogFile      = f""
        self.bitLogFile      = f""

        #TO BE DELETED
        #self.create = "create.tcl"
        #self.synth = "synth.tcl"
        #self.implementation = "implementation.tcl"
        #self.bitstream = "bitstream.tcl"
        #self.sta = "sta.tcl"
        #self.simfile = "sim.sh"


    def runCreate(self):
        self.vivadoCtrl.createPrj()
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        self.vivadoCtrl.printLogs(self.creationLogFile)
        #subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.create}"])

    def runSynth(self):
        self.vivadoCtrl.createSynth()  
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        self.vivadoCtrl.printLogs(self.synthLogFile)
        #subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.synth}"])
    
    def runRoute(self):
        self.vivadoCtrl.createPlaceRoute()
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        self.vivadoCtrl.printLogs(self.routeLogFile)
        #subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.implementation}"])

    def runSta(self):
        self.vivadoCtrl.createSTA()   
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        self.vivadoCtrl.printLogs(self.staLogFile)
        #subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.sta}"])

    def runBit(self):
        self.vivadoCtrl.createBitStream()
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        self.vivadoCtrl.printLogs(self.bitLogFile)
        #subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.bitstream}"])

    def runSim(self):
        self.vivadoCtrl.createSim()        
        if not (self.scripts_only):
            subprocess.call(["vivado", "-nolog", "-nojournal", "-notrace", "-mode",  "batch", "-source", f"{self.script_filename}"])
        self.vivadoCtrl.cleanEnv()
        #self.vivadoCtrl.printLogs()
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.simfile}"])        

    def runPrj(self):
        subprocess.call(["vivado", f'{self.args.path}/{self.args.module_name}.xpr'])        