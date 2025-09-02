class FeatureStart:
    def __init__(self):
        self.option_name = "Start"
        self.option_content = self.content()
        self.order = 40

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f2f7fb; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#2563eb; margin-bottom:6px;">Start Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#1d4ed8;">Start:</strong> Macro to kick off a project. Use <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">-b</code> or <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">--action</code> to string together tasks in sequence.
      </span>
    </div>

    <!-- Actions -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#0f766e; margin-bottom:6px;">Actions</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Letters used in <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-b</code> or <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--action</code> specify staged operations. Common flags:
      </div>
      <ul style="margin:6px 0 0 18px; padding:0; font-size:14px; list-style-type:disc;">
        <li><strong style="color:#1d4ed8;">c</strong>: Create a project.</li>
        <li><strong style="color:#1d4ed8;">d</strong>: Display project via GUI.</li>
        <li><strong style="color:#1d4ed8;">s</strong>: Synthesize the project.</li>
        <li><strong style="color:#1d4ed8;">p</strong>: Run place-and-route.</li>
      </ul>
      <div style="font-size:12px; color:#6b7280; margin-top:6px;">
        You can combine letters to perform multiple steps in order. The sequence dictates execution order (e.g., <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">cdsp</code> tries to create, display, synthesize, then place-and-route).
      </div>
    </div>

    <!-- Examples -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start -b c</code> <span style="color:#555;">→ creates a project</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start --action cd</code> <span style="color:#555;">→ creates and displays via GUI</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start -b s</code> <span style="color:#555;">→ synthesizes the project</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start -b sp</code> <span style="color:#555;">→ synthesizes and runs place-and-route</span></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls start -b cdsp</code> <span style="color:#555;">→ create, synthesize, place-and-route, and display</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Use combinations to build reproducible pipeline entry points (e.g., <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">rls start -b cdsp</code> for full setup + display). You can override defaults via YAML and layer additional flags.
      </div>
    </div>

  </body>
</html>
"""

