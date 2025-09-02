class FeatureHierarchy:
    def __init__(self):
        self.option_name = "Hierarchy"
        self.option_content = self.content()
        self.order = 11

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f2f7fb; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#2563eb; margin-bottom:6px;">Hierarchy Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#1d4ed8;">Hierarchy:</strong> Work in progress. Displays a top-level block diagram of the architecture. It does <em>not</em> show interconnections—only module presence and layering. Modules are included only if they are listed in the <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">rtl_manifest</code>. Clicking a module loads its layer/overlay in the diagram.
      </span>
    </div>

    <!-- Requirements -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#0f766e; margin-bottom:6px;">Requirements</div>
      <ul style="margin:6px 0 0 18px; padding:0; font-size:14px; list-style-type:disc;">
        <li><strong style="color:#1d4ed8;">rtl_manifest</strong> must enumerate all modules to appear in the diagram.</li>
        <li>Only module names are shown; <em>no signal-level</em> interconnects are rendered.</li>
        <li>Clicking a module should load its layer (e.g., reveal internal sub-blocks or metadata).</li>
      </ul>
      <div style="font-size:12px; color:#6b7280; margin-top:6px;">
        This view is intended as a lightweight architectural snapshot; full connectivity visualization is planned for future iterations.
      </div>
    </div>

    <!-- Diagram placeholder -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:6px;">Block Diagram</div>
      <div style="font-size:14px; margin-bottom:8px;">
        Top-level block diagram of the loaded architecture. Modules appear as clickable panels. (If no diagram is available, ensure your <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">rtl_manifest</code> is correctly populated.)
      </div>
      <div style="font-size:12px; background:#ffffff; padding:10px; border-radius:5px; border:1px dashed #a5b4fc;">
        <em style="color:#6b7280;">[Diagram area — modules listed here; click to load layer]</em>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#e8f0ff; padding:14px; border-left:5px solid #6366f1; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#4f46e5; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls hier</code> <span style="color:#555;">→ opens the block diagram view; modules from <strong>rtl_manifest</strong> are shown.</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Keep the <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">rtl_manifest</code> clean (no stray whitespace in paths) so modules reliably appear. Future versions will expose module interconnects and allow drilling down deeper.
      </div>
    </div>

  </body>
</html>
"""
