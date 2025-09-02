"""
config_manager.py
~~~~~~~~~~~~~~~~~~

This module exposes :class:`ConfigManager` which is responsible for
handling the high‑level project creation and clean‑up commands for the
hardware framework.  It centralises logic related to parsing the
initial command line arguments used to bootstrap a new project or
destroy an existing one.  It also hides details about the on‑disk
layout of templates and configuration files, making it easy to
generate or purge a project directory with a single method call.

The original implementation mixed argument parsing with side effects in
the constructor.  In this refactored version the logic is pulled
together into compact helper methods and sensible defaults are
factored into a dictionary.  A simple mapping is used to handle
options that take a value (e.g. ``--prj``) and those that toggle
behaviour (e.g. ``--pps``).  Project names are replaced in both
filenames and manifest content without shelling out to external
utilities.  When a generate or purge command is executed the process
terminates early, mirroring the behaviour of the original script.
"""

from __future__ import annotations

import os
import shutil
import sys
from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class InitOptions:
    """Structure holding the parsed initial options used to generate
    or purge a project.  Each field corresponds to a command line
    switch and carries either a user supplied value or a sensible
    default.  The ``define`` field derives its value from
    ``vendor``.
    """

    per_prj_scripts: str
    prj_name: str
    folder: str
    sim: str
    lint: str
    vendor: str
    yaml: str
    define: str

    @classmethod
    def from_args(cls, argv: List[str], defaults: Dict[str, str]) -> "InitOptions":
        """Parse the first stage command line options.

        The :mod:`argparse` module is deliberately avoided here because
        this parser only deals with a handful of flags and the
        semantics differ slightly from the subsequent stage which uses
        :mod:`argparse`.  Boolean flags like ``--pps`` flip a
        default value, whereas flags like ``--prj`` consume the
        following argument.  Unknown flags are ignored at this stage
        and passed through to the second stage.

        :param argv: the raw argument vector as provided by
            :data:`sys.argv`.
        :param defaults: mapping of default values for each option.
        :returns: an instance of :class:`InitOptions` populated from
            ``argv`` or ``defaults``.
        """
        # Helper to fetch a value following a flag or fall back to a
        # default.  If the flag appears but no value follows it the
        # default is used and the missing value is silently ignored.
        def get_value(flag: str, default: str) -> str:
            try:
                idx = argv.index(flag)
                return argv[idx + 1]
            except (ValueError, IndexError):
                return default

        # Boolean toggle for per project scripts
        per_prj_scripts = (
            '"per_prj_script:"off""'
            if '--pps' in argv
            else '"per_prj_script:"on""'
        )

        prj_name = get_value('--prj', defaults['prj_name'])
        folder = get_value('--nm', defaults['folder'])
        sim = get_value('--sm', defaults['sim'])
        lint = get_value('--lt', defaults['lint'])
        vendor = get_value('--vr', defaults['vendor'])
        yaml_file = get_value('--yaml', defaults['yaml'])

        # Derive the define macro based on vendor selection
        if 'xilinx' in vendor.lower():
            define = '+define+XILINX'
        elif 'microsemi' in vendor.lower():
            define = '+define+MICROSEMI'
        else:
            define = '+define+ALTERA'

        return cls(
            per_prj_scripts=per_prj_scripts,
            prj_name=prj_name,
            folder=folder,
            sim=sim,
            lint=lint,
            vendor=vendor,
            yaml=yaml_file,
            define=define,
        )


class ConfigManager:
    """Manage creation and destruction of project directories.

    This class encapsulates the logic required to bootstrap a new
    project based off a template directory, as well as removing an
    existing project directory.  It also handles printing version
    information and basic help text.
    """

    #: template directory bundled within the framework
    TEMPLATE_DIR = 'template_folder'
    #: default project name used within the template
    DEFAULT_PROJECT = 'sum'
    #: current framework version string
    VERSION_STR = '######################\n#  1.2.0 - Anchieta  #\n######################'

    def __init__(self, argv: List[str], script_path: str) -> None:
        self.argv = argv
        self.script_path = script_path
        self.curr_dir = os.getcwd()
        # Provide default values for all configurable parameters
        defaults: Dict[str, str] = {
            'prj_name': self.DEFAULT_PROJECT,
            'folder': 'rails',
            'sim': 'questa',
            'lint': 'verilator',
            'vendor': 'altera',
            'yaml': 'config.yaml',
        }
        # Parse high level options
        self.init_opts = InitOptions.from_args(argv, defaults)
        # Determine current yaml file used later in the flow
        self.curr_yaml: str = self.init_opts.yaml

    # -- public API -------------------------------------------------------

    def handle(self) -> bool:
        """Entry point for handling top level commands.

        The supported commands are ``generate``, ``purge`` and
        ``help``.  When one of these commands is executed the process
        terminates after performing its side effect; returning
        ``False`` to the caller.  If no such command is provided
        ``True`` is returned so that the caller may proceed with the
        remainder of the framework pipeline.

        :returns: ``False`` if a command that exits early has been
            processed, otherwise ``True``.
        """
        # Print version information and exit if requested
        if '--version' in self.argv:
            print(self.VERSION_STR)
            return False

        # No subcommand specified; print help by default
        if len(self.argv) < 2:
            self._print_help()
            return False

        cmd = self.argv[1]
        if cmd == 'generate':
            self.generate(self.init_opts)
            return False
        if cmd == 'purge':
            self.purge(self.init_opts)
            return False
        if cmd == 'help':
            self._print_help()
            return False
        # any other command falls through to the rest of the framework
        return True

    # -- command implementations -----------------------------------------

    def generate(self, opts: InitOptions) -> None:
        """Instantiate a new project from the template.

        The template is searched relative to the framework code.  The
        default ``ci_cd.yaml`` file is renamed to ``config.yaml`` and
        the contents are updated to reflect the chosen simulator,
        linter, vendor, project name and synthesis defines.  All
        occurrences of the default project name within manifest files
        are replaced with the user selected project name.  Finally,
        the newly created template tree is moved into the target
        folder defined by ``opts.folder``.
        """
        template_root = self._locate_template()
        if not template_root:
            print(f'corrupted framework folder in {self.TEMPLATE_DIR}')
            return
        # Copy the template structure into a working area
        if os.path.isdir(self.TEMPLATE_DIR):
            shutil.rmtree(self.TEMPLATE_DIR)
        shutil.copytree(template_root, self.TEMPLATE_DIR)
        # Rename ci_cd.yaml to config.yaml
        ci_cd_path = os.path.join(self.TEMPLATE_DIR, 'ci_cd.yaml')
        config_path = os.path.join(self.TEMPLATE_DIR, 'config.yaml')
        if os.path.exists(ci_cd_path):
            shutil.move(ci_cd_path, config_path)
        # Perform in place updates within the yaml file
        self._update_config_yaml(config_path, opts)
        # Rename project specific filenames
        self._rename_project_files(self.DEFAULT_PROJECT, opts.prj_name)
        # Replace project name occurrences in manifests
        self._replace_in_manifests(self.DEFAULT_PROJECT, opts.prj_name)
        # Move the populated template into the user specified folder
        target = opts.folder
        if os.path.isdir(target):
            shutil.rmtree(target)
        shutil.move(self.TEMPLATE_DIR, target)
        print('please configure your project information in the config.yaml file')

    def purge(self, opts: InitOptions) -> None:
        """Remove an existing project directory.

        If the folder specified by ``opts.folder`` exists it is
        recursively deleted.  A message is printed to inform the user
        about the removal.
        """
        target = opts.folder
        if os.path.isdir(target):
            print(f'destroying folder {target}')
            shutil.rmtree(target)

    # -- private helpers --------------------------------------------------

    def _print_help(self) -> None:
        """Display usage information for the framework."""
        print('create a project using rls generate. after that, use rls man to read manual')

    def _locate_template(self) -> Optional[str]:
        """Find the on‑disk location of the template directory.

        The template folder is expected to reside adjacent to the
        framework's Python module.  This method searches the directory
        containing the running script for a folder whose name contains
        :attr:`TEMPLATE_DIR` and returns its full path.

        :returns: full path to the template folder or ``None`` if
            nothing matches.
        """
        frm_dir = os.path.dirname(os.path.abspath(self.script_path))
        for entry in os.listdir(frm_dir):
            full = os.path.join(frm_dir, entry)
            if self.TEMPLATE_DIR in entry and os.path.isdir(full):
                return full
        return None

    def _rename_project_files(self, old_name: str, new_name: str) -> None:
        """Rename any files in the template that contain the default
        project name.

        :param old_name: substring to search for in filenames.
        :param new_name: replacement string.
        """
        for root, _, files in os.walk(self.TEMPLATE_DIR):
            for fname in files:
                if old_name in fname:
                    src = os.path.join(root, fname)
                    dst = os.path.join(root, fname.replace(old_name, new_name))
                    os.rename(src, dst)

    def _update_config_yaml(self, cfg_path: str, opts: InitOptions) -> None:
        """Apply user selections to the configuration yaml file.

        The configuration file contains a handful of sentinel strings
        that are replaced with the user supplied options.  This
        avoids shelling out to external tools (e.g. sed) and keeps
        processing within Python.  The sentinel strings mirror the
        defaults found in the original implementation.
        """
        if not os.path.exists(cfg_path):
            return
        with open(cfg_path, 'r', encoding='utf-8') as fh:
            content = fh.read()
        # Map placeholders in the template to their replacement values
        replacements = {
            '"questa"': f'"{opts.sim}"',
            '"altera"': f'"{opts.vendor}"',
            '"verilator"': f'"{opts.lint}"',
            '"sum"': f'"{opts.prj_name}"',
            '"per_prj_script:"no""': opts.per_prj_scripts,
            '"+define+ALTERA"': f'"{opts.define}"',
        }
        for needle, repl in replacements.items():
            content = content.replace(needle, repl)
        with open(cfg_path, 'w', encoding='utf-8') as fh:
            fh.write(content)

    def _replace_in_manifests(self, old_name: str, new_name: str) -> None:
        """Replace occurrences of the project name inside manifest files."""
        manifests_dir = os.path.join(self.TEMPLATE_DIR, 'manifests')
        if not os.path.isdir(manifests_dir):
            return
        for root, _, files in os.walk(manifests_dir):
            for fname in files:
                fpath = os.path.join(root, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as fh:
                        data = fh.read()
                    if old_name in data:
                        with open(fpath, 'w', encoding='utf-8') as fh:
                            fh.write(data.replace(old_name, new_name))
                except (UnicodeDecodeError, OSError):
                    # Skip binary files or unreadable files silently
                    continue