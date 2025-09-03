# 🛠️ Logic On Rails — Multi-Vendor EDA Automation Framework

Logic On Rails is a modular automation system designed to unify FPGA/ASIC flows across multiple vendors and tools.  
It simplifies project setup, synthesis, simulation, static timing analysis (STA), place-and-route (P&R), bitstream generation, and debug — while remaining vendor-agnostic.  

## ✨ Version:

1.0.2 - Anchieta

## ✨ Features

- **Vendor Support**
  - **Xilinx**: Vivado (synth, P&R, STA, bitstream, ILA/ChipScope debug)  
  - **Microsemi**: Libero SoC (Synplify Pro, STA, SmartDesigns, MSS support)  
  - **Altera/Intel**: Quartus Prime (SignalTap, Nios II, partitions, Platform Designer IPs)  
  - **Cadence**: Genus/Innovus/Tempus/Modus/Conformal (beta flow, Genus and Xcelium fully tested)  
- **Simulation**  
  - Vivado Simulator, ModelSim/Questa, Xcelium  
- **Linting**  
  - Verilator (cross-vendor)  
- **Manifest-driven design**  
  - YAML + file manifests control RTL, TB, IP, software sources, and constraints  
- **Reproducible flows**  
  - Command-line arguments + YAML configs for deterministic builds  
- **Extensible**  
  - Easily add new vendor flows or EDA tool integrations  

---

## 📦 Installation

Clone the repository and set up your environment:

```bash
git clone https://github.com/<your-user>/<your-repo>.git

add the following lines to your bashrc
PATH=$PATH:"<yourpath>/LogicOnRails/"
complete -W "auto lint generate purge prj start restart module hier update create delete synth bit sta sim route up report populate help man" rls
```

## 📦 Usage

Create project environment
rls create
Run lint checks with Verilator
rls lint
Run simulation (Vivado, Questa, or Xcelium)
rls sim
Run synthesis
rls synth
Place & Route
rls route
Static Timing Analysis
rls sta
Bitstream generation
rls bit

## 📦 Structure

project/
├── manifests/
│   ├── rtl.manifest       # RTL sources
│   ├── tb.manifest        # Testbenches
│   ├── ip.manifest        # Vendor IPs (xci, qsys, tcl, etc.)
│   ├── software.manifest  # Software sources (.c/.h)
│   └── inc.manifest       # Include directories
├── constraints/
│   ├── top.sdc / top.xdc / top.pdc
│   ├── top.pin
│   └── vendor_specific.cnfg
├── reports/
│   └── ...                # Generated reports/logs
└── config.yaml            # Project configuration


## 🔮 Roadmap

[] Improve VPI and coverage support in Vivado/Questa
[] Enhance STA report parsing across all vendors
[] Extend MSS/Nios/MicroBlaze firmware flow integration
[] Support on-chip scopes (ILA, SignalTap, Libero)
[] Add partial reconfiguration support
[] Full Cadence flow controllers (Tempus, Innovus, Jasper, Palladium, Protium)

