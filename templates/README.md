# Template description

A report should be created by the consultant who was involved during the consultation. The report file is expected be in ***.yaml*** or ***.yml*** format and should conform to the linting rules listed in __.yamllint.yml__.
About 20 fields are supposed to be filled by a consultant for the report creation. More details on them below:

1. **zammad_ticket_number**: The numeric ticket number from the HIFIS Helpdesk.
1. **ticket_link**: The consulting ticket URL
1. **project_name**: The consulting ticket title as written by the client.
1. **project_website**: External websites describing the client's project, if any.
1. **client_other_resources**: Directly relevant project material shared to us by the client. For eg. Gitlab repo of the project.
1. **consultant_names**: Name(s) of the HIFIS consultant(s) involved. 
1. **consultant_centers**: Institute(s) of the HIFIS consultant(s) involved, respectively.
1. **expert_names**: Name(s) of the HIFIS/non-HIFIS expert(s) involved.
1. **expert_centers**: Institute(s) of the HIFIS/non-HIFIS expert(s) involved, respectively.
1. **client_names**: Name(s) of the clients involved.
1. **client_centers**: Institute(s) of the client(s) involved, respectively.
1. **used_consultation_roles**: List of roles required by the consulation and covered by an consultant. Remove those not applicable for the consultation.
    1. **Technical domain**: Knowledge about a technical topic, i.e. Testing.
    1. **Tool**: Knowledge about a certain tool, i.e. Gitlab.
    1. **Scientific domain**: Knowledge about the application domain of the software (not IT).
    1. **Organisation**: Knowledge about tools, processes, contact persons, etc. of the organisation.
1. **start_date**: Filing date of the ticket as per ISO 8601 Data elements and interchange formats. _(yyyy-mm--dd)_
1. **end_date**: Date of closure as per ISO 8601 Data elements and interchange formats. _(yyyy-mm--dd)_
1. **survey_sent** Indicates that a survey was sent. Valid values are positive integers and zero. In case it was decided not to sent a survey, the selected value is 0.
1. **estimated_workload**: Estimated workload given in less or equal `days` until the request will be finished.
1. **final_workload**:  Approximated final workload given in less or equal `days` after the request was closed.
1. **workload_percentage_distribution**: Approximated distribution of workflow in percentage.
    1. **communication**: Calls, mail, etc.
    1. **preparation**: Reading up, learning a new tool, etc.
    1. **teaching**: Trainings, presentations, etc.
    1. **execution**: Coding, etc.
    1. **decision**: Thinking
    1. **other**: Unexpected further tasks
1. **internal_consulting_resources**: URL(s) to the consulting resources created as part the consultation.
1. **tags**: Keywords of technology/tools/concepts involved in the consultation.
1. **request_types**: Consulting type(s) as per the consulting handbook.
1. **communication_platforms**: Used means of communication to client other than the HIFIS Helpdesk.
1. **used_technologies**: Technologies/tools used by the consultant to cater the request.
1. **used_consulting_resources**: URL(s) to the existing resources reused for the consultation.
1. **other_identified_problems**: Other issue(s) identified by the consultant in addition to the main consulting request.
1. **remarks**: Free text describing the consulting story.

## Fill-in hints
* **Leave attributes empty if no value** - Use only keys without a following space after the colon to indicate an empty attributes.
* **No empty attribute lists** - Use `[]` to indicate empty attribute lists.  
* **No trailing spaces** - No spaces behind an attribute.
* **No long lines** - Add line breaks. If you do so, ensure you line does not end with a space.
