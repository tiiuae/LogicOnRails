class FeaturePrj:
    def __init__(self):
        self.option_name = "Prj"
        self.option_content = self.content()
        self.order = 98

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#eef7fc; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#2563eb; margin-bottom:6px;">Prj Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#1d4ed8;">Prj:</strong> Opens the project in the appropriate GUI using the correct underlying command line. It abstracts the toolchain invocation so users can consistently launch the GUI without memorizing per-tool commands.
      </span>
    </div>

    <!-- Behavior / Gui logic -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#0f766e; margin-bottom:6px;">Behavior</div>
      <div style="font-size:14px; margin-bottom:8px;">
        For most toolchains, <strong>rls prj</strong> simply launches their GUI frontend. 
        For <strong style="color:#7c3aed;">Cadence</strong> flows, if the <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">-g</code> flag is used <em>alongside</em> actions like <code>create</code>, <code>synth</code>, etc., the internal <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">gui_show</code> command is executed at the end to surface the result. Other chains ignore chaining and simply start their GUI.
      </div>
      <div style="font-size:12px; color:#6b7280;">
        This lets automation scripts end with a consistent GUI reveal regardless of underlying differences.
      </div>
    </div>

    <!-- Example -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls prj</code> <span style="color:#555;">→ opens the current project in its GUI.</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Use <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">rls prj</code> at the end of scripted flows to standardize GUI launching across vendors, especially when combining with <code>-g</code> for Cadence.
      </div>
    </div>

  </body>
</html>
"""

