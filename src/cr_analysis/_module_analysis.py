"""KPI evolution functionality"""
#=============#
#== IMPORTS ==#
#=============#
#: Std. modules, libraries
from pathlib import Path

#: External modules, libraries
from rich import print

#: Internal modules, libraries
from ._utils import (
    loading_data,
    counting_affiliations,
    counting_occurrence,
    counting_main_types,
    workload_distribution,
    tickets_per_month
)

from ._constants import current_year

#===============#
#== FUNCTIONS ==#
#===============#

#--
def reports_analysis(
    reports: Path,
    year: int = current_year,
    center: str = 'all'
):
    """Extract KPI's based on center and year. Only output."""
    #===== Initialization =============================#
    #===== Sub-Functions ==============================#

    #===== Routine ====================================#
    df = loading_data(reports=reports, year=year, center=center)
    #===== End Routine ================================#
    
    #===== Output =====================================#
    print("==============")
    print("QUICK ANALYSIS")
    print("==============")
    if center == 'all':
        #-- Affiliation count by consultant and expert centers
        print("\n----------------------------------------------\n")
        print(f"[bold]Affiliation Counts for Consultants in {year}:[/bold]\n")
        print(counting_affiliations(dataframe=df, column='consultants'))
        print("\n----------------------------------------------\n")
        print(f"[bold]Affiliation Counts for Experts in {year}:[/bold]\n")
        print(counting_affiliations(dataframe=df, column='experts'))
        print("\n----------------------------------------------\n")
        print(f"[bold]Affiliation Counts Overall in {year}:[/bold]\n")
        print(counting_affiliations(dataframe=df, column='consultants', add="experts", output='relative'))

    print("\n----------------------------------------------\n")
    print( "[bold]Average/Median workload per ticket in days[/bold]",
          f"{df['final_workload'].mean().round(2)} | {df['final_workload'].median().round(2)}"
    ) 
    print("\n----------------------------------------------\n")
    print(f"[bold]Request Types in {year} for [green]{center}[/green]:[/bold]\n")
    print(counting_occurrence(dataframe=df, column='request_types', output='relative'))
    print("\n----------------------------------------------\n")
    print(f"[bold]Main Request Types in {year} for [green]{center}[/green]:[/bold]\n")
    print(counting_main_types(dataframe=df, output='relative'))
    print("\n----------------------------------------------\n")
    print(f"[bold]Average workload distribution, % in {year} for [green]{center}[/green]:[/bold]\n")
    print(workload_distribution(df)[['category','percentage']])
    print("\n----------------------------------------------\n")
    print(f"[bold]Ticket request distribution per month in {year} for [green]{center}[/green]:[/bold]\n")
    print(tickets_per_month(df))
    #=== End Output ===================================#

    return df
