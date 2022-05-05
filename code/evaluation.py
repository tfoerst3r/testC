import argparse
import datetime
import sys
from collections import OrderedDict, Counter, defaultdict
from pathlib import Path

import pandas as pd
import yaml

PATH = r"../reports"

TYPE_CATEGORY_SE = [
    'Qualification',
    'Requirements Management',
    'Software Architecture',
    'Change Management',
    'Design and Implementation',
    'Software Test',
    'Release Management',
    'Automation and Dependency Management'
]

TYPE_CATEGORY_PRAC = [
    'Software or programming language migration',
    'Code audit',
    'Technology and Tool recommendations',
    'Infrastructure support'
]

TYPE_CATEGORY_LEGAL = [
    'Licenses',
    'Open Source',
    'Patent',
    'Contract Suggestions'
]

REQUEST_TYPES = TYPE_CATEGORY_SE + TYPE_CATEGORY_PRAC + TYPE_CATEGORY_LEGAL

WORKLOAD_CATEGORY = [
    'workload_percentage_distribution.communication',
    'workload_percentage_distribution.preparation',
    'workload_percentage_distribution.teaching',
    'workload_percentage_distribution.execution',
    'workload_percentage_distribution.decision',
    'workload_percentage_distribution.other'
]


def get_mean_final_workload(dataframe: pd.DataFrame) -> float:
    return dataframe['final_workload'].mean()


def reports_by_params(reports: pd.DataFrame, param: str, year=None) -> OrderedDict:
    param_count = {}
    reports = filter_column_by_year(reports, 'end_date', year)
    all_report_types = reports[param]
    for types in all_report_types:
        for _type in types:
            if _type in param_count:
                param_count[_type] += 1
            else:
                param_count[_type] = 1
    stx = sorted(param_count.items(), key=lambda kv: kv[1], reverse=True)
    sorted_dict = OrderedDict(stx)
    return sorted_dict


def get_average_work_distribution(dataframe: pd.DataFrame):
    avg_dict = {}
    for category in WORKLOAD_CATEGORY:
        avg_dict[category[33:]] = dataframe[category].mean()
    return avg_dict


def get_work_distribution_for_request_type(dataframe: pd.DataFrame):
    wd = dataframe[[*WORKLOAD_CATEGORY, 'request_types']].copy()
    request_types = wd['request_types'].to_list()
    principal_types = []
    for rt in request_types:
        if rt[0] in TYPE_CATEGORY_SE:
            principal_types.append('SE')
        elif rt[0] in TYPE_CATEGORY_LEGAL:
            principal_types.append('LEGAL')
        else:
            principal_types.append('PRAC')
    wd['Principal_Type'] = principal_types
    rslt_df = wd[wd['Principal_Type'] == 'SE']
    se_avg_dict = get_average_work_distribution(rslt_df)

    rslt_df = wd[wd['Principal_Type'] == 'LEGAL']
    legal_avg_dict = get_average_work_distribution(rslt_df)

    rslt_df = wd[wd['Principal_Type'] == 'PRAC']
    prac_avg_dict = get_average_work_distribution(rslt_df)

    return se_avg_dict, legal_avg_dict, prac_avg_dict


def reports_per_principal_request_type(reports: pd.DataFrame, year=None):
    reports = filter_column_by_year(reports, 'end_date', year)
    principal_types = Counter()
    for index, report in reports.iterrows():
        request_types = report['request_types']
        seen = set()
        for rt in request_types:
            category = 'PRAC'
            if rt in TYPE_CATEGORY_SE:
                category = 'SE'
            elif rt in TYPE_CATEGORY_LEGAL:
                category = 'LEGAL'
            if category not in seen:
                seen.add(category)
                principal_types[category] += 1
    print("No. of tickets per principal request_type")
    print(principal_types)
    print()
    return principal_types


def reports_by_request_type(reports: pd.DataFrame, year=None) -> Counter:
    reports = filter_column_by_year(reports, 'end_date', year)
    counter = Counter()
    for index, report in reports.iterrows():
        for request_type in report['request_types']:
            counter[request_type] += 1
    print("No. of tickets per request_type")
    print(counter)
    print()
    return counter


def request_type_by_affiliation(reports: pd.DataFrame, request_type=None, year=None) -> Counter:
    reports = filter_column_by_year(reports, 'end_date', year)
    reports = reports[['consultants', 'request_types']].copy()
    counter = Counter()
    for index, report in reports.iterrows():
        if request_type in report['request_types']:
            seen = set()
            for person in report['consultants']:
                affiliation = person['affiliation'].upper()
                if affiliation not in seen:
                    counter[affiliation] += 1
                    seen.add(affiliation)

    print(f"Reports worked on per centre for request type '{request_type}'")
    print(counter)
    print()
    return counter


def reports_by_affiliation(reports: pd.DataFrame, role='consultants', year=None) -> Counter:
    reports = filter_column_by_year(reports, 'end_date', year)

    counter = Counter()
    names = defaultdict(set)
    for index, report in reports.iterrows():
        seen = set()
        for person in report[role]:
            name = person['name'].upper()
            affiliation = person['affiliation'].upper()
            if affiliation not in seen:
                counter[affiliation] += 1
                seen.add(affiliation)
            if name not in names:
                names[affiliation].add(name)

    print(f"Reports worked on per centre with role {role}")
    print(counter)
    print(names)
    print()
    return counter


def filter_column_by_year(reports, column, year):
    if year:
        return reports[reports[column].dt.year == year].copy()
    return reports


def opened_reports(reports: pd.DataFrame, year=None) -> pd.DataFrame:
    reports = filter_column_by_year(reports, 'start_date', year)
    opened = reports['zammad_ticket_number'].groupby(
        [
            reports['start_date'].dt.year.rename('year'),
            reports['start_date'].dt.month.rename('month'),
        ]
    ).agg({'count'})

    print("Opened reports")
    print(opened)
    print(opened.sum())
    print()
    return opened


def closed_reports(reports: pd.DataFrame, year=None) -> pd.DataFrame:
    reports = filter_column_by_year(reports, 'end_date', year)
    closed = reports['zammad_ticket_number'].groupby(
        [
            reports['end_date'].dt.year.rename('year'),
            reports['end_date'].dt.month.rename('month'),
        ]
    ).agg({'count'})

    print("Closed reports:")
    print(closed)
    print(closed.sum())
    print()
    return closed


def convert_datatypes(df: pd.DataFrame) -> pd.DataFrame:
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    df['estimated_workload'] = pd.to_numeric(df['estimated_workload'])
    df['final_workload'] = pd.to_numeric(df['final_workload'])
    return df


def read_reports() -> pd.DataFrame:
    """
    Reads the yaml type report files to a pandas DataFrame
    """
    reports = []
    report_path = Path(PATH)

    # Iterates over all files in the path given
    report_files = report_path.glob("*.yml")

    for filename in report_files:
        try:
            with open(filename, 'r', encoding="utf-8") as fh:
                content_dict = yaml.safe_load(fh.read())
            report_df = pd.json_normalize(content_dict)
        except Exception as e:
            print(f"Failed parsing yaml at file {filename}", file=sys.stderr)
            raise e
        else:
            reports.append(report_df)
    reports_df = pd.concat(reports)
    reports_df.reset_index(drop=True, inplace=True)
    reports_df.set_index('zammad_ticket_number')

    return reports_df


def main(args):
    # Read the yaml files to pandas DataFrame
    reports = read_reports()
    # Converts column types to desired types
    reports = convert_datatypes(reports)

    if args.verbose > 0:
        print(f"======= Overall statistics =======")
        print()

        print("Total reports:", len(reports))
        print()

        # All time
        closed_reports(reports)
        opened_reports(reports)

        reports_by_affiliation(reports, 'consultants')
        reports_by_affiliation(reports, 'experts')
        reports_by_affiliation(reports, 'clients')

        reports_per_principal_request_type(reports)

        print("Mean workload per ticket (in days)")
        print(get_mean_final_workload(reports))
        print()

        print("Average workload distribution:")
        average_distribution = get_average_work_distribution(reports)
        average_distribution = pd.DataFrame.from_dict(average_distribution, orient="index")
        average_distribution.rename({0: '%'}, axis='columns', inplace=True)
        print(average_distribution)

    if args.verbose > 1:
        print(f"======= Even more statistics =======")
        print()

        print("No. of tickets per tag category")
        print(reports_by_params(reports, 'tags'))
        print()

        print("No. of tickets per used_technology")
        print(reports_by_params(reports, 'used_technologies'))
        print()

        print("No. of tickets per communication platform")
        print(reports_by_params(reports, 'communication_platforms'))
        print()

        reports_by_request_type(reports)
        print(f"REQUEST TYPES")
        print("=====================================================")
        for request_type in REQUEST_TYPES:
            request_type_by_affiliation(reports, request_type)
        print()

    if args.year:
        print(f"======= Reports for {args.year} =======")
        print()

        # Metrics
        closed_reports(reports, args.year)
        opened_reports(reports, args.year)

        reports_by_affiliation(reports, 'consultants', args.year)
        reports_by_affiliation(reports, 'experts', args.year)
        reports_by_affiliation(reports, 'clients', args.year)

        reports_by_request_type(reports, args.year)
        reports_per_principal_request_type(reports, args.year)
        print(f"REQUEST TYPES")
        print("=====================================================")
        for request_type in REQUEST_TYPES:
            request_type_by_affiliation(reports, request_type, args.year)
        print()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Report evaluation tool',
                                     add_help=False)
    parser.add_argument('--year', type=int,
                        default=datetime.date.today().year,
                        help="The report year. Defaults to the current year")
    parser.add_argument('--verbose', '-v',
                        action='count',
                        default=0,
                        help="Print overall statistics")
    arguments = parser.parse_args()
    main(arguments)
