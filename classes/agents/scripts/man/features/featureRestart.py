class FeatureRestart:
    def __init__(self):
        self.option_name = "Restart"
        self.option_content = self.content()
        self.order = 41

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#eef7fc; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#d946ef; margin-bottom:6px;">Restart Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#7c3aed;">Restart:</strong> Behaves like <em>Start</em> but first deletes the existing project before executing the staged steps. Use <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">-b</code> to chain operations.
      </span>
    </div>

    <!-- Behavior note -->
    <div style="background:#fff5f5; padding:14px; border-left:5px solid #dc2626; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:16px; font-weight:700; color:#9b1c1c; margin-bottom:4px;">Behavior</div>
      <div style="font-size:14px;">
        Existing project state is removed first (equivalent to a purge), then the sequence of actions encoded by the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">-b</code> string is executed in order.
      </div>
    </div>

    <!-- Actions recap -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#2563eb; margin-bottom:6px;">Actions</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Letters in the <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-b</code> string specify what to perform after the purge. Common codes:
      </div>
      <ul style="margin:6px 0 0 18px; padding:0; font-size:14px; list-style-type:disc;">
        <li><strong style="color:#1d4ed8;">c</strong>: Create a project.</li>
        <li><strong style="color:#1d4ed8;">d</strong>: Display via GUI.</li>
        <li><strong style="color:#1d4ed8;">s</strong>: Synthesize the project.</li>
        <li><strong style="color:#1d4ed8;">p</strong>: Run place-and-route.</li>
      </ul>
    </div>

    <!-- Examples -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #9333ea; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#4f46e5; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls restart -b c</code> <span style="color:#555;">→ deletes existing project, then creates a new one</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls restart -b cd</code> <span style="color:#555;">→ delete, create, and display via GUI</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls restart -b s</code> <span style="color:#555;">→ delete then synthesize</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls restart -b sp</code> <span style="color:#555;">→ delete, synthesize, and run place-and-route</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Use <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">rls restart -b cdsp</code> for a clean full pipeline (delete/create/display/synth+P&R) in one shot.
      </div>
    </div>

  </body>
</html>
"""







