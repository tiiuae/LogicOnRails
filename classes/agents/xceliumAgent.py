# =============================================================================
# Project:        Logic on Rails
# File:           xceliumAgent
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        aug 2025
# Description:    Top level class - Xcelium 
# =============================================================================

import subprocess
import os
import inspect
import sys
import os
import shutil


class XceliumAgent():
    def __init__(self, args):
        self.script_filename = f'./_xceliumScript.sh'
        self.log_filename = f'./_xceliumLog.txt'
        self.lint_filename = f'./_xceliumLint.sh'
        os.environ["xcelium_script_name"] = self.script_filename
        os.environ["xcelium_log_name"] = self.log_filename
        os.environ["xcelium_lint_name"] = self.lint_filename

        self.xrun_dir = f'./xdir'
        self.xrun_script_dir = f'{self.xrun_dir}/xcelium'
        os.environ["xrun_dir"] = self.xrun_dir
        os.environ["xrun_script_dir"] = self.xrun_script_dir

        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/xcelium".replace(os.path.basename(__file__), "")
        sys.path.insert(0, self.folder)
        from xceliumcontroller import XceliumController
        self.xrunCtrl = XceliumController()

        self.args   = args
        self.scripts_only = os.getenv('scripts_only')

        #do be deprecated
        self.simfile = "sim.sh"
        self.lintfile = "lint.sh"

    def preBuild(self):
        if (self.args.vendor == "altera"):
            if self.xrunCtrl.manifests["ips"] and any("ALTERA:" in s for s in self.xrunCtrl.manifests["ips"]):
                rmpaths = [
                    f"{self.xrun_dir}/common/modelsim_files.tcl",
                    f"{self.xrun_dir}/common/riviera_files.tcl",
                    f"{self.xrun_dir}/common/vcs_files.tcl",
                    f"{self.xrun_dir}/common/vcsmx_files.tcl",
                    f"{self.xrun_dir}/mentor",
                    f"{self.xrun_dir}/synopsys",
                    f"{self.xrun_dir}/aldec"
                ]
                if not os.path.isdir(self.xrun_script_dir):
                    print("ALTERA IP FLOW IN XCELIUM, BE SURE THE PROJECT IS CORRECTLY CREATED ")
                    subprocess.call(["ip-setup-simulation", f"--quartus-project=./{self.args.path}/{self.args.module_name}", f"--output-directory={self.xrun_dir}/", "--use-relative-paths"])
                    for p in rmpaths:
                            print(p)
                            if os.path.isdir(p): shutil.rmtree(p)
                            elif os.path.exists(p): os.remove(p)

    def runSim(self):
        self.preBuild()
        self.xrunCtrl.createSimEnv()        
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
            self.xrunCtrl.cleanEnv()
            self.xrunCtrl.printLogs()
        #to be deprecated
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.simfile}"])

    def runLint(self):
        self.xrunCtrl.createLintEnv()
        if not (self.scripts_only):
            subprocess.call(["/bin/bash", f"{self.script_filename}"])
            self.xrunCtrl.cleanEnv()  
        #to be deprecated
        #subprocess.call(["/bin/bash", f"{self.folder}/{self.lintfile}"])
