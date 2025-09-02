class FeatureLint:
    def __init__(self):
        self.option_name = "Lint"
        self.option_content = self.content()
        self.order = 32

    def content(self):
        return """
<!DOCTYPE html>
<html lang="en">
  <body style="margin:0; padding:16px; font-family:system-ui,-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif; background:#f5f7fa; color:#1f2d3a; line-height:1.45;">
    <!-- Title -->
    <div style="font-size:28px; font-weight:700; color:#4338ca; margin-bottom:6px;">Lint Command</div>
    <div style="font-size:14px; color:#475569; margin-bottom:16px;">
      <span>
        <strong style="color:#1d4ed8;">Lint:</strong> Runs the linter over RTL and testbench sources. 
        <span style="font-style:italic;">Verilator</span> is lightweight/free and catches early issues like size mismatches, logic loops, and unconnected signals. 
        The <span style="font-style:italic;">Xcelium HAL</span> linter is paid/heavier but provides deeper analysis. By default only RTL is checked; testbench and UVM files can be included optionally.
      </span>
    </div>

    <!-- Bypass Linter -->
    <div style="background:#fff7ed; padding:14px; border-left:5px solid #d97706; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#92400e; margin-bottom:4px;">Bypass Linter</div>
      <div style="font-size:14px; margin-bottom:6px;">
        Some code (simulation-only snippets, black boxes, or IP wrappers) may break strict linting. To exclude regions, wrap them with the special markers:
      </div>
      <div style="background:#f1f5f9; padding:10px; border-radius:5px; font-family:monospace; font-size:13px; margin-bottom:4px;">
        // framework lint_off<br>
        &lt;your code here&gt;<br>
        // framework lint_on
      </div>
      <div style="font-size:12px; color:#6b7280;">
        Only the code between <strong>lint_off</strong> and <strong>lint_on</strong> is skipped; rest is still analyzed.
      </div>
    </div>

    <!-- Log -->
    <div style="background:#ecf5ff; padding:14px; border-left:5px solid #2563eb; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#1e3a8a; margin-bottom:4px;">Log</div>
      <div style="font-size:14px;">
        Provide <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">-l</code> to persist linter output to log files for inspection and post-mortem. Logs are stored alongside the standard report directory.
      </div>
    </div>

    <!-- One_linter -->
    <div style="background:#eef6ff; padding:14px; border-left:5px solid #6366f1; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:20px; font-weight:700; color:#4f46e5; margin-bottom:4px;">One_linter</div>
      <div style="font-size:14px; margin-bottom:6px;">
        <strong>one_linter</strong> is a custom rule-based linter shipped with the framework. It enforces coding best practices such as flagging <code>always</code> blocks that are not labeled <code>always_ff</code>, <code>always_comb</code>, or <code>always_latch</code>. You can override it by replacing <code style="background:#f1f5f9; padding:2px 4px; border-radius:3px;">one_linter.py</code> under the <code>verilator</code> folder with your own implementation.
      </div>
    </div>

    <!-- Examples -->
    <div style="background:#f0f9ff; padding:14px; border-left:5px solid #9333ea; border-radius:6px; margin-bottom:16px;">
      <div style="font-size:18px; font-weight:700; color:#6b21a8; margin-bottom:4px;">Examples</div>
      <div style="font-size:14px;">
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls lint</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls lint -t</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls lint -l</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls lint -u</code></div>
        <div><code style="background:#f1f5f9; padding:4px 6px; border-radius:4px; display:block;">rls lint -s xcelium</code></div>
      </div>
    </div>

    <!-- Footer note -->
    <div style="font-size:12px; color:#6b7280; margin-top:8px;">
      <em>Tip: Combine flags to include UVM/testbench sources and capture verbose output for CI pipelines.</em>
    </div>
  </body>
</html>
"""
