class FeatureFlow:
    def __init__(self):
        self.option_name = "Flow"
        self.option_content = self.content()
        self.order = 2

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:18px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f3f7fc; color:#1f2d3a; line-height:1.45;">

    <!-- Title -->
    <div style="font-size:30px; font-weight:700; color:#1d4ed8; margin-bottom:6px;">Framework Flow</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        High-level orchestration of the framework: how configuration, creation, import, transformation, validation, and delivery stages are composed manually or via macros.
      </span>
    </div>

    <!-- Configuration -->
    <div style="background:#ecfdf5; padding:14px; border-left:5px solid #10b981; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#065f46; margin-bottom:6px;">1. Configuration</div>
      <div style="font-size:14px; margin-bottom:6px;">
        Everything begins with the <strong style="color:#1d4ed8;">YAML</strong> file and manifest definitions. System settings (vendor, firmware, paths), project parameters (module names, constraints, defines), simulation/synthesis/place-and-route overrides, and tool-specific flags (e.g., <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">synth_opt</code>, <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">pr_opt</code>, <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">sta_opt</code>, <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">bit_opt</code>) are declared here.
      </div>
      <div style="font-size:13px; color:#6b7280;">
        Manifests (<code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">rtl</code>, <code>tb</code>, <code>include</code>, etc.) enumerate actual source files consumed downstream.
      </div>
    </div>

    <!-- Core Pipeline -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">2. Core Pipeline</div>

      <!-- Create / Generate -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#2563eb;">Create / Generate</div>
        <div style="font-size:14px;">
          Initializes project structure. Commands like <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">generate</code> or <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">create</code> establish folders, vendor-specific project files, apply YAML defaults, ingest RTL/IP, constraints, and set up testbench/test parameters.
        </div>
      </div>

      <!-- Module Import -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#7c3aed;">Module</div>
        <div style="font-size:14px;">
          Imports template SystemVerilog modules with the standard naming convention (modifiable via <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--module_name</code> and <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--ignore</code>). This augments the design hierarchy before synthesis or simulation.
        </div>
      </div>

      <!-- Synthesis -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#059669;">Synthesis (synth)</div>
        <div style="font-size:14px;">
          Transforms RTL into a mapped netlist. Tool-specific flags from <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">synth_opt</code> are applied. Expected entry points vary per backend (e.g., <code>quartus_syn</code>, <code>synth_1</code>, <code>run_tool -name {SYNTHESIZE}</code>, or Genus).
        </div>
      </div>

      <!-- Place & Route -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#d946ef;">Place &amp; Route (route)</div>
        <div style="font-size:14px;">
          Performs physical implementation, assigning logic to device resources and routing interconnects. Customization comes from <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">pr_opt</code> entries per tool. This stage prepares for timing validation and bitstream generation.
        </div>
      </div>

      <!-- Static Timing Analysis -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#f59e0b;">Timing Analysis (STA)</div>
        <div style="font-size:14px;">
          Validates timing closure. Tool-specific STA flags live in <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">sta_opt</code>. Examples: Quartus uses <code>quartus_sta</code> with the SDC; Vivado extracts timing from <code>impl_1</code>; Libero uses <code>run_tool -name {VERIFYTIMING}</code>; Cadence/Tempus support is limited or absent.
        </div>
      </div>

      <!-- Simulation -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#2563eb;">Simulation (sim)</div>
        <div style="font-size:14px;">
          Executes functional and optionally post-synthesis/netlist simulations. Supported engines: <strong>Questa</strong>, <strong>ModelSim</strong>, <strong>Vivado</strong>, <strong>Xcelium</strong> (future: Icarus). IP compatibility must be respected (e.g., this toolchain does not implicitly translate IP compiled for one simulator to another unless vendor flows allow it). Defines are composed from simulation (<code>defines_sim</code>) and synthesis (<code>defines_syn</code>) sections, plus auto-injected flags like <code>SIMULATION</code> and the tool name (<code>QUESTA</code>, <code>MODELSIM</code>, etc.). Test names (from YAML or <code>-y</code>) are exposed both as defines and via simulator-specific switches. DPI integration (<code>--dpi</code>) pulls C/C++ sources from the software manifest. Access (<code>--access</code>) controls signal history granularity. Coverage (<code>--coverage</code>) is available in select engines and emits reports. GUI (<code>-g</code>) enables interactive introspection of the run.
        </div>
      </div>

      <!-- Upload / Program -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#059669;">Upload / Program (up)</div>
        <div style="font-size:14px;">
          Finalizes and transfers the bitstream or programming data. Backends include <code>quartus_asm</code>, <code>write_bitstream</code>, and <code>run_tool -name {GENERATEPROGRAMMINGDATA}</code>. Tool-specific overrides live in <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">bit_opt</code>. This stage typically follows successful implementation and verification.
        </div>
      </div>
    </div>

    <!-- Visualization & Inspection -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:6px;">3. Visualization &amp; Inspection</div>
      <div style="font-size:14px; margin-bottom:8px;">
        After transformations, users can explore and validate:
      </div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>prj</strong>: Launches the appropriate GUI front-end. For Cadence flows, using <code>-g</code> together with create/synth triggers a final <code>gui_show</code>.</li>
        <li><strong>hier</strong>: Displays a top-level block diagram based on <code>rtl_manifest</code>; modules are clickable to load layers.</li>
        <li><strong>lint</strong>: Static quality checks on RTL/testbench before synthesis, with bypass markers and customizable rules via <code>one_linter</code>.</li>
      </ul>
    </div>

    <!-- Macros & Shortcuts -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">4. Macros &amp; Convenience</div>
      <div style="font-size:14px; margin-bottom:6px;">
        Sequence and encapsulate common multi-step flows:
      </div>
      <ul style="margin:0; padding-left:20px; font-size:14px; list-style-type:disc;">
        <li><strong>start</strong>: Encodes chained actions (create, display, synth, route, etc.) using <code>-b</code> strings like <code>cdsp</code>.</li>
        <li><strong>restart</strong>: Purges existing state then re-executes a sequence.</li>
        <li><strong>auto</strong>: Drives the framework from a macro script for reproducible pipelines.</li>
      </ul>
    </div>

    <!-- Cleanup -->
    <div style="background:#fff5f5; padding:14px; border-left:5px solid #dc2626; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#9b1c1c; margin-bottom:6px;">5. Cleanup</div>
      <div style="font-size:14px;">
        Use <strong>purge</strong> / <strong>delete</strong> to remove generated artifacts, simulator state, and metadata for a clean slate. These operations are destructive and intended for controlled resets.
      </div>
    </div>

    <!-- Example End-to-End -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Example End-to-End Flow</div>
      <div style="font-size:14px;">
        <div>
          <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">
            rls start -b cdsp -v xilinx -m reg64 -z +define+DEBUG=1 -g
          </code>
          <span style="color:#555;">
            → create project, display it, synthesize, place-and-route, simulate with GUI and timing/coverage inspection.
          </span>
        </div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Combine clean YAML profiles with macros (e.g., <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">auto</code>, <code>start</code>) and bake in linting, simulation, and STA to guarantee deterministic hardware build & verification pipelines.
      </div>
    </div>

  </body>
</html>
"""













