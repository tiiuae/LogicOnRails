class FeatureUp:
    def __init__(self):
        self.option_name = "Up"
        self.option_content = self.content()
        self.order = 37

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f2f7fb; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#059669; margin-bottom:6px;">Up Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#0f766e;">Up:</strong> Uploads the bitstream to the target/project. Use <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">bit_opt</code> in the YAML to supply per-EDA-tool custom options. <em style="color:#b45309;">(Feature under active development; behavior may be unstable.)</em>
      </span>
    </div>

    <!-- Custom Options Notice -->
    <div style="background:#fff8ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#92400e; margin-bottom:4px;">Custom Bitstream Flags</div>
      <div style="font-size:14px;">
        Extend the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">bit_opt</code> section in the YAML to pass tool-specific upload or generation options without modifying the core flow.
      </div>
      <div style="font-size:13px; background:#ffffff; padding:10px; border-radius:5px; border:1px solid #d1d5db; margin-top:8px;">
        <div><strong>Example snippet:</strong></div>
        <pre style="margin:4px 0; padding:6px; background:#eef4ff; border-radius:4px; font-family:monospace;">
bit_opt:
  quartus: "--some-quartus-flag"
  vivado: "-force -quiet"
  libero: "-extra-upload-param"
        </pre>
        <div style="font-size:12px; color:#6b7280;">
          Each key names the target tool; values are appended during bitstream generation/upload.
        </div>
      </div>
    </div>

    <!-- Flow -->
    <div style="background:#ecfaff; padding:14px; border-left:5px solid #0ea5e9; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#0f4c81; margin-bottom:6px;">Flow</div>

      <!-- Quartus -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#2563eb; margin-bottom:4px;">Quartus</div>
        <div style="font-size:14px;">
          Quartus uses the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">quartus_asm</code> command to assemble and prepare the bitstream for upload.
        </div>
      </div>

      <!-- Vivado -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#9333ea; margin-bottom:4px;">Vivado</div>
        <div style="font-size:14px;">
          Vivado generates the bitstream via the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">write_bitstream</code> command.
        </div>
      </div>

      <!-- Libero -->
      <div style="margin-bottom:12px;">
        <div style="font-size:17px; font-weight:700; color:#92400e; margin-bottom:4px;">Libero</div>
        <div style="font-size:14px;">
          Libero invokes <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">run_tool -name {GENERATEPROGRAMMINGDATA}</code> to produce the programming data (bitstream).
        </div>
      </div>

      <!-- Cadence -->
      <div style="margin-bottom:4px;">
        <div style="font-size:17px; font-weight:700; color:#7c3aed; margin-bottom:4px;">Cadence</div>
        <div style="font-size:14px;">
          <strong style="color:#b91c1c;">No current support</strong> for Innovus GDSII generation in this flow.
        </div>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls up</code>
      </div>
    </div>

    <!-- Warning -->
    <div style="background:#fff7ed; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Warning:</div>
      <div style="font-size:13px; margin-top:4px;">
        Bitstream upload/generation logic is still evolving. Failures may occur silently—always verify output integrity before deployment.
      </div>
    </div>

  </body>
</html>
"""


