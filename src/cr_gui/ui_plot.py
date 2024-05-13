"""
Generates a software engineering consulting report based on YAML files in the specified `reports_dir` directory.
The report consists of several plots, which visualize different aspects of the data, such as the number
of reports per category, the number of reports per technology used, and the average workload distribution.
The generated report is saved as an HTML file with the specified `destination` path.

Args:
    destination (Path, optional): The destination path for the generated HTML report. Defaults to 'reports.html'
    reports (Path, optional): The directory containing YAML files with the necessary data to generate the report. Defaults to 'reports/'

Note:
    - Ensure that the specified `reports_dir` exists and contains YAML files with the necessary data.
"""

#: Std. modules, libraries
from pathlib import Path

#: External modules, libraries
import plotly.express as px
import plotly.offline as pyo

#: Internal modules, libraries
from cr_analysis._utils import (
    loading_data,
    counting_affiliations,
    counting_occurrence,
    counting_main_types,
    workload_distribution,
    tickets_per_month
)
from cr_analysis._constants import current_year

#------------------#
#-- plot reports --#
#------------------#

def plot_html_analysis(
    destination: Path = Path('reports.html'),
    reports: Path = Path('reports/'),
    year: int = current_year,
    center: str = 'all'
) -> None:
    """Creates the plotly output for HTML"""
    #---- Program routine ----------------------------#
    df = loading_data(reports=reports, year=year, center=center)

    tickets = len(df)
    workload_mean=round(df['final_workload'].mean(),2)
    workload_median=round(df['final_workload'].median(),2)

    if center == 'all':

        #== PLOT 1: Affiliation counts of consultants ==#
        myinput = "consultants"

        data = counting_affiliations(
                dataframe=df,
                column=myinput,
                output='relative'
            )

        #-- Create DataFrame with two columns 'index' and 'count'
        data = data.to_frame().reset_index()

        plot1 = px.pie(
            data,
            names='index',
            values='count'
        )

        plot1.update_layout(
            title=f"Rel. number of affiliations ({myinput})",
            hovermode='closest'
        )

        plot1_div = pyo.plot(plot1, output_type="div", include_plotlyjs=False)

        #== PLOT 2: Affiliation counts of experts ==#
        myinput = "experts"

        data = counting_affiliations(
                dataframe=df,
                column=myinput,
                output='relative'
        )

        #-- Create DataFrame with two columns 'index' and 'count'
        data = data.to_frame().reset_index()

        plot2 = px.pie(
            data,
            names='index',
            values='count'
        )

        plot2.update_layout(
            title=f"Rel. number of affiliations ({myinput})",
            hovermode='closest'
        )

        plot2_div = pyo.plot(
            plot2,
            output_type="div",
            include_plotlyjs=False
        )

        #== PLOT 3: Affiliation counts of overall (experts and consultants) ==#
        myinput1 = "consultants"
        myinput2 = "experts"

        data = counting_affiliations(
                dataframe=df,
                column=myinput1,
                add=myinput2,
                output='relative'
        )

        #-- Create DataFrame with two columns 'index' and 'count'
        data = data.to_frame().reset_index()

        plot3 = px.pie(
            data,
            names='index',
            values='count'
        )

        plot3.update_layout(
            title=f"Rel. number of affiliations ({myinput})",
            hovermode='closest'
        )

        plot3_div = pyo.plot(
            plot3,
            output_type="div",
            include_plotlyjs=False
        )

    else:
        plot1_div = ""
        plot2_div = ""
        plot3_div = ""

    #== PLOT 4: Request Types ==#
    data = counting_occurrence(
            dataframe=df,
            column="request_types",
            output='relative'
        )

    #-- DataFrame with two columns 'index' and 'count'
    data = data.to_frame().reset_index()

    plot4 = px.pie(
        data,
        names='index',
        values='count'
    )

    plot4.update_layout(
        title="Request Types",
        hovermode='closest'
    )

    plot4_div = pyo.plot(
        plot4,
        output_type="div",
        include_plotlyjs=False
    )

    #== PLOT 5: Main Request Types ==#
    data = counting_main_types(
            dataframe=df,
            output='relative'
    )
    #-- DataFrame with two columns 'index' and 'count'
    data = data.to_frame().reset_index()

    plot5 = px.pie(
        data,
        names='index',
        values='count'
    )

    plot5.update_layout(
        title="Rel. number of main request types",
        hovermode='closest'
    )

    plot5_div = pyo.plot(
        plot5,
        output_type="div",
        include_plotlyjs=False
    )

    #== PLOT 6: Average workload ==#
    data = workload_distribution(df=df)

    plot6 = px.pie(
        data,
        names='category',
        values='percentage'
    )

    plot6.update_layout(
        title="Average workload",
        hovermode='closest'
    )

    plot6_div = pyo.plot(
        plot6,
        output_type="div",
        include_plotlyjs=False
    )

    #== PLOT 7: Ticket request distribution per month ==#
    plot7 = px.bar(tickets_per_month(dataframe=df))

    plot7.update_layout(
        title="",
        xaxis_title=f"Year {year}",
        yaxis_title="Ticket request per month",
        showlegend=False,
        yaxis={'tickformat': ',d'}
    )

    plot7_div = pyo.plot(
        plot7,
        output_type="div",
        include_plotlyjs=False
    )


    #== Create the HTML output ==#
    html_report = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Report</title>
        <link href="https://fonts.googleapis.com/css?family=Roboto:300,400&display=swap" rel="stylesheet">
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    </head>
    <body>
        <header>
            <img src="https://hifis.net/assets/img/HIFIS_Logo_short_RGB_cropped.svg" alt="HIFIS Logo" width="20%">
            <h1 style="text-align: center">Software Engineering Consulting Report from <mark>{year}</mark> for <mark>{center}</mark></h1>
        </header>
        <div class="plot-container">
        
            <div class="row" style="display: flex; text-align: center">
                <div class="column" style="flex:33%">
                    <h2>Number of tickets</h2>
                    <p style="font-size:48px;">{tickets}</p>
                </div>
                <div class="column" style="flex:33%">
                    <h2>Average workload</h2>
                    <p style="font-size:48px;">{workload_mean} days</p>
                </div>
                <div class="column" style="flex:33%">
                    <h2>Median workload</h2>
                    <p style="font-size:48px;">{workload_median} days</p>
                </div>
            </div>
            
            <p style="margin-top: 2rem;"/>
            {plot1_div}
            <p style="margin-top: 2rem;"/>
            {plot2_div}
            <p style="margin-top: 2rem;"/>
            {plot3_div}
            <p style="margin-top: 2rem;"/>
            {plot4_div}
            <p style="margin-top: 2rem;"/>
            {plot5_div}
            <p style="margin-top: 2rem;"/>
            {plot6_div}
            <p style="margin-top: 2rem;"/>
            {plot7_div}
        </div>
    <footer>
        <p></p>
    </footer>
    </body>
    </html>
    """

    with open(destination, "w", encoding='utf-8') as f:
        f.write(html_report)

    print(f"Report written to {destination.absolute()}")
