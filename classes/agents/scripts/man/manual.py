# =============================================================================
# Project:        Logic on Rails
# File:           manual
# Author:         GPT 
# Modified by:    Matheus Lemes Ferronato
# Created:        15 aug 2025
# Description:    Manual 
# =============================================================================


import sys
import os
import inspect
import hashlib
import traceback
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QListWidget, QTextEdit,
    QPushButton, QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QLabel
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import importlib.util

# === Hardwired directory to scan. Change this to your actual manual classes folder ===
# e.g., absolute: Path("/home/matheusferronato/example_manual")
# or relative to this script: Path(__file__).resolve().parent / "example_manual"
MANUAL_ROOT = Path(__file__).resolve().parent / "example_manual"


def load_classes_from_path(root: Path):
    """
    Recursively imports .py files under `root`, instantiates any class that has a callable
    content() method, uses its self.option_name as the display label, and sorts by instance.order.
    Returns list of tuples: (display_name, instance)
    """
    raw_entries = []
    for pyfile in root.rglob("*.py"):
        try:
            digest = hashlib.md5(str(pyfile.resolve()).encode()).hexdigest()[:8]
            module_name = f"manual_mod_{pyfile.stem}_{digest}"
            spec = importlib.util.spec_from_file_location(module_name, str(pyfile))
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                for name, obj in vars(module).items():
                    if inspect.isclass(obj) and obj.__module__ == module.__name__:
                        if hasattr(obj, "content") and callable(getattr(obj, "content")):
                            try:
                                instance = obj()  # expect __init__ sets self.option_name and self.order
                                label_base = getattr(instance, "option_name", name)
                                order_value = getattr(instance, "order", 1_000_000)  # missing order goes to end
                                raw_entries.append({
                                    "class_name": name,
                                    "filename": pyfile.name,
                                    "instance": instance,
                                    "label_base": label_base,
                                    "order": order_value,
                                })
                            except Exception:
                                print(f"[warning] failed to instantiate class {name} in {pyfile}:")
                                traceback.print_exc()
        except Exception:
            print(f"[warning] failed to load {pyfile}:")
            traceback.print_exc()

    # detect duplicates of option_name
    counts = {}
    for e in raw_entries:
        counts[e["label_base"]] = counts.get(e["label_base"], 0) + 1

    enriched = []
    for e in raw_entries:
        if counts[e["label_base"]] > 1:
            display_name = f"{e['label_base']} ({e['class_name']} in {e['filename']})"
        else:
            display_name = e["label_base"]
        enriched.append({
            "display_name": display_name,
            "instance": e["instance"],
            "order": e["order"],
            "tie": e["label_base"].lower(),
        })

    # sort by order, then label_base (case-insensitive) to break ties
    enriched.sort(key=lambda x: (x["order"], x["tie"]))

    # produce final list of tuples
    final_list = [(e["display_name"], e["instance"]) for e in enriched]
    return final_list




class ManualWindow(QMainWindow):
    def __init__(self, class_instances):
        super().__init__()
        self.setWindowTitle("Application Manual")
        self.resize(900, 600)

        splitter = QSplitter(Qt.Horizontal, self)
        self.setCentralWidget(splitter)

        # Left panel: class list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        label = QLabel("Classes")
        label.setFont(QFont("", 12, QFont.Bold))
        left_layout.addWidget(label)
        self.list_widget = QListWidget()
        left_layout.addWidget(self.list_widget)  # scrollable automatically
        splitter.addWidget(left_widget)
        splitter.setStretchFactor(0, 1)

        # Right panel: content display
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)
        self.content_view = QTextEdit()
        self.content_view.setReadOnly(True)
        self.content_view.setAcceptRichText(True)
        self.content_view.setFontPointSize(11)
        right_layout.addWidget(self.content_view)

        # Close button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.close_btn)
        right_layout.addLayout(btn_layout)

        splitter.addWidget(right_widget)
        splitter.setStretchFactor(1, 3)

        # Populate list
        self.instances = {}
        for name, inst in class_instances:
            self.list_widget.addItem(name)
            self.instances[name] = inst

        self.list_widget.currentTextChanged.connect(self.on_selection_changed)
        if self.list_widget.count() > 0:
            self.list_widget.setCurrentRow(0)

    def on_selection_changed(self, text):
        inst = self.instances.get(text)
        if not inst:
            self.content_view.setPlainText("No content available.")
            return
        try:
            raw = inst.content()
            if not isinstance(raw, str):
                raw = str(raw)
            if "<" in raw and ">" in raw:
                self.content_view.setHtml(raw)
            else:
                self.content_view.setPlainText(raw)
        except Exception as e:
            self.content_view.setPlainText(f"Error calling content(): {e}")


def main():
    FALLBACK = Path(__file__).resolve().parent / "example_manual"
    frm_path = os.getenv("frm_path")
    script_path = os.getenv("script_path")
    if frm_path and script_path:
        root = Path(frm_path) / script_path / "man" / "features"
    else:
        print("Warning: frm_path or script_path not set, using fallback manual directory.", file=sys.stderr)
        root = FALLBACK
    root = root.resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: manual directory {root} does not exist or is not a directory.", file=sys.stderr)
        sys.exit(1)

    class_instances = load_classes_from_path(root)
    if not class_instances:
        print(f"No suitable classes found under {root}. Ensure each class has a content() method.")
    app = QApplication(sys.argv)
    win = ManualWindow(class_instances)
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
