class FeatureReport:
    def __init__(self):
        self.option_name = "Report"
        self.option_content = self.content()
        self.order = 36

    def content(self):
        return """
Displays Synthesis/Area/Timing Report (quartus only)
  
  GUI - 

  By default, the reports are parsed from the respective quartus log and printed in the terminal, 
  the user has the option to display the results in a text editor like Gedit, if the option -g is used.


  Ignore - 

  The reports may present information that is not relevant, for instance, synthesis information for third party IP. If the user wants
  to surpress said informatio, it can use the option -x when calling the command


  Level - 

  To be used in the utilization report. Show the utilization percentage in each hierarchycal level.


  Reports -

  The available reports are:

  Synthesis

  -> syn_summary - Synthesis summary

  -> fsm - FSM report

  -> register - Register report

  -> mux - MUX report

  -> megafunction - IP report

  -> syn_netlist - Post synthesis netlist

  -> resources - resources utilization report

  -> ram - BRAM report

  -> warnings - Warnings report


  Place and Route

  -> summary - P&R summary
  
  -> settings - Settings used during P&R
  
  -> netlist - post place and route netlist
  
  -> bank - Bank usage report
  
  -> io_warning - I/O warnings
  
  -> controll - Controll signal information
  
  -> statistics - Partition statistics
  
  -> usage - Usage information
  
  -> utilization - Utilization in percentage


  Timing

  -> path - SDC Paths

  -> clocks - Report clocks
  
  -> time - Timing closure summary
  
  -> frequency - FMax report
  
  -> setup - Setup report
  
  -> hold - Hold report
  
  -> signoff - Design assistant report
  
  -> ignored - Ignored constraints report
  
  -> empty - Empty collection


  Example - 

  rls report -r hold

  rls report -r summary -g

  rls report -r utilization -g -l 2
  
"""

    def content(self):
        return """to be reviewed"""