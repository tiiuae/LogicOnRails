class FeatureSynth:
    def __init__(self):
        self.option_name = "Synth"
        self.option_content = self.content()
        self.order = 33

    def content(self):
      return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f7fa; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#059669; margin-bottom:6px;">Synth Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#0f766e;">Synth:</strong> Synthesizes the project according to the current configuration.
      </span>
    </div>

    <!-- Custom Options -->
    <div style="background:#eefaf6; padding:14px; border-left:5px solid #10b981; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#047857; margin-bottom:4px;">Custom Options via <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">synth_opt</code></div>
      <div style="font-size:14px; margin-bottom:6px;">
        To pass tool-specific synthesis flags, augment the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">synth_opt</code> section in the YAML. This allows injecting extra arguments per EDA tool without changing core scripts. (Work in progress)
      </div>
      <div style="font-size:13px; background:#ffffff; padding:10px; border-radius:5px; border:1px solid #d1d5db; margin-bottom:4px;">
        <div><strong>Example snippet:</strong></div>
        <pre style="margin:4px 0; padding:6px; background:#f1f5f9; border-radius:4px; font-family:monospace;">
synth_opt:
  xilinx: "-directive Performance"
  altera: "--optimize-level=high"
  cadence: "-some_genus_flag value"
        </pre>
        <div style="font-size:12px; color:#6b7280;">
          Each key is the target EDA tool; the value is appended when invoking synthesis for that tool.
        </div>
      </div>
    </div>

    <!-- Flow -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Flow</div>

      <!-- Quartus -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#0f4c81; margin-bottom:4px;">Quartus</div>
        <div style="font-size:14px; margin-bottom:4px;">
          Quartus uses <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">quartus_syn</code> command to start the synthesizer.
        </div>
      </div>

      <!-- Vivado -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#6b21a8; margin-bottom:4px;">Vivado</div>
        <div style="font-size:14px; margin-bottom:4px;">
          Vivado will target and run <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">synth_1</code>; it resets it and re-executes the synthesis flow.
        </div>
      </div>

      <!-- Libero -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#92400e; margin-bottom:4px;">Libero</div>
        <div style="font-size:14px; margin-bottom:4px;">
          Libero runs <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">run_tool -name {SYNTHESIZE}</code> to execute the synthesis flow.
        </div>
      </div>

      <!-- Cadence -->
      <div style="margin-bottom:4px;">
        <div style="font-size:17px; font-weight:700; color:#7c3aed; margin-bottom:4px;">Cadence</div>
        <div style="font-size:14px; margin-bottom:4px;">
          The synthesis flow in Genus proceeds as follows:
        </div>
        <ol style="margin:6px 0 0 18px; padding:0; font-size:13px;">
          <li>Initially, Genus loads the library search directory and then loads the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">.lib</code> file defined in the YAML.</li>
          <li>If the hardcoded physical-aware switch is enabled, Genus loads the LEF, QRC, and captables.</li>
          <li>If the hardcoded scan-chain switch is enabled, Genus configures the DFT flow by creating pins and defining scan-chain methodology.</li>
          <li>Genus runs synthesis, mapping, and optimization steps, generating intermediate netlists at each stage.</li>
          <li>The database is saved.</li>
          <li>If scan-chain is enabled, Genus performs an additional <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">syn_opt</code> run, then writes the scan definition and ATPG files.</li>
          <li>Genus writes the updated netlist, <code>.sdc</code>, and corresponding <code>.sdf</code>.</li>
          <li>Timing, area, and power reports are generated.</li>
        </ol>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls synth</code></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffef6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Combine <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">synth_opt</code> with other YAML overrides (e.g., <code>vendor</code>, <code>module_name</code>) to target different flows in CI or multi-platform builds.
      </div>
    </div>

  </body>
</html>
"""


