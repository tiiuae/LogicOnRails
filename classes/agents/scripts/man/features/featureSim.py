class FeatureSim:
    def __init__(self):
        self.option_name = "Sim"
        self.option_content = self.content()
        self.order = 33

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:18px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f3f7fc; color:#1f2d3a; line-height:1.45;">

    <!-- Title -->
    <div style="font-size:30px; font-weight:700; color:#2563eb; margin-bottom:6px;">Simulate Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#1d4ed8;">Simulate:</strong> Runs the project through its simulation flow. Multiple simulators are supported; defines, testbench, waveform, DPI, coverage, and GUI options are combinable to tailor each run. Note: SDF flow is not automatically injected unless manually added via <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">sim_opt</code> and incorporated in the top-level testbench.
      </span>
    </div>

    <!-- Supported Tools -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Supported Simulators &amp; Compatibility</div>
      <div style="font-size:14px; margin-bottom:6px;">
        Full support exists for <strong>Questa</strong>, <strong>ModelSim</strong>, <strong>Vivado</strong>, and <strong>Xcelium</strong>. <em>Future:</em> plans to include Icarus. Be cautious: external or vendor-specific IPs must be tool-compatible. IP compiled for Questa will not necessarily work in Vivado simulation, whereas vendor flows like Quartus/Vivado sometimes allow their IPs to be reused across simulators (e.g., Xcelium/Questa on Vivado-based projects). Netlist simulation works if primitives are provided.
      </div>
    </div>

    <!-- Simulator-based Defines -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:4px;">Simulator-based Defines</div>
      <div style="font-size:14px; margin-bottom:6px;">
        By default the simulator loads defines from both the simulation (<code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">defines_sim</code>) and synthesis (<code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">defines_syn</code>) sections of the YAML or CLI, if they match the expected pattern <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">+define+NAME=VALUE</code>. Additionally, the framework injects <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">SIMULATION</code> and a tool-specific define like <code>QUESTA</code>, <code>MODELSIM</code>, etc., to let scripts differentiate the runtime environment.
      </div>
    </div>

    <!-- Testname -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Test Name</div>
      <div style="font-size:14px;">
        Loaded from the YAML (<code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">default_test</code>) and overridable with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-y</code>. It is emitted both as a define (e.g., <code>DEFAULT_TEST</code>) and via simulator-specific switches such as <code>+test</code> when supported.
      </div>
    </div>

    <!-- Options -->
    <div style="background:#ecfaff; padding:14px; border-left:5px solid #0ea5e9; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#0f4c81; margin-bottom:6px;">Options</div>

      <!-- Simulator selection -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#4338ca; margin-bottom:4px;">Simulator</div>
        <div style="font-size:14px;">
          Select which simulator to drive with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--simulator</code> (aliases: <code>--sim</code>). Supported values: <strong>questa</strong>, <strong>modelsim</strong>, <strong>xcelium</strong>, and <strong>vivado</strong>. Tool compatibility of IP must be respected.
        </div>
      </div>

      <!-- DPI -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#059669; margin-bottom:4px;">DPI and VPI</div>
        <div style="font-size:14px;">
          Enable sourcing and compiling of C/C++ integration code with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--dpi</code>. When active, Questa and Xcelium will pull from the software manifest (<code>manifest_soft.f</code>) for <code>.c</code> / <code>.h</code> files.
        </div>
      </div>

      <!-- Access -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#1d4ed8; margin-bottom:4px;">Access</div>
        <div style="font-size:14px;">
          Controlled with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-a / --access</code>. When enabled, all signal transitions are recorded (slower simulation); when disabled, only signals explicitly included in the waveform file are tracked.
        </div>
      </div>

      <!-- Coverage -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#7c3aed; margin-bottom:4px;">Coverage</div>
        <div style="font-size:14px;">
          Toggle coverage analysis with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--coverage</code>. Available in Questa, ModelSim, and Xcelium (if IMC is installed). Results appear in <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">/reports</code> and a summary may be shown automatically via a browser window.
        </div>
      </div>

      <!-- GUI -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#2563eb; margin-bottom:4px;">GUI</div>
        <div style="font-size:14px;">
          Invoke the graphical user interface with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-g / --gui</code>. When provided without value it defaults to <code>on</code>.
        </div>
      </div>

      <!-- User-based Defines -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#92400e; margin-bottom:4px;">User-based Defines</div>
        <div style="font-size:14px;">
          Use <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-z / --defines_sim</code> to inject custom simulation defines. Accepted patterns include:
          <div style="margin:6px 0;">
            <code style="background:#f1f5f9; padding:3px 6px; border-radius:4px; display:inline-block;">+define+Variable=&lt;Value&gt;</code>,
            <code style="background:#f1f5f9; padding:3px 6px; border-radius:4px; display:inline-block;">+define+UNITS=18</code>,
            <code style="background:#f1f5f9; padding:3px 6px; border-radius:4px; display:inline-block;">+define+Intel</code>,
            <code style="background:#f1f5f9; padding:3px 6px; border-radius:4px; display:inline-block;">+define+Intel+define+UNITS=18</code>
          </div>
          These are merged with the auto-generated simulator-specific and <code>SIMULATION</code> defines.
        </div>
      </div>

      <!-- Testbench -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#0f766e; margin-bottom:4px;">Testbench</div>
        <div style="font-size:14px;">
          Default testbench is sourced from the YAML. Override it with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-t</code> providing the path to an alternate top-level testbench.
        </div>
      </div>

      <!-- Wave -->
      <div style="margin-bottom:4px;">
        <div style="font-size:17px; font-weight:700; color:#a855f7; margin-bottom:4px;">Wave</div>
        <div style="font-size:14px;">
          Preload or specify a waveform file with <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-w</code>. This determines which signals are initially visible when GUI is on.
        </div>
      </div>
    </div>

    <!-- Examples -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim --dpi on</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim -g</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim --simulator vivado</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim -z +define+SUM=18</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls sim -w ./wave/wave.w</code></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Always lint before simulation, ensure IP compatibility with the chosen simulator, and layer simulator-based defines with user overrides for deterministic test runs. Use the GUI flag to inspect waveforms and coverage in real time.
      </div>
    </div>

  </body>
</html>
"""







