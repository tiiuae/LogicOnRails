class FeatureYaml:
    def __init__(self):
        self.option_name = "Yaml"
        self.option_content = self.content()
        self.order = 0
    
    def __str__(self):
        return self.option_name

    def __repr__(self):
        return self.option_name

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f7f9fc; color:#1f2d3a; line-height:1.5;">

    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#2563eb; margin-bottom:8px;">YAML Configuration Manual</div>

    <!-- Overview -->
    <div style="font-size:14px; color:#475569; margin-bottom:20px;">
      <strong>Overview:</strong> The <code style="background:#eef4fc; padding:2px 6px; border-radius:4px;">YAML</code> file inside the <strong>root directory</strong> of your project provides initial configuration.  
      Most values may be updated at runtime via command arguments. Use it to persist long-term defaults (rarely changed) or convenient defaults like the most-used test name or waveform file.
    </div>

    <!-- About YAML -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:20px;">
      <div style="font-size:20px; font-weight:700; color:#0f766e; margin-bottom:4px;">About YAML</div>
      <div style="font-size:14px;">
        YAML stores structured data in a <strong>key:value</strong> pattern, mapping naturally to Python <code>dict</code> structures.
      </div>
    </div>

    <!-- Categories -->
    <div style="font-size:18px; font-weight:600; color:#7c3aed; margin-bottom:12px;">YAML Configuration Categories</div>

    <!-- System -->
    <div style="background:#ecfdf5; padding:14px; border-left:5px solid #10b981; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#065f46;">System</div>
      <div style="font-size:13px; margin:6px 0;">Variables that affect the entire project (toolchain, processor, firmware, and control options).</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>vendor</strong>: Project vendor (altera, xilinx, cadence, microsemi).</li>
        <li><strong>simulator</strong>: Simulator to use (questa, modelsim, xcelium, vivado).</li>
        <li><strong>linter</strong>: Linter choice (xcelium, verilator).</li>
        <li><strong>per_prj_script</strong>: Custom per-project override scripts.</li>
        <li><strong>keep</strong>: Prevents deletion of EDA-generated files after run.</li>
        <li><strong>scripts_only</strong>: Generates scripts without executing tools. Requires <em>keep</em> or <em>log</em> to persist scripts.</li>
      </ul>
    </div>

    <!-- Project -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#7c2d12;">Project</div>
      <div style="font-size:13px; margin:6px 0;">Variables controlling project folder structure and tool-specific behavior.</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>module_name</strong>: Project name (default = top-level testbench).</li>
        <li><strong>uproc</strong>: Microprocessor existence. Options: on, off.</li>
        <li><strong>firmware</strong>: Path to firmware root (.hex expected).</li>
        <li><strong>path</strong>: Project path where directory is created.</li>
        <li><strong>ext_modules</strong>: Enable external modules (manifest_ext_ip). Options: on, off.</li>
        <li><strong>defines_syn</strong>: Synthesis defines (+define+Name=Value).</li>
        <li><strong>constraints</strong>: Constraint folder (.sdc, optional .xdc/.pdc).</li>
        <li><strong>message_lvl</strong>: Debug verbosity (LOG_INF, LOG_WRN, LOG_CRT, LOG_ERR, LOG_DBG).</li>
        <li><strong>rev</strong>: Project revision (non-functional).</li>
        <li><strong>log</strong>: Saves executed commands + warnings/errors to reports directory.</li>
      </ul>
    </div>

    <!-- Simulation -->
    <div style="background:#eef2ff; padding:14px; border-left:5px solid #6366f1; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#4338ca;">Simulation</div>
      <div style="font-size:13px; margin:6px 0;">Simulation control variables.</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>defines_sim</strong>: Defines for simulation (+define+Name=Value).</li>
        <li><strong>tb</strong>: Testbench top file or alternate architecture.</li>
        <li><strong>access</strong>: Enable signal history. Options: on, off.</li>
        <li><strong>coverage</strong>: Enable coverage tracking. Options: on, off.</li>
        <li><strong>dpi</strong>: Source/compile .c/.h from software manifest. Options: on, off.</li>
        <li><strong>uvm</strong>: Include UVM manifest (Xcelium only). Options: on, off.</li>
        <li><strong>comp_opt</strong>: Simulation model (deprecated). Options: netlist, off.</li>
        <li><strong>gui</strong>: Run with GUI. Options: on, off.</li>
        <li><strong>wave</strong>: Preload waveform path in GUI mode.</li>
      </ul>
    </div>

    <!-- Manifests -->
    <div style="background:#fff; padding:14px; border-left:5px solid #8b5cf6; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#5b21b6;">Manifests</div>
      <div style="font-size:13px; margin:6px 0;">Paths to manifest files.</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>source_rtl</strong>: RTL manifest for synthesis.</li>
        <li><strong>source_ips</strong>: IP manifest with vendor prefix.</li>
        <li><strong>source_tb</strong>: Testbench manifest (.sv only).</li>
        <li><strong>source_soft</strong>: Software manifest (.c/.h).</li>
        <li><strong>source_inc</strong>: Include manifest for dependencies.</li>
        <li><strong>source_netlist</strong>: Netlist manifest (.v/.hdl).</li>
        <li><strong>source_lib</strong>: External library manifest (precompiled).</li>
        <li><strong>source_ext</strong>: External/encrypted RTL manifest.</li>
        <li><strong>source_uvm</strong>: UVM manifest (Xcelium; deprecated).</li>
        <li><strong>source_mocked</strong>: Mocked manifest (.sv for Verilator lint).</li>
      </ul>
    </div>

    <!-- Quartus -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#1e40af;">Quartus</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>quartus_version</strong>: Quartus version.</li>
        <li><strong>quartus_device</strong>: Target device.</li>
        <li><strong>quartus_family</strong>: Target family.</li>
      </ul>
    </div>

    <!-- Vivado -->
    <div style="background:#f3f4f6; padding:14px; border-left:5px solid #9333ea; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#6b21a8;">Vivado</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>vivado_device</strong>: Target device.</li>
      </ul>
    </div>

    <!-- GoWin -->
    <div style="background:#fff8f0; padding:14px; border-left:5px solid #f97316; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#9a3412;">GoWin</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>gowin_device</strong>: Target device.</li>
      </ul>
    </div>

    <!-- Questa -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #0ea5e9; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#1e3a8a;">Questa</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>reports_dir</strong>: Report output directory.</li>
      </ul>
    </div>

    <!-- Verilator -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #6366f1; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#4f46e5;">Verilator</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>verilator_warn_options</strong>: Custom warning flags.</li>
      </ul>
    </div>

    <!-- Microsemi -->
    <div style="background:#ecfdf5; padding:14px; border-left:5px solid #059669; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#065f46;">Microsemi</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>libero_device</strong>: Target device.</li>
        <li><strong>libero_family</strong>: Target family.</li>
        <li><strong>libero_die</strong>: Target die.</li>
        <li><strong>libero_package</strong>: Target package.</li>
        <li><strong>pdc_override</strong>: Override automatic PDC creation (on/off).</li>
        <li><strong>pdc_folder</strong>: Path to PDC folder (/io and /fp required).</li>
      </ul>
    </div>

    <!-- Cadence -->
    <div style="background:#f9f5ff; padding:14px; border-left:5px solid #a855f7; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#7e22ce;">Cadence</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>def_file</strong>: DEF file path.</li>
        <li><strong>lef_file</strong>: LEF abstraction file.</li>
        <li><strong>lib_file</strong>: Liberty file with timing data.</li>
        <li><strong>low_power_flow</strong>: Enables low-power flow (unused).</li>
        <li><strong>dbg_flow</strong>: Enables debug power flow (unused).</li>
      </ul>
    </div>

    <!-- Per Tool Option -->
    <div style="background:#fffcee; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:17px; font-weight:700; color:#92400e;">Per Tool Option</div>
      <div style="font-size:13px; margin:6px 0;">Fine-grained tool control options.</div>
      <ul style="margin:0 0 0 18px; font-size:14px;">
        <li><strong>synth_opt</strong>: Custom synthesis options.</li>
        <li><strong>pr_opt</strong>: Custom place-and-route options.</li>
        <li><strong>sim_opt</strong>: Custom simulation options.</li>
        <li><strong>sta_opt</strong>: Static timing analysis options.</li>
        <li><strong>bit_opt</strong>: Bitstream generation options.</li>
      </ul>
    </div>

  </body>
</html>
"""