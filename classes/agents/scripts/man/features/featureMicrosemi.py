class FeatureMicrosemi:
    def __init__(self):
        self.option_name = "Microsemi"
        self.option_content = self.content()
        self.order = 11

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:20px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f9fafb; color:#1f2937; line-height:1.6;">

    <!-- Title -->
    <h1 style="color:#047857; font-size:28px; font-weight:700; margin-bottom:8px;">Microsemi Flow</h1>

    <!-- Overview -->
    <p style="font-size:15px; color:#4b5563; margin-bottom:20px;">
      The <strong>Microsemi flow</strong> integrates <strong>Libero SoC</strong> for synthesis (via Synplify Pro), 
      place-and-route, static timing analysis (STA), and debug. Simulation is performed externally using 
      <strong>ModelSim</strong> or <strong>Questa</strong>.
    </p>

    <!-- Quick Info -->
    <div style="background:#ecfdf5; border-left:5px solid #10b981; padding:14px; border-radius:6px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#065f46; margin-bottom:6px;">Environment</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li><strong>Vendor:</strong> Microsemi</li>
        <li><strong>Tool:</strong> Libero SoC</li>
        <li><strong>Simulator:</strong> ModelSim / Questa</li>
        <li><strong>Linter:</strong> Verilator</li>
      </ul>
    </div>

    <!-- Requirements -->
    <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#1d4ed8; margin-bottom:6px;">Requirements</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li>Libero must be installed and available in <code>$PATH</code>.</li>
        <li>The <strong>constraints</strong> folder must contain an <code>.sdc</code> file named after the top module.</li>
        <li>If a <code>&lt;module_name&gt;.pin</code> file exists:
          <ul>
            <li>The tool will generate an <code>io.pdc</code> file (same name as the top module).</li>
            <li>A corresponding <code>fppdc</code> file must also be present in the same constraints folder.</li>
          </ul>
        </li>
        <li>If no pin/fppdc files exist, you may enable the <strong>pdc_override</strong> option in the config manifest:
          <ul>
            <li>This forces the script generator to look inside a specified folder.</li>
            <li>The folder must contain:
              <ul>
                <li>an <code>io/</code> subdirectory with one or more <code>iopdc</code> files</li>
                <li>a <code>fp/</code> subdirectory with one or more <code>fppdc</code> files</li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </div>

    <!-- Flow -->
    <div style="background:#fff7ed; border-left:5px solid #d97706; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#92400e; margin-bottom:6px;">Flow</h2>
      <p style="font-size:14px;">To run the Microsemi flow, configure your project YAML file with <code>vendor: microsemi</code>, then populate the manifests:</p>
      <ol style="font-size:14px; margin-left:20px;">
        <li>Add RTL files to <code>manifest_rtl</code>.</li>
        <li>Add testbench files to <code>manifest_tb</code>. If <code>.c</code> files are required for DPI, list them in the <code>software</code> manifest.</li>
        <li>Add IPs to the <code>ip</code> manifest:
          <ul>
            <li>Each IP must be provided as a <code>.tcl</code> file.</li>
            <li>IPs can be exported directly from the Libero GUI (<em>Right-click → Export</em>).</li>
            <li><strong>SmartDesigns</strong> are supported.</li>
          </ul>
        </li>
      </ol>

      <p style="margin-top:12px; font-size:14px;"><strong>Command sequence:</strong></p>
      <pre style="background:#f3f4f6; padding:10px; border-radius:6px; font-size:13px; overflow:auto;">
rls create
rls lint
rls sim
rls synth
rls route
rls sta
rls bit
      </pre>
    </div>

    <!-- TODO -->
    <div style="background:#fee2e2; border-left:5px solid #dc2626; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#b91c1c; margin-bottom:6px;">TODO / Known Limitations</h2>
      <ul style="font-size:14px; margin-left:20px;">
        <li><strong>Simulation:</strong> Direct Libero simulation is not supported; the tool runs ModelSim/Questa instead.</li>
        <li><strong>Netlist simulation:</strong> Only supported if the user manually generates the netlist and lists it in <code>rtl/tb</code> manifests.</li>
        <li><strong>STA reports:</strong> STA runs, but report fetching/parsing is incomplete.</li>
        <li><strong>MSS support:</strong> MSS configuration files are supported, but firmware flow integration requires improvement.</li>
        <li><strong>Bitstream generation:</strong> Untested.</li>
        <li><strong>Bitstream upload:</strong> Untested.</li>
        <li><strong>On-chip scope:</strong> Not supported.</li>
        <li><strong>Logic partitions:</strong> Not supported.</li>
        <li><strong>Partial reconfiguration:</strong> Not supported.</li>
      </ul>
    </div>

  </body>
</html>
"""