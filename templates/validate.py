import datetime
import json
import os

import click
import jsonschema
import yaml

try:
    from yaml import CLoader as YamlLoader
except ImportError:
    from yaml import YamlLoader


@click.command()
@click.argument(
    "consulting-reports", nargs=-1, type=click.Path(exists=True, dir_okay=False)
)
@click.option(
    "--schema-file", required=True, type=click.Path(exists=True, dir_okay=False)
)
@click.pass_context
def validate_reports(ctx, consulting_reports, schema_file):
    """Validate all given yml files according to the provided JSON-Schema."""
    # Ensure color output in GitLab CI
    if "CI" in os.environ:
        ctx.color = True

    exit_code = 0

    with open(schema_file, "r") as schemafile_object:
        schema = json.load(schemafile_object)
    validator = jsonschema.Draft7Validator(schema)

    for file in consulting_reports:
        with open(file, "r", encoding='utf-8') as yamlfile:
            try:
                report = yaml.load(yamlfile, Loader=YamlLoader)
            except yaml.YAMLError as e:
                click.secho(f"Error while loading {file}", fg="red")
                if hasattr(e, "problem_mark"):
                    mark = e.problem_mark
                    click.secho(
                        f"  Error position: (Line {mark.line+1}:Column {mark.column+1})",
                        fg="red",
                    )
        # Convert datetime objects to ISO8601 string
        report = {
            key: report[key]
            if not isinstance(report[key], (datetime.date, datetime.datetime))
            else report[key].isoformat()
            for key in list(report)
        }

        if validator.is_valid(report):
            click.secho(f"{file}: Validation succeeded", fg="green")
        else:
            click.secho(f"{file}: Validation failed", fg="red")
            exit_code += 1
            for error in validator.iter_errors(report):
                click.secho(f"  * {error.message} at {error.absolute_schema_path}", fg="red")
                for c in error.context:
                    click.secho(f"\t\tContext: {c.message} at {c.absolute_schema_path}", fg="red")


        # Check if workload_percentage_distribution sums up to 100
        if 0 > sum(report["workload_percentage_distribution"].values()) < 100:
            exit_code += 1
            click.secho(
                f"{file}: Workload % distribution doesn't add up to 100", fg="red"
            )

    # Make sure to exit with a code other than zero to notify GitLab CI
    exit(exit_code)


if __name__ == "__main__":
    validate_reports()
