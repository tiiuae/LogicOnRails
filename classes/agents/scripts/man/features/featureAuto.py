class FeatureAuto:
    def __init__(self):
        self.option_name = "Auto"
        self.option_content = self.content()
        self.order = 50

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f8fc; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#0f766e; margin-bottom:6px;">Auto Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#0f766e;">Auto:</strong> Macro engine to automate a sequence of actions. Provide a path to a macro/script file and the framework will interpret and execute the encoded steps in order.
      </span>
    </div>

    <!-- Behavior -->
    <div style="background:#eefaf6; padding:14px; border-left:5px solid #10b981; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#047857; margin-bottom:4px;">What it does</div>
      <div style="font-size:14px;">
        The <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">auto</code> command reads a user-provided macro file and runs the steps described inside, enabling reproducible multi-stage flows without manual chaining.
      </div>
      <div style="font-size:13px; margin-top:8px;">
        The macro file is expected to contain the sequence of commands or actions in the framework's script syntax. Providing flexibility, users can define creation, synthesis, routing, display, and other operations in one file.
      </div>
    </div>

    <!-- Invocation -->
    <div style="background:#ffffff; padding:14px; border-radius:8px; border:1px solid #d1d5db; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#2563eb; margin-bottom:6px;">Invocation</div>
      <div style="font-size:14px;">
        Use <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">-p</code> or <code style="background:#eef4fa; padding:2px 4px; border-radius:3px;">--path</code> to supply the path to the macro script.
      </div>
      <div style="font-size:14px; margin-top:8px;">
        <code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls auto -p ./path/to/automation_file.script</code>
      </div>
    </div>

    <!-- Example -->
    <div style="background:#ecf5ff; padding:14px; border-left:5px solid #4338ca; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Example</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls auto -p ./scripts/build_and_deploy.script</code> <span style="color:#555;">→ executes the sequence defined in <em>build_and_deploy.script</em>.</span></div>
      </div>
    </div>

    <!-- Tip -->
    <div style="background:#fffdf6; padding:12px; border-left:5px solid #d97706; border-radius:6px;">
      <div style="font-size:14px; font-weight:600; color:#92400e;">Tip:</div>
      <div style="font-size:13px; margin-top:4px;">
        Keep macro files small and composable. Version them alongside your YAML configurations to reproduce environments reliably in CI or debugging sessions.
      </div>
    </div>

  </body>
</html>
"""







