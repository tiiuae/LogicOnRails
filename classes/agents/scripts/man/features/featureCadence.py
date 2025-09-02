class FeatureCadence:
    def __init__(self):
        self.option_name = "Cadence"
        self.option_content = self.content()
        self.order = 14

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:20px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f9fafb; color:#1f2937; line-height:1.6;">

    <!-- Title -->
    <h1 style="color:#7e22ce; font-size:28px; font-weight:700; margin-bottom:8px;">Cadence Flow</h1>

    <!-- Overview -->
    <p style="font-size:15px; color:#4b5563; margin-bottom:20px;">
      The <strong>Cadence flow</strong> leverages a suite of tools for RTL-to-GDSII and verification:
      <em>Genus</em>, <em>Modus</em>, <em>Innovus</em>, <em>Conformal</em>, <em>Tempus</em>, <em>Palladium</em>, and <em>Protium</em>.  
      Simulation and linting are handled by <strong>Xcelium</strong>.  
    </p>

    <p style="font-size:15px; color:#4b5563; margin-bottom:20px;">
      This flow is still under development and should be considered <strong>beta</strong>. 
      <strong>Genus and Xcelium</strong> (synthesis and simulation) are fully supported and tested. Other tools are partially integrated
      and may require manual adjustments via script generation.
    </p>

    <!-- Quick Info -->
    <div style="background:#f3e8ff; border-left:5px solid #9333ea; padding:14px; border-radius:6px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#6b21a8; margin-bottom:6px;">Environment</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li><strong>Vendor:</strong> Cadence</li>
        <li><strong>Tools:</strong> Genus, Modus, Innovus, Conformal, Tempus, Palladium, Protium</li>
        <li><strong>Simulator:</strong> Xcelium</li>
        <li><strong>Linter:</strong> Xcelium</li>
      </ul>
    </div>

    <!-- Requirements -->
    <div style="background:#ffffff; border:1px solid #d1d5db; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#1d4ed8; margin-bottom:6px;">Requirements</h2>
      <ul style="margin:0; padding-left:20px; font-size:14px;">
        <li>Cadence tools (Genus, Innovus, Xcelium, etc.) must be installed and available in <code>$PATH</code>.</li>
        <li>Scripts are generated automatically by the flow. Use the <strong>script_only</strong> YAML option to generate scripts without executing them, useful for manual tuning.</li>
        <li>The YAML configuration enables/disables generation of directives such as:
          <ul>
            <li>Debug instrumentation</li>
            <li>ATPG generation (via Modus)</li>
            <li>Low-power synthesis directives</li>
            <li>Physical-aware synthesis</li>
          </ul>
        </li>
        <li>Different file types can be provided to guide tools:
          <ul>
            <li><code>.def</code> – design exchange format</li>
            <li><code>.lef</code> – library exchange format (cells/blocks)</li>
            <li><code>.scan</code> – scan chain definitions</li>
            <li><code>.saif</code> – switching activity for power analysis</li>
            <li><code>.cpf</code> – common power format (low-power intent)</li>
            <li><code>.lib</code> – liberty timing models</li>
          </ul>
        </li>
        <li>If a single file is provided (e.g., <code>.lib</code>), it is loaded directly. If a folder path is given, all files of that type in the folder are loaded automatically.</li>
      </ul>
    </div>

    <!-- Flow -->
    <div style="background:#fff7ed; border-left:5px solid #d97706; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#92400e; margin-bottom:6px;">Flow</h2>
      <p style="font-size:14px;">To run the Cadence flow, configure your project YAML file with <code>vendor: cadence</code>, then add RTL sources to <code>manifest_rtl</code>. Example commands:</p>

      <pre style="background:#f3f4f6; padding:10px; border-radius:6px; font-size:13px; overflow:auto;">
# Run Genus synthesis (fully supported and tested)
rls synth
# Run Xcelium simulator (fully supported and tested)
rls sim

# Run Modus ATPG (beta, not fully tested)
rls bit
      </pre>
    </div>

    <!-- TODO -->
    <div style="background:#fee2e2; border-left:5px solid #dc2626; border-radius:6px; padding:14px; margin-bottom:20px;">
      <h2 style="font-size:18px; font-weight:700; color:#b91c1c; margin-bottom:6px;">TODO / Known Limitations</h2>
      <p style="font-size:14px;">The following integrations are planned but not yet complete:</p>
      <ul style="font-size:14px; margin-left:20px;">
        <li><strong>Verisium</strong> controller integration</li>
        <li><strong>Tempus</strong> controller integration</li>
        <li><strong>Innovus</strong> controller integration</li>
        <li><strong>Palladium</strong> emulation controller integration</li>
        <li><strong>Protium</strong> prototyping controller integration</li>
        <li><strong>Conformal</strong> equivalence checker integration</li>
        <li><strong>Jasper</strong> formal verification integration</li>
      </ul>
    </div>

  </body>
</html>
"""