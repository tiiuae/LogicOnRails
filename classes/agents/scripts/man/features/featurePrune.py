class FeaturePurge:
    def __init__(self):
        self.option_name = "Purge"
        self.option_content = self.content()
        self.order = 21

    def content(self):
        return  """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f7f9fc; color:#1f2d3a; line-height:1.45;">
    <!-- Header -->
    <div style="font-size:26px; font-weight:700; color:#dc2626; margin-bottom:8px;">Purge Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span><strong style="color:#b91c1c;">Purge:</strong> Deletes a folder containing the default project in the current directory.</span>
    </div>

    <!-- Description -->
    <div style="background:#fff5f5; padding:14px; border-radius:8px; border:1px solid #fca5a5; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:600; color:#9b1c1c; margin-bottom:6px;">What it does</div>
      <div style="font-size:14px;">
        Removes the generated project directory (default project) from the current working directory. Use with caution: this is destructive and does not prompt for recovery.
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block; margin-bottom:4px;">rls purge</code>
      </div>
    </div>

    <!-- Warning -->
    <div style="background:#fff7ed; padding:12px 14px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">
        Note:
      </div>
      <div style="font-size:13px; margin-top:4px;">
        This operation deletes the project folder; ensure you have backups if needed or confirmations in your workflow before invoking it in automated scripts.
      </div>
    </div>

  </body>
</html>
"""