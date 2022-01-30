import sys
from pathlib import Path

import cmd2
from creole.setup_utils import assert_rst_readme
from dev_shell.base_cmd2_app import DevShellBaseApp
from dev_shell.command_sets import DevShellBaseCommandSet
from dev_shell.command_sets.dev_shell_commands import DevShellCommandSet as OriginDevShellCommandSet
from dev_shell.command_sets.dev_shell_commands import run_linters
from dev_shell.config import DevShellConfig
from dev_shell.utils.colorful import blue, bright_blue, cyan, print_error
from dev_shell.utils.subprocess_utils import verbose_check_call
from poetry_publish.publish import poetry_publish

import dragonpy
from dragonpy.components.rom import ROMDownloadError
from dragonpy.core.configs import machine_dict


PACKAGE_ROOT = Path(dragonpy.__file__).parent.parent.parent


@cmd2.with_default_category('DragonPy commands')
class DragonPyCommandSet(DevShellBaseCommandSet):
    def do_download_roms(self, statement: cmd2.Statement):
        """
        Download/Test only ROM files
        """
        roms = list(machine_dict.items())
        print(f'Download {len(roms)} platform roms...')
        success = 0
        for machine_name, data in roms:
            machine_config = data[1]
            print(blue(f'Download / test ROM for {bright_blue(machine_name)}:'))

            for rom in machine_config.DEFAULT_ROMS:
                print(f"\tROM file: {cyan(rom.FILENAME)}")
                try:
                    content = rom.get_data()
                except ROMDownloadError as err:
                    print_error(f'Download {err.url!r} -> {err.origin_err}')
                    continue

                size = len(content)
                print(f"\tfile size is ${size:04x} (dez.: {size:d}) Bytes\n")
                success += 1

        print(f'{success} ROMs succeed.')


class DevShellCommandSet(OriginDevShellCommandSet):

    # TODO:
    # pyupgrade --exit-zero-even-if-changed --py3-plus --py36-plus --py37-plus --py38-plus
    # `find . -name "*.py" -type f ! -path "./.tox/*" ! -path "./htmlcov/*" ! -path "*/volumes/*"

    def do_publish(self, statement: cmd2.Statement):
        """
        Publish "dev-shell" to PyPi
        """
        # don't publish if README is not up-to-date:
        assert_rst_readme(package_root=PACKAGE_ROOT, filename='README.creole')

        # don't publish if code style wrong:
        run_linters()

        # don't publish if test fails:
        verbose_check_call('pytest', '-x')

        poetry_publish(
            package_root=PACKAGE_ROOT,
            version=dragonpy.__version__,
            creole_readme=True,  # don't publish if README.rst is not up-to-date
        )


class DevShellApp(DevShellBaseApp):
    pass


def get_devshell_app_kwargs():
    """
    Generate the kwargs for the cmd2 App.
    (Separated because we needs the same kwargs in tests)
    """
    config = DevShellConfig(package_module=dragonpy)

    # initialize all CommandSet() with context:
    kwargs = dict(config=config)

    app_kwargs = dict(
        config=config,
        command_sets=[
            DragonPyCommandSet(**kwargs),
            DevShellCommandSet(**kwargs),
        ],
    )
    return app_kwargs


def devshell_cmdloop():
    """
    Entry point to start the "dev-shell" cmd2 app.
    Used in: [tool.poetry.scripts]
    """
    c = DevShellApp(**get_devshell_app_kwargs())
    sys.exit(c.cmdloop())
