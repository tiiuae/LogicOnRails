class FeatureGenerate:
    def __init__(self):
        self.option_name = "Generate"
        self.option_content = self.content()
        self.order = 20

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f7f9fc; color:#1f2d3a; line-height:1.45;">
    <!-- Header -->
    <div style="font-size:26px; font-weight:700; color:#2563eb; margin-bottom:8px;">Generate Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>The <strong style="color:#1d4ed8;">generate</strong> command creates a folder with a default project in the current directory.</span>
    </div>

    <!-- Arguments -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#0f766e; margin-bottom:6px;">Arguments</div>
      <ul style="margin:8px 0 0 18px; padding:0; list-style-type:disc; font-size:14px;">
        <li><strong style="color:#1d4ed8;">--pps</strong>: <span style="font-style:italic;">PerProjectScripts</span>, enables the PPS option in the manifest. <span style="color:#d97706;">(to be implemented)</span></li>
        <li><strong style="color:#1d4ed8;">--prj</strong>: Override the default project name defined in the YAML.</li>
        <li><strong style="color:#1d4ed8;">--nm</strong>: Change the generated folder name.</li>
        <li><strong style="color:#1d4ed8;">--sm</strong>: Select a different default simulator.</li>
        <li><strong style="color:#1d4ed8;">--lt</strong>: Override the default linter.</li>
        <li><strong style="color:#1d4ed8;">--vr</strong>: Change the default vendor. Updating the vendor also updates the default <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">synth_def</code>.</li>
      </ul>
    </div>

    <!-- Examples -->
    <div style="background:#ecf5ff; padding:14px; border-left:5px solid #3b82f6; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px; margin:4px 0;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls generate</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls generate --nm test_script</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls generate --nm test_script --vr microsemi</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px;">rls generate --nm test_script --vr microsemi --lt xcelium</code></div>
      </div>
    </div>

  </body>
</html>
"""
