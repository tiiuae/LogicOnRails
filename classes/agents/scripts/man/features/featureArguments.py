class FeatureArguments:
    def __init__(self):
        self.option_name = "Arguments"
        self.option_content = self.content()
        self.order = 1

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:18px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f7f9fc; color:#1f2d3a; line-height:1.45;">
    <div style="font-size:30px; font-weight:700; color:#1d4ed8; margin-bottom:4px;">Command-line Arguments</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      Description of all available flags, grouped by logical category. Each flag can be passed in short or long form; where applicable aliases are shown.
    </div>

    <!-- System -->
    <div style="background:#ecfdf5; padding:14px; border-left:5px solid #10b981; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#065f46; margin-bottom:6px;">System</div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>-v / --vendor</strong>: Project vendor name (e.g., altera, xilinx, cadence, microsemi).</li>
        <li><strong>-f / --firmware / --fw</strong>: Firmware path or name; used to locate the <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">.hex</code> file for soft/hardcore.</li>
        <li><strong>-p / --path</strong>: Root project path where the project folder will be created or operated on.</li>
        <li><strong>-U / --uproc</strong>: Indicates microprocessor presence/configuration (hard or soft); signals the framework to load firmware and related subsystem support.</li>
      </ul>
    </div>

    <!-- Simulation -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Simulation</div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>-a / --access / --acc</strong>: Enable signal history capture (access) during simulation; available in tools like Questa, ModelSim, Vivado, Xcelium.</li>
        <li><strong>-c / --coverage / --cov</strong>: Enable coverage collection; results go into the reports directory.</li>
        <li><strong>-i / --dpi</strong>: Enable DPI integration for sourcing and compiling <code>.c</code>/<code>.h</code> from the software manifest.</li>
        <li><strong>-o / --comp_opt / --compile</strong>: Simulation model selection (e.g., netlist vs other modes); controls how the simulation is built/executed.</li>
        <li><strong>-g / --gui</strong>: Toggle graphical interface for the simulation. Optional flag; if provided without value it defaults to <code>on</code>. Enables GUI mode.</li>
        <li><strong>-u / --uvm</strong>: Enable UVM inclusion. Optional; when present without explicit value it defaults to <code>on</code>.</li>
        <li><strong>-y / --default_test</strong>: Default test name for UVM runs when none is explicitly provided.</li>
        <li><strong>-t / --tb / --testbench</strong>: Specify testbench top file or override which testbench to load. Optional; can be used to switch tests dynamically.</li>
        <li><strong>-w / --wave / --wv</strong>: Path to waveform file to preload when GUI is active.</li>
        <li><strong>-s / --simulator / --sim</strong>: Simulator selection (e.g., questa, modelsim, xcelium, vivado).</li>
        <li><strong>-z / --defines_sim / --dsim</strong>: Simulation defines; format typically <code>+define+NAME=VALUE</code> and influences conditional compilation in sim.</li>
      </ul>
    </div>

    <!-- Project -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:6px;">Project</div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>-m / --module_name / --name</strong>: Top module name for the project; overrides default naming.</li>
        <li><strong>-e / --ext_modules / --ext</strong>: Enable external modules as declared in manifests; separates designer RTL from imported vendor pieces.</li>
        <li><strong>-M / --message </strong>: Message level throughout the framework, if message is less than the specified level, it shall not be displayed. possible values are LOG_INF, LOG_WRN, LOG_CRT, LOG_ERR, LOG_DBG.</li>
        <li><strong>-d / --defines_syn / --dsyn</strong>: Synthesis defines; injected into synthesis flow in the tool-specific define format.</li>
        <li><strong>-k / --constraints / --constr</strong>: Path to constraint directory or file set used by synthesis/place-and-route flows.</li>
        <li><strong>-l / --log / --logs</strong>: Enable logging of project commands/output. Optional flag; if provided without a value defaults to <code>on</code>.</li>
      </ul>
    </div>

    <!-- Reports & Actions -->
    <div style="background:#fefce8; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:6px;">Reports &amp; Actions</div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>-r / --report</strong>: Select which report to print; default is <code>summary</code>.</li>
        <li><strong>-x / --ignore</strong>: Substring to filter out or ignore in the generated reports.</li>
        <li><strong>-n / --level</strong>: Level/depth of the utilization report GUI; controls verbosity or detail in the UI.</li>
        <li><strong>-b / --action</strong>: Staged operation string composed of letters (e.g., <code>c</code>=create, <code>s</code>=synth, <code>r</code>=route, <code>d</code>=display) to sequence tasks in one invocation.</li>
      </ul>
    </div>

    <!-- Manifests -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Manifests</div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>-B / --mf_tb</strong>: Testbench manifest path; lists all testbench-related files.</li>
        <li><strong>-R / --mf_rtl</strong>: RTL manifest path; lists RTL source files to be used in synthesis and flow.</li>
        <li><strong>-I / --mf_inc</strong>: Include manifest path; directories to add to include/search path for synthesis, linting, and simulation.</li>
      </ul>
    </div>

    <!-- Summary example -->
    <div style="background:#ffffff; padding:14px; border:1px solid #d1d5db; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#2563eb; margin-bottom:6px;">Example Invocation</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start -b cdsp -v xilinx -m reg64 -z +define+DEBUG=1 -g</code> <span style="color:#555;">→ create, display, synth, place-and-route with Xilinx vendor, top module <strong>reg64</strong>, synthesis define, and GUI enabled.</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#f0f9ff; padding:12px; border-left:5px solid #2563eb; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#1e3a8a;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Combine and override these flags incrementally in YAML and CLI for reproducible flows. Use <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-b</code> to sequence multiple stages without separate invocations.
      </div>
    </div>

  </body>
</html>
"""







