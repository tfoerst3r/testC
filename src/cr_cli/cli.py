""" CLI for Consulting Reports """
#=============#
#== IMPORTS ==#
#=============#
#-- Std. libraries
from pathlib import Path

#-- External libraries
import typer
from typing_extensions import Annotated

#-- Internal libraries
from cr_analysis import reports_validation
from cr_analysis import reports_linting
from cr_analysis import reports_analysis
from cr_analysis._constants import current_year

try:
    from cr_gui import create_html_report
    from cr_gui import plot_html_analysis
    GUI = True
except ImportError:
    GUI = False

#=====================#
#== Program routine ==#
#=====================#
app = typer.Typer()

#== Typer CLI methods ==#

#-- validate --#
@app.command()
def validate(
    reports: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
        ),
    ] = Path("./reports/"),
    schema_reference_file: Path = Path("./templates/consultation-report.schema.json"),
):
    """Validates the overall consistency of the presented reports."""
    #-- Run function validation_reports
    reports_validation(reports=reports,schema_file=schema_reference_file)

#-- lint --#
@app.command()
def lint(
    reports: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
        ),
    ] = Path("reports/"),
    linter_config: Path = Path(".yamllint.yml")
):
    """ Checks if the yaml files are linted correctly."""
    reports_linting(reports=reports,linter_config=linter_config)


#-- analysis --#
@app.command()
def analysis(
    reports: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
        ),
    ] = Path("reports/"),
    year: int = current_year,
    center: str = 'all',
    ):
    """ Extract most import information for reporting. """
    reports_analysis(reports=reports, year=year, center=center)

    return 0

if GUI:
    #-------------------#
    #-- create_report --#
    #-------------------#
    @app.command()
    def create():
        """
        Creates a report via a HTML interface 
        """
        create_html_report()

        return 0

    @app.command()
    def plot(
        destination: Annotated[
            Path,
            typer.Option(
                exists=False,
                file_okay=True,
                dir_okay=False,
                readable=True,
            ),
        ] = Path("reports.html"),
        reports: Annotated[
            Path,
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=True,
                readable=True,
            ),
        ] = Path("reports/"),
        year: int = current_year,
        center: str = 'all',
    ):
        """
        Creates a HTML with plots based on the CLI analysis output.
        """    
        plot_html_analysis(
            destination=destination,
            reports=reports,
            year=year,
            center=center
        )
