class FeatureCreate:
    def __init__(self):
        self.option_name = "Create"
        self.option_content = self.content()
        self.order = 30

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f7fa; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#2563eb; margin-bottom:6px;">Create Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span><strong style="color:#1d4ed8;">Create:</strong> This command creates the project folder and runs the initial configuration.</span>
    </div>

    <!-- Quartus Flow -->
    <div style="background:#ecf9ff; padding:14px; border-left:5px solid #0ea5e9; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#0f4c81; margin-bottom:4px;">Quartus Flow</div>
      <div style="font-size:14px; margin-bottom:8px;">
        The flow starts with <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">project_new</code> to generate a new Quartus project, then:
      </div>
      <ol style="margin:6px 0 0 18px; padding:0; font-size:13px;">
        <li>Family and device assignments are generated.</li>
        <li>Defines configuration loaded from YAML or CLI.</li>
        <li>RTL and external IPs loaded from manifests.</li>
        <li>IPs (again) are instantiated from manifest.</li>
        <li>Altera-specific external configurations are applied.</li>
        <li>.sdc file is loaded.</li>
        <li>SignalTap configuration (if present in <code>/constraints</code>) is loaded.</li>
        <li>Partition (if present) is loaded.</li>
        <li><code>.pin</code> file under constraints is parsed and correct pin assignment is generated.</li>
      </ol>
    </div>

    <!-- Vivado Flow -->
    <div style="background:#f7edff; padding:14px; border-left:5px solid #9333ea; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#6b21a8; margin-bottom:4px;">Vivado Flow</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Starts with <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">create_project</code> to create a new <em>.xprj</em>, then:
      </div>
      <ol style="margin:6px 0 0 18px; padding:0; font-size:13px;">
        <li>RTL and external IPs are loaded.</li>
        <li>Defines from YAML or CLI are parsed into format <code>verilog_define &lt;define_name=[value]&gt;</code>.</li>
        <li>Top architecture is defined.</li>
        <li>Vivado-specific IPs are generated; can be sourced via <code>.tcl</code> (preferred) or <code>.xci</code>.</li>
        <li>Testbench files are loaded and compile order updated.</li>
        <li>.xdc is generated from <code>.sdc</code> and pin info, or loaded if a correctly named one exists.</li>
        <li>Project is saved.</li>
      </ol>
    </div>

    <!-- Libero Flow -->
    <div style="background:#fff8ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:4px;">Libero Flow</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Starts with <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">new_project</code> to create a <em>.prx</em>. Then:
      </div>
      <ol style="margin:6px 0 0 18px; padding:0; font-size:13px;">
        <li><strong style="color:#b91c1c;">(0)</strong> The new_project uses hardcoded lines — review the script before running.</li>
        <li>Include paths loaded by parsing include manifest and invoking <code>set_global_include_path_order</code>.</li>
        <li>RTL and external IPs from manifests are loaded.</li>
        <li>MSS-specific configurations loaded (requires <code>ACTEL_SW_DIR</code> correctly set).</li>
        <li>IPs are sourced from manifest.</li>
        <li>.sdc file is loaded.</li>
        <li>.pdc files are created from <code>.pin</code> or loaded if override is enabled (one <code>iopdc</code> and one <code>fppdc</code> expected).</li>
        <li>Top-level architecture defined.</li>
        <li>Testbench files are loaded; top module set based on YAML.</li>
        <li>Constraints (SDC/PDC) applied per tool.</li>
        <li>Defines are configured for the synthesizer.</li>
      </ol>
    </div>

    <!-- Cadence Flow -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #8b5cf6; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#7c3aed; margin-bottom:4px;">Cadence Flow</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Begins with <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">genus</code> to create a new database project. Then:
      </div>
      <ol style="margin:6px 0 0 18px; padding:0; font-size:13px;">
        <li>Define power rails (<strong>VDD</strong> and <strong>VSS</strong>).</li>
        <li>Load RTL files into database.</li>
        <li>Load external modules.</li>
        <li>Load netlists if present.</li>
        <li>Check design for unresolved references.</li>
        <li>Elaborate and initialize the design.</li>
        <li>Load <code>.sdc</code> into Genus.</li>
      </ol>
    </div>

    <!-- Related Files -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#0f766e; margin-bottom:6px;">Related Files</div>

      <!-- RTL Design -->
      <div style="margin-bottom:12px;">
        <div style="font-size:16px; font-weight:600; color:#2563eb;">RTL Design</div>
        <div style="font-size:13px; margin:4px 0;">
          Correct RTL loading requires proper manifest contents. Manifests must not contain whitespace in paths (even inside comments). Comments use <code>#</code>. Paths are relative to the project's root (not filesystem root). Common manifests: <code>rtl_manifest</code>, <code>ip_manifest</code>, and <code>tb_manifest</code>.
        </div>
      </div>

      <!-- I/O Pins -->
      <div style="margin-bottom:12px;">
        <div style="font-size:16px; font-weight:600; color:#10b981;">I/O Pins</div>
        <div style="font-size:13px; margin:4px 0;">
          Input/output pins can be pre-assigned via the <code>.pin</code> in <code>/constraints</code>. It's a CSV-like file with columns:
        </div>
        <div style="font-size:12px; background:#f1f5f9; padding:8px; border-radius:4px; margin-top:4px;">
          <strong>Pin Name;</strong> Pin Specification; Pin Location; Pin Direction [ I , O ]; Vendor [ xilinx, altera, microsemi ]
        </div>
        <div style="font-size:13px; margin-top:6px;">
          Vivado/Libero translate this into <code>.xdc</code>/<code>.pdc</code>, while Quartus injects directly into <code>.qsf</code>.
        </div>
      </div>

      <!-- STP File -->
      <div style="margin-bottom:12px;">
        <div style="font-size:16px; font-weight:600; color:#d946ef;">STP File</div>
        <div style="font-size:13px; margin:4px 0;">
          SignalTap Probe (STP) is Quartus-specific, enabling runtime signal inspection. To load it, place a valid <code>.stp</code> in <code>/constraints</code> named identically to the project.
        </div>
      </div>

      <!-- SDC -->
      <div style="margin-bottom:12px;">
        <div style="font-size:16px; font-weight:600; color:#f59e0b;">SDC</div>
        <div style="font-size:13px; margin:4px 0;">
          The <code>.sdc</code> carries timing constraints. The script loads it from <code>/constraints</code> if it matches the project name.
        </div>
      </div>

      <!-- Partition -->
      <div style="margin-bottom:12px;">
        <div style="font-size:16px; font-weight:600; color:#9333ea;">Partition</div>
        <div style="font-size:13px; margin:4px 0;">
          (Quartus only) Partition splits the design into subregions. A <code>.partition</code> file under <code>/constraints</code> defines it in CSV style:
        </div>
        <div style="font-size:12px; background:#eef6ff; padding:8px; border-radius:4px; margin-top:4px;">
          Partition Name; Partition hierarchy (e.g. top.designA.partition); Top Level Arch; Vendor; Load enabled; Load From; Dump Syn Enabled; Dump P&amp;R Enabled; dump Path
        </div>
      </div>

      <!-- Altera Configurations -->
      <div style="margin-bottom:4px;">
        <div style="font-size:16px; font-weight:600; color:#065f46;">Altera Configurations</div>
        <div style="font-size:13px; margin:4px 0;">
          The <code>.altera_cnfg</code> file supplies Altera-specific overrides before project creation. Entries here are merged/copied into the final <code>.qsf</code>.
        </div>
      </div>
    </div>

    <!-- Examples -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#312e81; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px; margin:4px 0;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create --vendor xilinx</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create -p &lt;new_prj_path&gt;</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create --uproc &lt;on/off&gt;</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create --dsyn +define+PLL +define+BUS_WIDTH=64</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls create --path &lt;new_prj_path&gt; --module_name reg64 --mf_rtl &lt;manifest_rtl_file&gt;</code></div>
      </div>
    </div>

  </body>
</html>
"""