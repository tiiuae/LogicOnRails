"""
project_parser.py
~~~~~~~~~~~~~~~~~~

This module defines :class:`ProjectParser` which is responsible for
loading user and default YAML configuration files, parsing runtime
arguments and translating them into environment variables.  It
consolidates functionality previously spread across the original
`frmParser.py` file, grouping related operations into concise helper
methods.  Environment variable assignment is driven by a mapping
structure rather than repetitive manual assignments, making the code
both shorter and easier to maintain.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, Tuple, Any
import yaml


class ProjectParser:
    """Parse project configuration and command line arguments.

    A two stage configuration mechanism is employed by the framework:
    first a YAML file is read to obtain defaults, and then command
    line arguments override selected values.  The parsed arguments are
    stored in a namespace returned to the caller along with a list of
    unparsed strings which identify the action to perform.  Finally
    environment variables are populated to allow downstream tools to
    operate without explicitly passing all options around.
    """

    def __init__(self, frm_file: str, user_yaml: str = 'config.yaml', default_yaml: str = 'ci_cd.yaml') -> None:
        self.frm_file = frm_file
        self.user_yaml = user_yaml
        self.default_yaml = default_yaml
        # Ensure we are running in a directory that contains the
        # configuration file; search current and parent directory
        self._change_into_project_dir()
        # Load configuration from YAML
        self.config: Dict[str, Any] = self._load_yaml()
        # Decompose top level keys into attributes for convenience
        self.system = self.config.get('system', {})
        self.prj = self.config.get('prj', {})
        self.simulation = self.config.get('simulation', {})
        self.manifests = self.config.get('manifests', {})
        self.questa = self.config.get('questa', {})
        self.modelsim = self.config.get('modelsim', {})
        self.verilator = self.config.get('verilator', {})
        self.quartus = self.config.get('quartus', {})
        self.vivado = self.config.get('vivado', {})
        self.libero = self.config.get('libero', {})
        self.gowin = self.config.get('gowin', {})
        self.cadence = self.config.get('cadence', {})

    # -- configuration loading -------------------------------------------

    def _change_into_project_dir(self) -> None:
        """Change the working directory so that the user YAML file is
        discoverable.

        The framework first looks for ``user_yaml`` in the current
        directory; if not found it will search the parent directory and
        change into it.  If the file cannot be found in either place
        the program terminates with a message.  This mirrors the
        behaviour of the original implementation but avoids silent
        continuation when no configuration exists.
        """
        if os.path.exists(self.user_yaml):
            return
        parent = os.path.join(os.getcwd(), '..')
        if os.path.exists(os.path.join(parent, self.user_yaml)):
            os.chdir(parent)
            return
        print(f'no {self.user_yaml} file on the current folder or on the parent folder')
        sys.exit(1)

    def _load_yaml(self) -> Dict[str, Any]:
        """Load configuration from YAML.

        If the user specified YAML file exists it is loaded; otherwise
        the default YAML is used.  All keys remain unmodified to
        preserve backwards compatibility with existing configuration
        files.
        """
        cfg_path = self.user_yaml if os.path.exists(self.user_yaml) else self.default_yaml
        with open(cfg_path, 'r', encoding='utf-8') as fh:
            print(f'configuring env using {cfg_path}')
            return yaml.safe_load(fh) or {}

    # -- argument parsing ------------------------------------------------

    def parse_inputs(self) -> Tuple[argparse.Namespace, list[str]]:
        """Parse command line arguments following the initial stage.

        A large number of options are supported; most simply override
        corresponding values from the YAML configuration.  Unknown
        arguments are collected into a list which identifies the
        requested action (e.g. ``['synth']``).  See the framework
        documentation for a full description of each option.

        :returns: a tuple of the parsed namespace and a list of
            unparsed positional arguments.
        """
        parser = argparse.ArgumentParser(description='Framework runtime options')
        # Build up a sequence of arguments along with their defaults
        # derived from the loaded YAML.  Where the YAML does not
        # provide a value an empty string is used.
        parser.add_argument('-v', '--vendor', default=self.system.get('vendor', ''), help='System - Vendors name')
        parser.add_argument('-f', '--firmware', '--fw', default=self.prj.get('firmware', ''), help='Project - Firmware folder path')
        parser.add_argument('-p', '--path', default=self.prj.get('path', ''), help='Project - Project Path')
        parser.add_argument('-U', '--uproc', default=self.prj.get('uproc', ''), help='Project - Processor type')
        parser.add_argument('-M', '--message', default=self.prj.get('message_lvl', ''), help='Project - Message Level')
        parser.add_argument('-K', '--keep', nargs='?', const='on', default=self.system.get('keep', ''), help='System - Keep tool generated files')
        parser.add_argument('-s', '--simulator', '--sim', default=self.system.get('simulator', ''), help='System - Simulator to be used')
        parser.add_argument('-a', '--access', '--acc', default=self.simulation.get('access', ''), help='Simulation - Access Option')
        parser.add_argument('-c', '--coverage', '--cov', nargs='?', const='on', default=self.simulation.get('coverage', ''), help='Simulation - Coverage option')
        parser.add_argument('-i', '--dpi', nargs='?', const='on', default=self.simulation.get('dpi', ''), help='Simulation - testbench SV DPI enable')
        parser.add_argument('-o', '--comp_opt', '--compile', default=self.simulation.get('comp_opt', ''), help='Simulation - Netlist or Coverage')
        parser.add_argument('-g', '--gui', nargs='?', const='on', default=self.simulation.get('gui', ''), help='Simulation - Graphical User Interface mode')
        parser.add_argument('-u', '--uvm', nargs='?', const='on', default=self.simulation.get('uvm', ''), help='Simulation - Enables UVM include')
        parser.add_argument('-y', '--default_test', nargs='?', const='on', default=self.simulation.get('default_test', ''), help='Simulation - Default test for UVM')
        parser.add_argument('-t', '--tb', '--testbench', nargs='?', const='on', default=self.simulation.get('tb', ''), help='Simulation - Test Bench')
        parser.add_argument('-w', '--wave', '--wv', default=self.simulation.get('wave', ''), help='Simulation - Path to sim wave file')
        parser.add_argument('-z', '--defines_sim', '--dsim', default=self.simulation.get('defines_sim', ''), help='Project - Simulation defines')
        parser.add_argument('-m', '--module_name', '--name', default=self.prj.get('module_name', ''), help='Project - Top module name')
        parser.add_argument('-e', '--ext_modules', '--ext', default=self.prj.get('ext_modules', ''), help='Project - External Modules enable')
        parser.add_argument('-d', '--defines_syn', '--dsyn', default=self.prj.get('defines_syn', ''), help='Project - Synthesis defines')
        parser.add_argument('-k', '--constraints', '--constr', default=self.prj.get('constraints', ''), help='Project - Constraints path')
        parser.add_argument('-r', '--report', default='summary', help='Reports - Report to be printed')
        parser.add_argument('-x', '--ignore', default='', help='Reports - Substring to be ignored in the reports')
        parser.add_argument('-l', '--log', '--logs', nargs='?', const='on', default=self.prj.get('log', ''), help='Project - Dump logs')
        parser.add_argument('-n', '--level', default='0', help='Reports - level of the utilization report gui')
        parser.add_argument('-b', '--action', default='', help='Stages, c creates syn r route d display')
        parser.add_argument('-B', '--mf_tb', default=self.manifests.get('source_tb', ''), help='Manifest - TB')
        parser.add_argument('-R', '--mf_rtl', default=self.manifests.get('source_rtl', ''), help='Manifest - RTL')
        parser.add_argument('-I', '--mf_inc', default=self.manifests.get('source_inc', ''), help='Manifest - INCLUDE')
        parser.add_argument('--yaml', default='', help='Pre Run option, select which yaml to use')
        # Parse known arguments and capture the remainder as the requested action
        args, unknown = parser.parse_known_args()
        # If a yaml override is supplied update our yaml path for future steps
        if args.yaml:
            self.user_yaml = args.yaml
        return args, unknown

    # -- environment variable population ---------------------------------

    def populate_env(self, args: argparse.Namespace) -> None:
        """Populate environment variables for downstream tools.

        A mapping of environment variable names to either computed
        values or values extracted from the YAML configuration is used
        to drive assignment.  This greatly reduces code repetition
        compared with the original implementation and makes the intent
        explicit.  Any missing values default to an empty string.
        """
        # Helper to safely fetch a value from a configuration section
        def get(section: Dict[str, Any], key: str) -> str:
            return str(section.get(key, ''))

        # Basic file based environment variables derived from args
        dynamic_files = {
            'source_sdc': f'{args.constraints}/{args.module_name}.sdc',
            'source_pins': f'{args.constraints}/{args.module_name}.pin',
            'quartus_config': f'{args.constraints}/{args.module_name}.altera_cnfg',
            'quartus_stp': f'{args.constraints}/{args.module_name}.stp',
            'vivado_xdc': f'{args.constraints}/{args.module_name}.xdc',
            'libero_iopdc': f'{args.constraints}/{args.module_name}_io.pdc',
            'libero_fppdc': f'{args.constraints}/{args.module_name}_fp.pdc',
            'quartus_part': f'{args.constraints}/{args.module_name}.partition',
        }
        for env_name, value in dynamic_files.items():
            os.environ[env_name] = value

        # Simple mappings from arguments to environment names
        args_map = {
            'scripts_only': self.system.get('scripts_only', ''),
            'linter': self.system.get('linter', ''),
            'rev': self.prj.get('rev', ''),
            'prj_path': args.path,
            'module_name': args.module_name,
            'vendor': args.vendor,
            'prj_constraint': args.constraints,
            'gui': args.gui,
            'log': args.log,
            'keep': args.keep,
            'tb': args.tb,
            'wave': args.wave,
            'coverage': args.coverage,
            'access': args.access,
            'synth_def': args.defines_syn,
            'sim_def': args.defines_sim,
            'default_test': args.default_test,
            'message_lvl': args.message,
            'uproc': args.uproc,
            'firmware_path': args.firmware,
            'ext_modules': args.ext_modules,
            'comp_opt': args.comp_opt,
            'uvm': args.uvm,
            'dpi': args.dpi,
            'ignore': args.ignore,
        }
        for env_name, value in args_map.items():
            os.environ[env_name] = str(value)

        # Manifests and optional sources
        manifest_map = {
            'source_rtl': args.mf_rtl,
            'source_tb': args.mf_tb,
            'source_inc': args.mf_inc,
            'source_ips': self.manifests.get('source_ips', ''),
            'source_ext': self.manifests.get('source_ext', ''),
            'source_lib': self.manifests.get('source_lib', ''),
            'source_soft': self.manifests.get('source_soft', ''),
            'source_netlist': self.manifests.get('source_netlist', ''),
            'source_bb': self.manifests.get('source_bb', ''),
            'source_uvm': self.manifests.get('source_uvm', ''),
        }
        for env_name, value in manifest_map.items():
            os.environ[env_name] = str(value)

        # Vendor specific options
        vendor_opts = {
            'verilator_opt': (self.verilator, 'verilator_warn_options'),
            'questa_sim_opt': (self.questa, 'sim_opt'),
            # ModelSim
            'modelsim_skip_vopt': (self.modelsim, 'skip_vopt'),
            'modelsim_sim_vopt': (self.modelsim, 'sim_vopt'),
            'modelsim_sim_vsim': (self.modelsim, 'sim_vsim'),
            'modelsim_sim_vlog': (self.modelsim, 'sim_vlog'),
            'modelsim_sim_vcom': (self.modelsim, 'sim_vcom'),
        }
        for env_name, (section, key) in vendor_opts.items():
            os.environ[env_name] = get(section, key)

        # Quartus, Libero, Vivado, Gowin, Cadence categories
        complex_categories = [
            (self.quartus, {
                'quartus_version': 'quartus_version',
                'quartus_device': 'quartus_device',
                'quartus_family': 'quartus_family',
                'quartus_synth_opt': 'synth_opt',
                'quartus_pr_opt': 'pr_opt',
                'quartus_sim_opt': 'sim_opt',
                'quartus_sta_opt': 'sta_opt',
                'quartus_sta_bit': 'bit_opt',
            }),
            (self.libero, {
                'libero_device': 'libero_device',
                'libero_family': 'libero_family',
                'libero_package': 'libero_package',
                'libero_pdc_oride': 'pdc_override',
                'libero_pdc_folder': 'pdc_folder',
                'libero_die': 'libero_die',
                'libero_synth_opt': 'synth_opt',
                'libero_pr_opt': 'pr_opt',
                'libero_sim_opt': 'sim_opt',
                'libero_sta_opt': 'sta_opt',
                'libero_prebit_opt': 'prebit_opt',
                'libero_bit_opt': 'bit_opt',
                'libero_up_opt': 'up_opt',
            }),
            (self.vivado, {
                'vivado_device': 'vivado_device',
                'vivado_synth_opt': 'synth_opt',
                'vivado_pr_opt': 'pr_opt',
                'vivado_sim_opt': 'sim_opt',
                'vivado_sta_opt': 'sta_opt',
                'vivado_bit_bit': 'bit_opt',  # see note below
            }),
            (self.gowin, {
                'gowin_device': 'gowin_device',
                'gowin_synth_opt': 'synth_opt',
                'gowin_pr_opt': 'pr_opt',
                'gowin_sim_opt': 'sim_opt',
                'gowin_sta_opt': 'sta_opt',
                'gowin_sta_bit': 'bit_opt',
            }),
            (self.cadence, {
                'cadence_lef': 'lef_file',
                'cadence_def': 'def_file',
                'cadence_lib': 'lib_file',
                'cadence_saif': 'saif_file',
                'cadence_cap': 'cap_file',
                'cadence_spef': 'spef_file',
                'cadence_gds2': 'gds2_file',
                'cadence_qrc': 'qrc_file',
                'cadence_cpf': 'cpf_file',
                'cadence_lp_syn': 'low_power_flow',
                'cadence_dbg_syn': 'dbg_flow',
                'cadence_phy_syn': 'phy_flow',
                'cadence_ispt_syn': 'ispatial_flow',
                'cadence_scanc_syn': 'scanc_flow',
                'cadence_atpg_syn': 'atpg_flow',
                'cadence_lec_syn': 'lec_flow',
                'cadence_synth_opt': 'synth_opt',
                'cadence_pr_opt': 'pr_opt',
                'cadence_sim_opt': 'sim_opt',
                'cadence_sta_opt': 'sta_opt',
                'cadence_bit_opt': 'bit_opt',
            }),
        ]
        
        for section, mapping in complex_categories:
            for env_name, key in mapping.items():
                os.environ[env_name] = get(section, key)
        
        # Flags derived from simple boolean settings
        os.environ['access_opt'] = '+acc' if args.access == 'on' else ''
        os.environ['dpi_opt'] = '-dpiheader' if args.dpi == 'on' else ''

        # Miscellaneous environment variables
        os.environ['reports_path'] = 'reports/'
        # Remove the trailing script name (e.g. frl) from frm_file
        os.environ['frm_path'] = self.frm_file.replace(os.path.basename(self.frm_file), '')
        os.environ['script_path'] = 'classes/agents/scripts'