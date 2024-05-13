#=============#
#== IMPORTS ==#
#=============#

#: Std. libraries
from pathlib import Path

#: External modules,libraries
import pandas
import yaml

try:
    # Attempt to use CLoader
    from yaml import CLoader as YAML_Loader
except ImportError:
    # Fallback to regular Loader if CLoader is not available
    from yaml import BaseLoader as YAML_Loader

#: Internal modules,libraries
from ._constants import (
    REQUEST_MAIN_TYPES,
    month_names
)

#===============#
#== FUNCTIONS ==#
#===============#

#-- Loading the yaml file
def loading_yaml_to_pathlib_glob(reports: Path):

    reports = Path(reports)

    #-- In case where a single file is provided
    if reports.is_file():
        yaml_files = [reports]
    else:
        yaml_files = reports.glob("*.yml")

    return yaml_files

#-- Loading the yaml to a pandas dataframe
def loading_yaml_to_dataframe(reports: Path):

    data_list = []

    yaml_files = loading_yaml_to_pathlib_glob(reports)

    #-- Read and parse yaml linter output
    for filename in yaml_files:
        with open(filename, "r", encoding="utf-8") as file:
            data = yaml.load(file,Loader=YAML_Loader)
            data_list.append(data)

    return pandas.DataFrame(data_list)

#--
def loading_data(
    reports: Path,
    year: int, 
    center: str
):
    #-- Loading the dataset
    df = loading_yaml_to_dataframe(reports=reports)

    #-- Setting datetime to the pandas datetime format
    df['start_date'] = pandas.to_datetime(df['start_date'])
    df['end_date']   = pandas.to_datetime(df['start_date'])

    #-- Filtering tickets based on the year
    #df = df[(df['start_date'].dt.year == report_year) | (df['end_date'].dt.year == report_year)]
    df = df[df['end_date'].dt.year == year]

    #-- Filtering per affiliation
    if center != 'all':
        #----- Statistics about consultants center --------#
        center_consultant_list = []
        for i in range(len(df)):
            if len(df['consultants'].iloc[i]) > 0:
                if df['consultants'].iloc[i][0]['affiliation'] == center :
                    center_consultant_list.append(i)

        df = df.iloc[center_consultant_list]

    return df

#------------------------------------------------------#
def counting_affiliations(
    dataframe: pandas.DataFrame,
    column: str,
    add: str = "None",
    output: str = "relative"
) -> pandas.Series:
    """Counts affiliations absolute, relative"""
    ##----- Initialization ----------------------------#
    affiliations = []

    #----- Routine ------------------------------------#
    for entry in dataframe[column]:
        if isinstance(entry, list):
            for person in entry:
                affiliations.append(person['affiliation'])

    if add != "None":
        for entry in dataframe[add]:
            if isinstance(entry, list):
                for person in entry:
                    affiliations.append(person['affiliation'])

    count_dict = pandas.Series(affiliations).value_counts()
    #----- End Routine --------------------------------#

    #----- Output -------------------------------------#
    if output == 'relative':
        return count_dict/count_dict.sum()
    elif output == 'absolute':
        return count_dict
    else:
        raise TypeError("Wrong given output. Available output types are: relative|absolute")

#------------------------------------------------------#
def counting_occurrence(
    dataframe: pandas.DataFrame,
    column: str,
    output: str = 'relative'
) -> pandas.Series:
    """Counts based on tags; absolute, relative output"""
    tags = pandas.Series([tag for sublist in dataframe[column].dropna() for tag in sublist]).value_counts()

    if output == 'relative':
        return tags/tags.sum()
    elif output == 'absolute':
        return tags
    else:
        raise TypeError("Wrong given output. Available output types are: relative|absolute")

#--
def counting_main_types(
    dataframe: pandas.DataFrame,
    output: str = 'relative'
) -> pandas.Series:
    """Counts based on main request types (SE, LEGAL, PRAC)"""
    request_main_types_counts = {category: 0 for category in REQUEST_MAIN_TYPES}
    for i, val in enumerate(REQUEST_MAIN_TYPES):
        #-- create a regular expression pattern and apply it to the pandas.Series
        mypattern = '|'.join(REQUEST_MAIN_TYPES[val])
        request_main_types_counts[val] = sum(
            dataframe['request_types'].apply(
                lambda x: any(pandas.Series(x).str.contains(mypattern))
                )
            )
    maintypes = pandas.Series(request_main_types_counts)

    maintypes.name = 'count'

    if output == 'relative':
        return maintypes/maintypes.sum()
    elif output == 'absolute':
        return maintypes
    else:
        raise TypeError("Wrong given output. Available output types are: relative|absolute")

#--
def workload_distribution(df):
    """Calculate the workload distribution"""
    workload_data = df["workload_percentage_distribution"].apply(pandas.Series)
    workload_average = (
        workload_data.mean()
        .reset_index()
        .rename(columns={"index": "category", 0: "value"})
    )

    #-- Round the percentage values
    workload_average["percentage"] = workload_average["value"].round(1)

    workload_average['value'] /= 100
    return workload_average

#--
def tickets_per_month(
    dataframe: pandas.DataFrame
) -> pandas.Series:
    """Ticket starting count per month"""
    months = pandas.Series(0, index=range(1, 13), name="Counts")

    monthly_requests = (
        dataframe["start_date"]
        .groupby([dataframe["start_date"].dt.month])
        .count()
        .reset_index(name="Count")
        .rename(columns={"start_date": "Months"})
    ).set_index("Months")["Count"]

    for month in monthly_requests.index:
        months[month] = monthly_requests[month]

    months.rename(index=month_names, inplace=True)

    return months

    #date_index = [f"{year}-{month:02d}" for year, month in monthly_requests.index]
