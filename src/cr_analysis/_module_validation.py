#=============#
#== IMPORTS ==#
#=============#

#: Std. libraries
from pathlib import Path
import datetime

#: External modules, libraries
import json
import jsonschema
import yaml
from rich import print

#: Internal modules, libraries
from ._utils import loading_yaml_to_pathlib_glob


#===============#
#== FUNCTIONS ==#
#===============#

#----------------------#
#-- validate_reports --#
#----------------------#
def reports_validation(
    reports: Path,
    schema_file: Path,
    ):
    """
    Validate report files against a JSON schema.

    This function checks the correctness and validity of report YAML files against a JSON schema.
    It prints validation results and exits with a non-zero exit code if any errors are found.

    :param reports: A path to a single YAML file or a directory containing YAML files to be validated.
                    The default is the 'reports/' directory.
    :param schema_file: A path to the JSON schema file used for validation.
                    The default is './templates/consultation-report.schema.json'.
    :returns: error id, if set to 1 it it indicate an error.
    """

    errors = False

    yaml_files = loading_yaml_to_pathlib_glob(reports)

    with open(schema_file, "r", encoding="utf-8") as schema_file_object:
        schema = json.load(schema_file_object)

    validator = jsonschema.Draft7Validator(schema)

    for filename in yaml_files:
        #-- open each file
        with open(filename, "r", encoding="utf-8") as file:
            try:
                report = yaml.safe_load(file)
            except yaml.YAMLError as e:
                errors = True
                print(f"[bold red]Error while loading {filename}[/bold red]")
                if hasattr(e, "problem_mark"):
                    mark = e.problem_mark
                    print(f"  Error position: (Line {mark.line}:Column {mark.column + 1})")

            # Convert datetime objects to ISO8601 string
            report = {
                key: report[key]
                if not isinstance(report[key], (datetime.date, datetime.datetime))
                else report[key].isoformat()
                for key in list(report)
            }

            if not validator.is_valid(report):
                errors = True
                print(f"[bold red]{filename}: Validation failed[/bold red]")
                for error in validator.iter_errors(report):
                    print(
                        f"[bold red]  * {error.message} at {error.absolute_schema_path}[/bold red]"
                    )
                    for c in error.context:
                        print(
                            f"[bold red]\t\tContext: {c.message} at {c.absolute_schema_path}[/bold red]"
                        )

            # Check if workload_percentage_distribution sums up to 100
            sum_workload = sum(report["workload_percentage_distribution"].values())
            if sum_workload != 100:
                errors = True
                print(
                    f"[bold red]{filename}: Workload % distribution doesn't add up to 100 (current sum: {sum_workload})[/bold red]"
                )

    #-- Error handling
    if errors == 0:
        print("[green bold]>>> No validation errors found! <<<[/green bold]")
    else:
        exit(code=1)
        #raise typer.Exit(code=1)

    return 0
