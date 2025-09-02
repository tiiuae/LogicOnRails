import subprocess
import inspect
import os

class GowinAgent():
    def __init__ (self, args):
        self.caller_file = inspect.getouterframes(inspect.currentframe(), 2)[0]
        self.frm_path = os.path.abspath(self.caller_file.filename)
        self.folder = f"{self.frm_path}scripts/gowin".replace(os.path.basename(__file__), "")
        self.args = args
        self.create = "gowin_create.tcl"
        self.synth = "gowin_synth.tcl"
        self.implementation = "gowin_implementation.tcl"
        self.bitstream = "gowin_bitstream.tcl"
        #self.sta = "gowin_sta.tcl"
        self.simfile = "gowin_sim.sh"


    def runCreate(self):
        subprocess.call(["gw_sh", f"{self.folder}/{self.create}"])

    def runSynth(self):
        subprocess.call(["gw_sh", f"{self.folder}/{self.synth}"])
        
    def runRoute(self):
        subprocess.call(["gw_sh", f"{self.folder}/{self.implementation}"])
#frm_path/$script_path/gowin/gowin_synth.tcl
    ##def runBit(self):
    ##    subprocess.call(["gowin", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.bitstream}"])

    ##def runSta(self):
    ##    subprocess.call(["gowin", "-nolog", "-nojournal", "-notrace", "-mode",  "tcl", "-source", f"{self.folder}/{self.sta}"])

    def runSim(self):
        subprocess.call(["/bin/bash", f"{self.folder}/{self.simfile}"])        

    def runPrj(self):
        subprocess.call(["gw_ide", f'{self.args.path}/{self.args.module_name}.gprj'])        