class FeatureDelete:
    def __init__(self):
        self.option_name = "Delete"
        self.option_content = self.content()
        self.order = 31

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f4f6fa; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#b91c1c; margin-bottom:6px;">Delete Project</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span><strong style="color:#dc2626;">Deletes the project folder</strong> and associated auxiliary directories/files in the current working directory. This is destructive—ensure you have backups or explicit confirmation in automation before running.</span>
    </div>

    <!-- Deleted items -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:6px;">Removed Files &amp; Directories</div>
      <div style="font-size:14px; margin-bottom:8px;">
        The following paths are deleted when the command is executed:
      </div>
      <ul style="margin:6px 0 0 18px; padding:0; font-size:13px; list-style-type:disc;">
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./&lt;prj_name&gt;</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./.bpad</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./.simvision</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./questa/aldec</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./questa/common</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./questa/mentor</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./questa/synopsys</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./questa/xcelium</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">transcript</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/common</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/libraries_ext</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/libraries_ip</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/libraries_tb</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/logs</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/xcelium</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/cds.lib</code></li>
        <li><code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">./xcelium/hdl.var</code></li>
      </ul>
    </div>

    <!-- Example -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls delete</code>
      </div>
    </div>

    <!-- Warning -->
    <div style="background:#fff8f0; padding:12px 14px; border-left:5px solid #dc2626; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#9b1c1c;">Warning:</div>
      <div style="font-size:13px; margin-top:4px;">
        This operation permanently removes the project and related metadata. There is no automatic recovery. Use in scripts only when you explicitly intend to discard the entire project state.
      </div>
    </div>

  </body>
</html>
"""