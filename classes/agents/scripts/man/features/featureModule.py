class FeatureModule:
    def __init__(self):
        self.option_name = "Module"
        self.option_content = self.content()
        self.order = 97

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f8fc; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#7c3aed; margin-bottom:6px;">Module Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#5b21b6;">Module:</strong> Imports a template SystemVerilog module following the framework standard. By default the name is <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">&lt;project_module_name&gt;_eg</code>. Override or adjust behavior with flags.
      </span>
    </div>

    <!-- Behavior / Options -->
    <div style="background:#fff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#2563eb; margin-bottom:6px;">Options</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Control the imported module's name and suffix:
      </div>
      <ul style="margin:6px 0 0 18px; padding:0; list-style-type:disc; font-size:14px;">
        <li><strong style="color:#1d4ed8;">--module_name</strong>: Override the default module name (replaces <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">&lt;project_module_name&gt;_eg</code>).</li>
        <li><strong style="color:#1d4ed8;">--ignore on</strong>: Remove the <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">_eg</code> suffix from the generated file/module name.</li>
      </ul>
      <div style="font-size:12px; color:#6b7280; margin-top:6px;">
        If both are used, <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--module_name</code> sets the base name and <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--ignore on</code> suppresses the automatic <code>_eg</code> suffix.
      </div>
    </div>

    <!-- Examples -->
    <div style="background:#ecf5ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls module</code> <span style="color:#555;">→ imports default module named &lt;project_module_name&gt;_eg</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls module --module_name adder</code> <span style="color:#555;">→ imports module named <strong>adder</strong>_eg</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls module --module_name adder --ignore on</code> <span style="color:#555;">→ imports module named <strong>adder</strong> (no <code>_eg</code> suffix)</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Combine <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--module_name</code> with consistent naming in your YAML to keep template tracking predictable across CI runs.
      </div>
    </div>

  </body>
</html>
"""