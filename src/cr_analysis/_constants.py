import datetime

#=======================================#
#== INITALISATION VALUES AND CONTANTS ==#
#=======================================#
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

WORKLOAD_CATEGORY = [
    'workload_percentage_distribution.communication',
    'workload_percentage_distribution.preparation',
    'workload_percentage_distribution.teaching',
    'workload_percentage_distribution.execution',
    'workload_percentage_distribution.decision',
    'workload_percentage_distribution.other'
]

REQUEST_MAIN_TYPES = {'SE': TYPE_CATEGORY_SE, 'LEGAL': TYPE_CATEGORY_LEGAL, 'PRAC': TYPE_CATEGORY_PRAC}
current_year = int(datetime.date.today().strftime("%Y"))
current_date = datetime.datetime.now().strftime("%Y-%m-%d")

month_names = {
    1: 'Jan',
    2: 'Feb',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'Aug',
    9: 'Sept',
    10: 'Oct',
    11: 'Nov',
    12: 'Dec'
}
