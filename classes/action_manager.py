"""
action_manager.py
~~~~~~~~~~~~~~~~~~

This module defines :class:`ActionManager` which orchestrates the
execution of synthesis, simulation and other build stages based on
command line input.  It wraps an underlying EDA controller object
responsible for interfacing with vendor tools and provides higher
level convenience commands such as ``create``, ``delete`` and
``update``.  The implementation minimises repetition by using
collections to drive dispatch and clean up behaviour.
"""

from __future__ import annotations

import os
import subprocess
import shutil
from typing import List, Callable, Dict

from classes.agents.edaController import EDAController  # type: ignore

import sys


class ActionManager:
    """Dispatch runtime actions based on command line requests."""

    def __init__(self, funcs: List[str], curr_dir: str, frm_file: str, args) -> None:
        self.funcs = funcs
        self.curr_dir = curr_dir
        self.frm_file = frm_file
        self.args = args
        # Derived environment values
        self.frm_path = os.getenv('frm_path', '')
        self.script_path = os.getenv('script_path', '')
        self.packages_path = f"{self.frm_path}/packages"
        # Instantiate the vendor controller
        self.edaCtrl = EDAController(args, os.environ.get('linter'))
        self._validate_single_func()

    def _validate_single_func(self) -> None:
        if len(self.funcs) != 1:
            print(f'Number of functions called must be one, number called is {len(self.funcs)}')
            sys.exit(1)
        self.func = self.funcs[0]

    # -- public API -------------------------------------------------------

    def run(self) -> None:
        """Execute the requested function if available."""
        method: Callable[[], None] | None = getattr(self, self.func, None)
        if not method:
            print(f'Invalid command: {self.func}')
            return
        method()

    # -- dispatchable actions --------------------------------------------

    def synth(self) -> None:
        self.edaCtrl.agtVendor.runSynth()

    def route(self) -> None:
        self.edaCtrl.agtVendor.runRoute()

    def bit(self) -> None:
        self.edaCtrl.agtVendor.runBit()

    def prj(self) -> None:
        self.edaCtrl.agtVendor.runPrj()

    def keep(self) -> None:
        self.edaCtrl.agtVendor.runKeep()

    def lint(self) -> None:
        self.edaCtrl.agtLint.runLint()

    def sim(self) -> None:
        self.edaCtrl.agtSim.runSim()

    def up(self) -> None:
        if (self.args.vendor == "microsemi"):
            self.edaCtrl.agtVendor.runUp()
        else:
            """Placeholder for future JTAG or GUI upload commands."""
            print('this command is only valid for microsemi flow, skipping')


    def sta(self) -> None:
        self.edaCtrl.agtVendor.runSta()

    def netlist(self) -> None:
        self.edaCtrl.agtVendor.runNetlist()

    def jtag(self) -> None:
        self.edaCtrl.agtVendor.runJtag()



    def report(self) -> None:
        self.edaCtrl.agtVendor.runReport()

    def start(self) -> None:
        """Composite command to create and/or build a project.

        The ``-b`` or ``--action`` flag may contain multiple
        characters; each character triggers an action in a well defined
        order.  For example ``csrd`` will perform creation, synthesis,
        routing and display in sequence.  Unknown characters are
        ignored.
        """
        action_map: Dict[str, Callable[[], None]] = {
            'c': self.create,
            's': self.synth,
            'r': self.route,
            't': self.sta,
            'b': self.bit,
            'd': self.prj,
        }
        for flag in self.args.action:
            func = action_map.get(flag)
            if func:
                func()

    def restart(self) -> None:
        """Delete all build artefacts and rerun the start sequence."""
        self.delete()
        self.start()


    def create(self) -> None:
        """Create a new project directory and initialise vendor data."""
        if not os.path.exists(self.args.path):
            os.makedirs(self.args.path)
        self.edaCtrl.agtVendor.runCreate()

    def delete(self) -> None:
        """Remove generated artefacts for a clean build."""
        # Directories to delete recursively
        dirs = [
            self.args.path,
            '.bpad',
            '.simvision',
            'questa/aldec',
            'questa/common',
            'questa/mentor',
            'questa/synopsys',
            'questa/xcelium',
            'xcelium/common',
            'xcelium/libraries_ext',
            'xcelium/libraries_ip',
            'xcelium/libraries_tb',
            'xcelium/logs',
            'xcelium/xcelium',
        ]
        for d in dirs:
            if os.path.isdir(d):
                shutil.rmtree(d)
        # Files to remove
        files = [
            'transcript',
            'xcelium/cds.lib',
            'xcelium/hdl.var',
        ]
        for f in files:
            if os.path.isfile(f):
                os.remove(f)
        print('environment successfully deleted')

    def update(self) -> None:
        """Update scripts from the framework into the current project.

        Scripts are copied from the framework's internal ``framework``
        directory into the project root.  Certain folders and files
        (like manifests and wave files) are deliberately skipped to
        avoid accidental overwrites.  Existing destination folders are
        deleted prior to copying to ensure a clean update.
        """
        skip_folders = {'manifests', 'wave', 'ci_cd.yaml'}
        framework_folder = 'framework'
        script_folder = 'scripts'
        frm_dir = os.getcwd()
        frm_path = os.path.abspath(self.frm_file)
        frm_root = os.path.dirname(frm_path)
        source_folder = os.path.join(frm_root, framework_folder, script_folder)
        for entry in os.listdir(source_folder):
            if entry in skip_folders:
                continue
            src = os.path.join(source_folder, entry)
            dst = os.path.join(frm_dir, entry)
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            if os.path.isfile(src):
                shutil.copy2(src, dst)
            else:
                print(f'update {entry}')
                shutil.copytree(src, dst)

    def man(self) -> None:
        """Display the manual for the framework."""
        subprocess.call(['python3', f'{self.frm_path}/{self.script_path}/man/manual.py'])

    def hier(self) -> None:
        """Display the module hierarchy."""
        subprocess.call(['python3', f'{self.frm_path}/{self.script_path}/hierarchy/hierarchy.py'])

    def module(self) -> None:
        """Run the file handler module."""
        subprocess.call(['python3', f'{self.frm_path}/{self.script_path}/file_handler/file_handler.py'])

    def auto(self) -> None:
        """Execute a shell script at the project path."""
        subprocess.call(['/bin/bash', self.args.path])

    def populate(self) -> None:
        """Print the packages path used by the framework."""
        print(self.packages_path)