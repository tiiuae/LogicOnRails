class FeatureXilinx:
    def __init__(self):
        self.option_name = "Xilinx"
        self.option_content = self.content()
        self.order = 12

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:20px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f9fafb; color:#1f2937; line-height:1.6;">

    <!-- Title -->
    <h1 style="color:#9333ea; font-size:28px; font-weight:700; margin-bottom:8px;">Xilinx Flow</h1>

    <!-- Overview -->
    <p style="font-size:15px; color:#4b5563; margin-bottom:20px;">
      The <strong>Xilinx flow</strong> integrates <strong>Vivado</strong> for synthesis, simulation, place-and-route,
      static timing analysis (STA), and on-chip debug (ChipScope/ILA). It is designed for FPGA projects targeting Xilinx devices,
      and provides a fully integrated toolchain with strong IP ecosystem support.
    </p>

    <!-- Quick Info -->
    <div style="background:#f3e8ff; border-left:5px solid #9333ea; padding:14px; border-radius:6px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#6b21a8; margin-bottom:6px;">Environment</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li><strong>Vendor:</strong> Xilinx</li>
        <li><strong>Tool:</strong> Vivado</li>
        <li><strong>Simulator:</strong> Vivado Simulator</li>
        <li><strong>Linter:</strong> Verilator</li>
      </ul>
    </div>

    <!-- Requirements -->
    <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#1d4ed8; margin-bottom:6px;">Requirements</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li>Vivado must be installed and available in <code>$PATH</code>.</li>
        <li>The <strong>constraints</strong> folder must contain either:
          <ul>
            <li>An <code>.xdc</code> file named after the top module, or</li>
            <li>An <code>.sdc</code> file + <code>&lt;module_name&gt;.pin</code> file, from which Vivado will generate the required <code>.xdc</code>.</li>
          </ul>
        </li>
        <li>If an <code>&lt;module_name&gt;.xdc</code> already exists in the constraints folder when creating the project,
            it will be sourced directly. In this case, the <code>.sdc</code> and <code>.pin</code> files are ignored.</li>
      </ul>
    </div>

    <!-- Flow -->
    <div style="background:#fff7ed; border-left:5px solid #d97706; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#92400e; margin-bottom:6px;">Flow</h2>
      <p style="font-size:14px;">
        To run the Xilinx flow, configure your project YAML file with <code>vendor: xilinx</code>, then populate the manifests:
      </p>
      <ol style="font-size:14px; margin-left:20px;">
        <li>Add RTL files to <code>manifest_rtl</code>.</li>
        <li>Add testbench files to <code>manifest_tb</code>. If <code>.c</code> files are required for DPI, include them in the <code>software</code> manifest.<br>
            (<em>DPI is supported, but VPI is not</em>.)</li>
        <li>Add IPs to the <code>ip</code> manifest:
          <ul>
            <li>IP files may be either <code>.xci</code> or <code>.tcl</code>.</li>
            <li>TCL IPs can be exported directly from Vivado GUI using:
              <pre style="background:#f3f4f6; padding:6px; border-radius:4px; font-size:13px; overflow:auto;">
write_bd_tcl -force &lt;ip_name&gt;.tcl
              </pre>
            </li>
            <li>Vivado must be aware of any custom IP repository locations (set in <code>IP_REPO_PATHS</code>).</li>
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
        <li><strong>VPI support:</strong> Not supported in Vivado simulation environment.</li>
        <li><strong>Coverage:</strong> No coverage analysis available in Vivado simulator.</li>
        <li><strong>Alternative simulators:</strong> No current support to run Xilinx flow with ModelSim/Questa.</li>
        <li><strong>Netlist simulation:</strong> Only supported if the user manually generates the netlist and adds it to <code>rtl/tb</code> manifests.</li>
        <li><strong>STA reports:</strong> Flow runs STA, but report parsing/fetching is incomplete.</li>
        <li><strong>MicroBlaze MSS support:</strong> Config file is supported, but firmware flow integration needs improvement.</li>
        <li><strong>Bitstream generation:</strong> Feature untested.</li>
        <li><strong>Bitstream upload:</strong> Feature untested.</li>
        <li><strong>ChipScope / ILA:</strong> Not supported in current flow.</li>
        <li><strong>Logic partitions:</strong> Not supported.</li>
        <li><strong>Partial reconfiguration:</strong> Not supported.</li>
      </ul>
    </div>

  </body>
</html>
"""