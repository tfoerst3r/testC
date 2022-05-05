# Consulting Reports

This is a sample adaptable repository for storing, managing and analysing consulting reports. The structured reports in
YAML format faciliates easy human and/or machine readability. Along with Python-based scripts, these reports can be 
analysed or evaluated for various data of interest. In a nutshell, the repo provides a base template YAML with 
description, few real-life examples of populated consultation reports, Python script for statistics generation and 
full-fleged Gitlab-CI setup for linting and data validation.

Note that this repository should be used in conjunction with the [HIFIS-Consulting-Handbook](https://goo.gl/maps/3z7H4uHAioN9kE958)


## Repo structure
```
Consulting-Reports
│   README.md
│   requirements-ci.txt    
│   .yamllint.yml
│   .gitlab-ci.yml
│   .gitignore
│   
└───code
│   │   evaluation.py
│   │   requirements.txt
│
│───templates
│       │   README.md
│       │   validate.py
│       │   structured_report_template.yml
│       │   consultation-report.schema.json
│   
└───reports
    │   56131_EarthSystems.yml
    │   56083_BlairWitchProject.yml
    │   56531_Manhattan.yml
```

## YAML Templates

In the `templates` folder you can find a sample template for preparing consulting report. Each consultant is expected to fill in a copy of the template and place in 
`reports` folder. This template can be customized according to the needs of the consulting service. Note that the python
script for further evaluation might also require changes, accordingly.

## Evaluation

A vanilla evaluation script (Python) alongside a requirements.txt can be found in the `code` folder. The script generates
some useful statistics like average workload, no.of consultations of specific type etc.

##### Usage
A report for 2021 can be created with:
```shell
python code/evaluation.py --year 2021
```
You can use ``-v`` multiple times to print verbose output.

We recommend creating a Python (>= 3.9) virtual environment to install all the dependencies listed in `requirements.txt`
before executing the evaluation script.
```shell
git clone <repo_URL/consulting-reports>
cd consulting-reports
pip install -r code/requirements.txt
```

Note: The ``requirements-ci.txt`` file in this repo is to setup up the Python dependencies 
for linting and validation jobs for the Gitlab-CI client.

##  Sample `reports`

The `reports` folder contains a few sample reports from real consulting encounters inside HIFIS. Each sample report in 
the folder is chosen from a different `request_type`. (Refer [HIFIS-Consulting-Handbook](https://goo.gl/maps/3z7H4uHAioN9kE958) for
more information on `request_type`).

Each YAML file is named in `<ticket number>_<project_name>.yml` format, viz.
1. 56131_EarthSystems.yml
1. 56083_BlairWitchProject.yml
1. 56531_Manhattan.yml


## Authors
The HIFIS Consulting Team: (in alphabetical order)
1. Ashis Ravindran, DKFZ Heidelberg
2. Benjamin Wolff, DLR Cologne
3. Martin Stoffers, DLR Cologne
4. Thomas Förster, HZDR Dresden
5. Tobias Huste, HZDR Dresden
