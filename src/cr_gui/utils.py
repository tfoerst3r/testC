#-- Std. modules/libraries
import subprocess

#-------------------#
#-- create_report --#
#-------------------#
def create_html_report():
    """
    Launches web ui to fill in a consultation report
    """

    command = ["streamlit", "run", "./src/cr_gui/ui_create.py"]
    with subprocess.Popen(command) as proc:
        try:
            proc.wait()
        except KeyboardInterrupt:
            print("Kill streamlit")
            proc.terminate()
            proc.wait()
