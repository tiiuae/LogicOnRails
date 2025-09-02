import sys
import os
import re
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,
                               QGridLayout, QLabel, QSizePolicy)
from PySide6.QtCore import (Qt, Signal, QPropertyAnimation, QRect, QEasingCurve,
                            Property)
from PySide6.QtGui import QPainter, QColor, QFont, QKeyEvent

# ==============================================================================
# 1. HELPER CLASSES AND FUNCTIONS
# ==============================================================================

class VerilogParser:
    """
    Handles parsing manifest files and Verilog source files to understand
    the design hierarchy.
    """

    def __init__(self):
        # A database mapping a module name to its source file path
        # e.g., {"top_level": "src/top_level.v"}
        self.module_db = {}
        # Regex to find module definitions, e.g., "module my_module"
        self.module_def_re = re.compile(r"^\s*module\s+([a-zA-Z0-9_]+)")
        # Regex to find module instantiations, e.g., "my_module u_my_module ("
        self.module_inst_re = re.compile(
            r"^\s*([a-zA-Z0-9_]+)\s+(?:#\s*\(.*\))?\s*([a-zA-Z0-9_]+)\s*\("
        )

    def build_db_from_manifests(self, manifest_paths: list[str]):
        """Reads manifest files and populates the module database."""
        print("🔍 Searching for Verilog files in manifests...")
        all_verilog_files = set()
        for manifest_path in manifest_paths:
            try:
                with open(manifest_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            all_verilog_files.add(line)
            except FileNotFoundError:
                print(f"⚠️ Warning: Manifest file not found: {manifest_path}")

        for file_path in all_verilog_files:
            self._find_module_in_file(file_path)
        print(f"✅ Found {len(self.module_db)} modules.")

    def _find_module_in_file(self, file_path: str):
        """Scans a single file for a module definition and adds it to the db."""
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    match = self.module_def_re.match(line)
                    if match:
                        module_name = match.group(1)
                        self.module_db[module_name] = file_path
                        # Assuming one module definition per file for simplicity
                        return
        except FileNotFoundError:
            print(f"⚠️ Warning: Verilog file not found: {file_path}")
        except Exception as e:
            print(f"Error reading {file_path}: {e}")


    def get_instantiations(self, module_name: str) -> list[tuple[str, str]]:
        """
        Parses the file defining `module_name` and returns a list of its
        instantiated modules.

        Returns:
            A list of tuples: (module_type, instance_name)
        """
        file_path = self.module_db.get(module_name)
        if not file_path:
            return []

        instantiations = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Find the module definition block to avoid parsing outside it
                module_content_match = re.search(
                    rf"module\s+{module_name}[\s\S]*?endmodule", content
                )
                if not module_content_match:
                    return []
                
                module_block = module_content_match.group(0)
                for line in module_block.splitlines():
                    match = self.module_inst_re.match(line)
                    if match:
                        module_type = match.group(1)
                        instance_name = match.group(2)
                        # Avoid matching `module` keyword itself or other keywords
                        if module_type not in ["module", "endmodule", "initial", "always"]:
                             instantiations.append((module_type, instance_name))
        except Exception as e:
            print(f"Error parsing {file_path} for module {module_name}: {e}")

        return instantiations

def get_color_from_string(s: str) -> QColor:
    """Generates a consistent, visually pleasing color from a string."""
    hash_val = hash(s)
    hue = hash_val % 360
    # Use a fixed saturation and value for pastel-like colors
    return QColor.fromHsv(hue, 180, 220)

# ==============================================================================
# 2. CUSTOM QT WIDGETS
# ==============================================================================

class ModuleBlock(QWidget):
    """A custom widget representing an instantiated module block."""
    # Signal to be emitted on right-click, carrying the module type
    rightClicked = Signal(str)

    def __init__(self, module_type: str, instance_name: str, parent=None):
        super().__init__(parent)
        self.module_type = module_type
        self.instance_name = instance_name
        self.color = get_color_from_string(module_type)
        self.is_hovered = False
        
        # Enable mouse tracking and set size policy
        self.setMouseTracking(True)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumSize(120, 120)

        # Animation for hover effect
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def paintEvent(self, event):
        """Draws the block's square and text."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the rounded rectangle background
        painter.setBrush(self.color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 10, 10)

        # Draw the text in the center
        painter.setPen(Qt.GlobalColor.black)
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Display both module type and instance name
        text = f"{self.module_type}\n({self.instance_name})"
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

    def mousePressEvent(self, event):
        """Handles mouse clicks to detect a right-click."""
        if event.button() == Qt.MouseButton.RightButton:
            print(f"🖱️ Right-click on '{self.instance_name}' ({self.module_type}). Drilling down...")
            self.rightClicked.emit(self.module_type)
        else:
            super().mousePressEvent(event)

    def enterEvent(self, event):
        """Handles the mouse entering the widget area for the hover effect."""
        self.is_hovered = True
        self.animation.setStartValue(self.geometry())
        # Enlarge the widget by 10%
        new_rect = self.geometry().adjusted(-10, -10, 10, 10)
        self.animation.setEndValue(new_rect)
        self.animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Handles the mouse leaving the widget area."""
        self.is_hovered = False
        self.animation.setStartValue(self.geometry())
        # Shrink back to original size
        new_rect = self.geometry().adjusted(10, 10, -10, -10)
        self.animation.setEndValue(new_rect)
        self.animation.start()
        super().leaveEvent(event)

# ==============================================================================
# 3. MAIN APPLICATION WINDOW
# ==============================================================================

class BlockDiagramApp(QMainWindow):
    """The main application window."""
    def __init__(self, parser: VerilogParser, top_level_name: str):
        super().__init__()
        self.parser = parser
        self.history = [top_level_name] # Stack to track navigation history

        self.setWindowTitle("Verilog Hierarchy Visualizer")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(20, 20, 20, 20)

        self.redraw_ui()

    def redraw_ui(self):
        """Clears and redraws the UI with blocks for the current module."""
        # Clear existing widgets from the layout
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        current_module = self.history[-1]
        self.setWindowTitle(f"Hierarchy Of: {current_module}")
        
        instantiations = self.parser.get_instantiations(current_module)

        if not instantiations:
            # Display a message if there are no sub-modules
            label = QLabel(f"Module '{current_module}' has no instantiations.")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 16px; color: grey;")
            self.grid_layout.addWidget(label, 0, 0)
            return

        # Arrange blocks in a grid
        cols = 3 # max columns
        for i, (module_type, instance_name) in enumerate(instantiations):
            block = ModuleBlock(module_type, instance_name)
            block.rightClicked.connect(self.drill_down)
            row, col = divmod(i, cols)
            self.grid_layout.addWidget(block, row, col)

    def drill_down(self, module_type: str):
        """Changes the view to the selected submodule."""
        if module_type in self.parser.module_db:
            self.history.append(module_type)
            self.redraw_ui()
        else:
            print(f"🚫 Error: Module '{module_type}' not found in the database.")
            # Optionally, show a message box to the user here
            
    def go_back(self):
        """Navigates to the previously viewed module."""
        if len(self.history) > 1:
            print("⬅️ Navigating back...")
            self.history.pop()
            self.redraw_ui()
        else:
            print("Already at the top level.")

    def keyPressEvent(self, event: QKeyEvent):
        """Handles key presses for navigation."""
        if event.key() == Qt.Key.Key_Backspace:
            self.go_back()
        else:
            super().keyPressEvent(event)


# ==============================================================================
# 4. MAIN EXECUTION
# ==============================================================================

def main():
    """
    The main entry point of the script.
    
    ACTION REQUIRED:
    1. Create the folder/file structure below.
    2. Populate the files with your Verilog code.
    3. Ensure the paths in `manifest_files` and `top_level_module` are correct.
    
    Expected file structure:
    /your_project_folder/
    ├── visualizer.py       (this script)
    ├── manifest1.txt
    ├── manifest2.txt
    └── src/
        ├── top_level.v
        ├── processor.v
        ├── memory.v
        └── alu.v
    """
    
    # ------------------ CONFIGURATION ------------------
    # 3) A list of manifest file paths must be hardcoded.
    manifest_files = ["manifest1.txt", "manifest2.txt"]

    # 6) The name of the top-level architecture is hardcoded.
    top_level_module = "top_level"
    # ---------------------------------------------------

    # --- Create dummy files for demonstration if they don't exist ---
    if not os.path.exists("src"): os.makedirs("src")
    
    dummy_files = {
        "manifest1.txt": "src/top_level.v\nsrc/memory.v",
        "manifest2.txt": "# Other components\nsrc/processor.v\nsrc/alu.v",
        "src/top_level.v": """
            module top_level(input clk, input rst);
              processor proc_inst (.clk(clk), .rst(rst));
              memory #(.WIDTH(32)) mem_inst (.clk(clk));
            endmodule
        """,
        "src/processor.v": """
            module processor(input clk, input rst);
              alu alu_inst_0 (.clk(clk));
              alu alu_inst_1 (.clk(clk));
            endmodule
        """,
        "src/memory.v": "module memory(input clk); /* No instances */ endmodule",
        "src/alu.v": "module alu(input clk); /* No instances */ endmodule"
    }
    
    for path, content in dummy_files.items():
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.write(content.strip())
            print(f"📄 Created dummy file: {path}")
    # --- End of dummy file creation ---
    
    app = QApplication(sys.argv)

    parser = VerilogParser()
    # 2, 4) Load all manifest files
    parser.build_db_from_manifests(manifest_files)
    
    # 7) Check if the top level module exists
    if top_level_module not in parser.module_db:
        print(f"❌ FATAL: Top level module '{top_level_module}' not found in any manifest file.")
        sys.exit(1)

    # 8) Create and show the interactive window
    window = BlockDiagramApp(parser, top_level_module)
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()