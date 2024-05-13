#=============#
#== IMPORTS ==#
#=============#

#: Std. libraries
from pathlib import Path

#: External modules, libraries
from yamllint.config import YamlLintConfig
from yamllint import linter
from rich import print
from rich.table import Table
from rich.console import Console

#: Internal modules, libraries
from ._utils import loading_yaml_to_pathlib_glob

#===============#
#== FUNCTIONS ==#
#===============#

#-----------------#
#-- lint_report --#
#-----------------#
def reports_linting(
    reports: Path,
    linter_config: Path
):
    """Lint report files using a specified YAML linter configuration.

    This function checks the correctness of YAML report files using a specified YAML lint configuration.
    A table of linter errors is displayed for each file containing errors.
    The function exits with a non-zero exit code if any errors are found.

    :param reports: A path to a single YAML file or a directory containing YAML files to be linted.
                    The default is the 'reports/' directory.
    :param linter_config: A path to the YAML lint configuration file. The default is '.yamllint.yml'.
    :raises: typer.Exit with a non-zero exit code if any linter errors are found.
    """
    table = Table(title="Linter errors")
    table.add_column("File", justify="right", style="cyan", no_wrap=True)
    table.add_column("Messages", style="magenta")
    configuration = YamlLintConfig(file=linter_config)

    #-- In case where a single file is provided

    yaml_files = loading_yaml_to_pathlib_glob(reports)

    #-- Read and parse yaml linter output
    for yaml_path in yaml_files:
        with open(yaml_path, "r", encoding="utf-8") as yaml_file:
            gen = linter.run(yaml_file, configuration)
            res = list(gen)
            if len(res) > 0:
                table.add_row(str(yaml_path), str(res))

    if table.rows:
        console = Console()
        console.print(table)
        exit(code=1)
        #raise typer.Exit(code=1)
    else:
        print("[green bold]>>> No linting errors found! <<<[/green bold]")

    return table
