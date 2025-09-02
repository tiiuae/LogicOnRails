class FeatureSTA:
    def __init__(self):
        self.option_name = "STA"
        self.option_content = self.content()
        self.order = 35

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f0f4f8; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#d946ef; margin-bottom:6px;">STA Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#7c3aed;">STA:</strong> Performs static timing analysis on the synthesized design. Add tool-specific flags in the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">sta_opt</code> section of the YAML to inject custom options per EDA tool. <em>Note:</em> The STA flow is currently incomplete and lacks uniform support across vendors; the Quartus path is the most mature today.
      </span>
    </div>

    <!-- Custom Options -->
    <div style="background:#f9f5ff; padding:14px; border-left:5px solid #8b5cf6; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#5b21b6; margin-bottom:4px;">Custom Flags via <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">sta_opt</code></div>
      <div style="font-size:14px; margin-bottom:6px;">
        Extend <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">sta_opt</code> in YAML to pass vendor-specific timing analysis options without modifying internal flow logic.
      </div>
      <div style="font-size:13px; background:#ffffff; padding:10px; border-radius:5px; border:1px solid #d1d5db; margin-bottom:4px;">
        <div><strong>Example snippet:</strong></div>
        <pre style="margin:4px 0; padding:6px; background:#eef4ff; border-radius:4px; font-family:monospace;">
sta_opt:
  quartus: "--collapse_registers --report_timing"
  vivado: "-delay_analysis full"
  libero: "-verify_timing_extra"
        </pre>
        <div style="font-size:12px; color:#6b7280;">
          Each key targets a tool; the value is appended during the STA invocation for that tool.
        </div>
      </div>
    </div>

    <!-- Flow -->
    <div style="background:#ffffff; padding:14px; border-radius:6px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Flow</div>

      <!-- Quartus -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#2563eb; margin-bottom:4px;">Quartus</div>
        <div style="font-size:14px;">
          Quartus runs <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">quartus_sta</code> with the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">--sdc</code> argument pointing to the project's SDC file.
        </div>
      </div>

      <!-- Vivado -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#9333ea; margin-bottom:4px;">Vivado</div>
        <div style="font-size:14px;">
          Vivado loads the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">impl_1</code> implementation generated after place-and-route and runs <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">report_timing_summary</code> on it.
        </div>
      </div>

      <!-- Libero -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#92400e; margin-bottom:4px;">Libero</div>
        <div style="font-size:14px;">
          Libero opens the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">.prjx</code> project and invokes <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">run_tool -name {VERIFYTIMING}</code>.
        </div>
      </div>

      <!-- Cadence -->
      <div style="margin-bottom:4px;">
        <div style="font-size:17px; font-weight:700; color:#7c3aed; margin-bottom:4px;">Cadence</div>
        <div style="font-size:14px;">
          <strong style="color:#b91c1c;">No current support for Tempus.</strong>
        </div>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls sta</code>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Layer <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">sta_opt</code> with upstream overrides (e.g., <code>vendor</code>, <code>module_name</code>, <code>synth_opt</code>, <code>route</code>) to refine timing analyses in CI or multi-tool flows.
      </div>
    </div>

  </body>
</html>
"""

