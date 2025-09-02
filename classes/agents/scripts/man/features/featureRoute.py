class FeatureRoute:
    def __init__(self):
        self.option_name = "Route"
        self.option_content = self.content()
        self.order = 34

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f9fb; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#d946ef; margin-bottom:6px;">Route Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#7c3aed;">Route:</strong> Performs place-and-route for the synthesized design. This finalizes physical implementation by mapping logic to devices and routing interconnects.
      </span>
    </div>

    <!-- Custom Options -->
    <div style="background:#f3f0ff; padding:14px; border-left:5px solid #9333ea; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#5b21b6; margin-bottom:4px;">Custom Place &amp; Route Flags via <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">pr_opt</code></div>
      <div style="font-size:14px; margin-bottom:6px;">
        To inject tool-specific place-and-route options, extend the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">pr_opt</code> section in the YAML. This enables fine-grained control per EDA tool without modifying core flow logic.
      </div>
      <div style="font-size:13px; background:#ffffff; padding:10px; border-radius:5px; border:1px solid #d1d5db; margin-bottom:4px;">
        <div><strong>Example snippet:</strong></div>
        <pre style="margin:4px 0; padding:6px; background:#eef4ff; border-radius:4px; font-family:monospace;">
pr_opt:
  xilinx: "-directive Timing -routing_effort high"
  altera: "--place_optimize balanced"
  cadence: "-some_innovus_route_flag value"
        </pre>
        <div style="font-size:12px; color:#6b7280;">
          Each key corresponds to the target tool; the value is appended during the route invocation for that tool.
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
          Quartus uses <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">quartus_fit</code> command to start the synthesizer.
        </div>
      </div>

      <!-- Vivado -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#6b21a8; margin-bottom:4px;">Vivado</div>
        <div style="font-size:14px; margin-bottom:4px;">
          Vivado will target and run <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">impl_1</code>; it resets it and re-executes the implementation flow.
        </div>
      </div>

      <!-- Libero -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#92400e; margin-bottom:4px;">Libero</div>
        <div style="font-size:14px; margin-bottom:4px;">
          Libero runs <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">run_tool -name {PLACEROUTE}</code> to execute the synthesis flow.
        </div>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #7c3aed; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#4f46e5; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls route</code></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #f59e0b; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Combine <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">pr_opt</code> with upstream overrides (e.g., <code>vendor</code>, <code>module_name</code>, <code>synth_opt</code>) to tailor multi-tool CI pipelines or perform experimental P&R strategies.
      </div>
    </div>

  </body>
</html>
"""
