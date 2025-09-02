# =============================================================================
# Project:        Logic on Rails
# File:           edaController
# Author:         Matheus Lemes Ferronato /in/matheusferronato/
# Modified by:
# Created:        jul 2025
# Description:    Generic call for different classes 
# =============================================================================

from .alteraAgent import AlteraAgent
from .xilinxAgent import XilinxAgent
from .gowinAgent import GowinAgent
from .questaAgent import QuestaAgent
from .xceliumAgent import XceliumAgent
from .verilatorAgent import VerilatorAgent
from .microsemiAgent import MicrosemiAgent
from .modelsimAgent import ModelSimAgent
from .cadenceAgent import CadenceAgent

import os

class EDAController():
    def __init__(self, args, linter):
        self.vendor = args.vendor.lower()
        self.simulator = args.simulator.lower()
        self.linter = linter.lower()
        self.agtVendor = self.select_vendor(self.vendor, args)
        self.agtSim = self.select_sim(self.simulator, self.vendor, args)
        self.agtLint = self.select_linter(self.linter, args)

    #### VENDOR #####        
    def select_vendor(self, vendor, args):
        if (vendor == "altera"): return AlteraAgent(args)
        if (vendor == "cadence"): return CadenceAgent(args)
        elif (vendor == "gowin"): return GowinAgent(args)
        elif (vendor == "microsemi"): return MicrosemiAgent(args)
        else: return XilinxAgent(args)
        
    #### SIMULATOR #####
    def select_sim(self, simulator, vendor, args):
        if (simulator == "modelsim"):
            if (vendor == "gowin"): return  GowinAgent(args)
            else: return ModelSimAgent(args)
        elif (simulator == "questa"): return QuestaAgent(args)
        elif (simulator == "vivado"): return XilinxAgent(args)
        elif (simulator == "xcelium"): return XceliumAgent(args)
        elif (simulator == "cadence"): return XceliumAgent(args)
        else: return ModelSimAgent(args)

    #### LINTER #####
    def select_linter(self, linter, args):
        if (linter == "verilator"): return VerilatorAgent(args)
        else: return XceliumAgent(args) 
          