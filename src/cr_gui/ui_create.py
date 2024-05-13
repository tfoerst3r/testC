#-- Std. modules/libraries
import textwrap
from pathlib import Path

#-- External modules libraries
import streamlit as st
from streamlit_tags import st_tags
import yaml

#-- Internal modules libraries
from cr_gui.constants import (
    consultant_centers,
    consultation_roles,
    consulting_types,
    available_communication_platforms
)

def input_people_info(title: str, count: int):
    people = []
    if count > 0:
        st.subheader(title)
        for i in range(count):
            with st.expander(f"{title[:-1]} {i + 1}"):
                name = st.text_input(f"{title[:-1]} {i + 1} Name")
                affiliation = st.selectbox(
                    f"{title[:-1]} {i + 1} Affiliation", consultant_centers
                )
                # affiliation here will only be the abbreviation of the center. Which is before the first comma
                # See "ui_data.py"
                people.append(
                    {"name": name, "affiliation": affiliation.split(",", 1)[0]}
                )
    return people


def main():
    # === Create a dictionary to store all inputs ===#
    data = {}
    st.title("HIFIS Consulting Form")

    # === Ticket Details === #
    st.subheader("Ticket Details")
    zammad_ticket_number = st.number_input(
        "Zammad Ticket Number (required)",
        min_value=561000,
        value=562222,
        help="The numeric ticket number from the HIFIS Helpdesk.",
    )

    ticket_link = st.text_input(
        label="Ticket Link (required)",
        value="https://support.hifis.net/#ticket/zoom/1111",
        help="The consulting ticket URL",
    )
    project_name = st.text_input(
        label="Project Name (required)",
        help="The consulting ticket title as written by the client.",
    )
    project_website = st.text_input(
        label="Project Website (optional)",
        help="External websites describing the client's project, if any.",
    )
    # ====================== #

    # === Consultants === #
    st.subheader("Consultants")
    consultant_count = st.number_input("Number of Consultants", min_value=1, step=1)
    consultants = input_people_info("Consultants", consultant_count)
    # =================== #

    # === Experts === #
    st.subheader("Experts")
    expert_count = st.number_input("Number of Experts", min_value=0, step=1)
    experts = input_people_info("Experts", expert_count)
    # =============== #

    # === Clients === #
    st.subheader("Clients")
    client_count = st.number_input(
        "Number of Clients", min_value=1, max_value=10, step=1
    )
    clients = input_people_info("Clients", client_count)

    # === Consultation Roles === #
    st.subheader("Consultation Roles")
    used_consultation_roles = st.multiselect(
        "Consultant Roles (optional)",
        consultation_roles,
        help="List of roles required by the consultation and covered by an consultant.",
    )
    # ========================== #

    # === Dates ===#
    st.subheader("Dates")
    start_date = st.date_input(
        "Start Date (required)",
        format="YYYY-MM-DD",
        help="Filing date of the ticket as per ISO 8601 Data elements and interchange formats. (YYYY-MM-DD)",
    )
    end_date = st.date_input(
        "End Date (required)",
        format="YYYY-MM-DD",
        help="Date of closure as per ISO 8601 Data elements and interchange formats. (YYYY-MM-DD)",
    )

    survey_sent = st.number_input(
        label="Number of Sent Survey (required)",
        min_value=0,
        help="Indicates the number of sent out surveys. Valid are positive integers and zero. "
        "Zero indicates, that a survey was not sent.",
    )
    # =============#

    # === Workload === #
    st.subheader("Workload")

    estimated_workload = st.number_input(
        label="Estimated Workload (required)",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help="Estimated workload given in less or equal days until the request will be finished.",
    )
    final_workload = st.number_input(
        label="Final Workload (required)",
        min_value=0.0,
        format="%.1f",
        step=0.1,
        help=" Approximated final workload given in less or equal days after the request was closed.",
    )
    # ================ #

    # === Workload Distribution (required) ===#
    st.subheader("Workload Percentage Distribution (required)")
    st.caption("Approximated distribution of workflow in percentage.")

    # .. communication slider
    communication = st.slider(
        "Communication (%)",
        min_value=0,
        max_value=100,
        step=5,
        help="Calls, mail, etc.",
    )

    # .. preparation slider
    preparation = st.slider(
        "Preparation (%)",
        min_value=0,
        max_value=100,
        step=5,
        help="Reading up, learning a new tool, etc.",
    )

    # .. teaching slider
    teaching = st.slider(
        "Teaching (%)",
        min_value=0,
        max_value=100,
        step=5,
        help="Trainings, presentations, etc.",
    )

    # .. execution slider
    execution = st.slider(
        "Execution (%)", min_value=0, max_value=100, step=5, help="Coding, etc."
    )

    # .. descision slider
    decision = st.slider(
        "Decision (%)", min_value=0, max_value=100, step=5, help="Thinking"
    )

    # .. descision slider
    other = st.slider(
        "Other (%)", min_value=0, max_value=100, step=5, help="Unexpected further tasks"
    )

    total = communication + preparation + teaching + execution + decision + other
    if total > 100:
        st.error(
            f"The total percentage is {total}%."
            f"Please adjust the values so that the total does not exceed 100%."
        )
    # ======================================== #

    # Tags
    st.markdown(
        "<style> .stMarkdown { font-size: 14px; margin-bottom: -2.0rem; } "
        "label { display: flex; flex-direction: row; justify-content:flex-end; flex: 1 1 0%; } "
        "p { font-size: 14px; } </style>",
        unsafe_allow_html=True,
    )
    # ".st-emotion-cache-1whk732 { display: flex; flex-direction: row; justify-content:flex-end; flex: 1 1 0%; } "

    tags = st_tags(
        label="Keywords of technology/tools/concepts involved in the consultation.",
        text="Press enter to submit tag",
        maxtags=20,
        key="tags",
    )

    # Request Types
    request_types = st.multiselect(
        "Request Types",
        consulting_types,
        help="Consulting type(s) as per "
        "[the consulting handbook](https://hifis.net/consulting-handbook/consulting_guide/#consulting-types).",
    )

    # === Communication Platforms === #
    communication_platforms = st.multiselect(
        "Communication Platforms",
        available_communication_platforms,
        help="Used means of communication to client other than the HIFIS Helpdesk.",
    )

    # === Optional Fields === #

    # ---
    st.markdown(
        "Client Other Resources (optional)",
        help="URL(s) to the consulting resources created as part the consultation.",
    )
    client_other_resources = st_tags(
        label="",
        text="Press enter to submit tag",
        key="client_other_resources",
    )

    # ---
    st.markdown(
        "Internal Consulting Resources (optional)",
        help="URL(s) to the consulting resources created as part the consultation.",
    )
    internal_consulting_resources = st_tags(
        label="",
        text="Press enter to submit tag",
        key="internal_consulting_resources",
    )

    # ---
    st.markdown(
        "Used Technologies (optional)",
        help="Technologies/tools used by the consultant to cater the request.",
    )
    used_technologies = st_tags(
        label="",
        text="Press enter to submit tag",
        key="used_technologies",
    )

    # ---
    st.markdown(
        "Used Consulting Resources (optional)",
        help="URL(s) to the existing resources reused for the consultation.",
    )
    used_consulting_resources = st_tags(
        label="",
        text="URL of an existing reused resource.",
        key="used_consulting_resources",
    )

    # ---
    st.markdown(
        "Other Identified Problems (optional)",
        help="Other issue(s) identified by the consultant in addition to the main consulting request.",
    )
    other_identified_problems = st_tags(
        label="",
        text="Press enter to submit tag",
        key="other_identified_problems",
    )

    remarks = st.text_area(
        "Remarks (optional)", help="Free text describing the consulting story."
    )

    filename = st.text_input(
        label="Name of yaml report file (change if needed)",
        value=f"{zammad_ticket_number}_{project_name.replace(' ','-')}.yml",
    )

    # Gather inputs
    data["zammad_ticket_number"] = zammad_ticket_number
    data["ticket_link"] = ticket_link
    data["project_name"] = project_name
    data["project_website"] = project_website

    data["consultants"] = consultants
    data["experts"] = experts
    data["clients"] = clients

    data["start_date"] = start_date
    data["end_date"] = end_date
    data["survey_sent"] = survey_sent

    data["estimated_workload"] = estimated_workload
    data["final_workload"] = final_workload

    data["workload_percentage_distribution"] = {
        "communication": communication,
        "preparation": preparation,
        "teaching": teaching,
        "execution": execution,
        "decision": decision,
        "other": other,
    }

    data["tags"] = tags
    data["request_types"] = request_types
    data["communication_platforms"] = communication_platforms

    data["client_other_resources"] = client_other_resources
    data["internal_consulting_resources"] = internal_consulting_resources
    data["used_technologies"] = used_technologies
    data["used_consulting_resources"] = used_consulting_resources
    data["other_identified_problems"] = other_identified_problems
    data["remarks"] = remarks

    if st.button("Submit"):
        report_file = Path(f"./reports/{filename}")
        if report_file.exists():
            st.toast(f"{str(report_file)} already existent! Please check!")
        else:
            st.write("Report submitted!")
            st.write(data)  # Display the collected data

            # Add a custom representer for strings to the YAML dumper.
            # If the string length exceeds 60 characters, it will:
            # 1. Wrap the string at 60 characters per line.
            # 2. Use the block-style indicator `|` to preserve newlines in the output.
            # If the string is 60 characters or fewer, it will be represented as is.
            yaml.add_representer(
                str,
                lambda dumper, input_data: dumper.represent_scalar(
                    "tag:yaml.org,2002:str",
                    textwrap.fill(input_data, width=60)
                    if len(input_data) > 60
                    else input_data,
                    style="|" if len(input_data) > 60 else None,
                ),
            )

            # Save data to YAML
            with open(f"./reports/{filename}", "w", encoding="utf-8") as file:
                yaml.dump(data, file, sort_keys=False, allow_unicode=True)

            st.write(f"Data saved to {filename}!")


if __name__ == "__main__":
    main()
