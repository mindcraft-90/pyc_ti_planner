import streamlit as st

from modules.constants import st_icons, mat_icons
from modules.utilities import download_json_file, upload_json_file


pages = {
    "": [
        st.Page(page="sections/home.py", title="Home")
    ],
    "Planners": [
        st.Page(page="sections/habitat_planner.py", title="Habitat Planner", icon=st_icons["hab"]),
        st.Page(page="sections/ship_designer.py", title="Ship Designer", icon=st_icons["ship"])
    ],
    "Resources": [
        st.Page(page="sections/info_support.py", title="Info & Support", icon=mat_icons["info"])
    ]
}

st.navigation(pages).run()


with st.sidebar:
    st.write("")

    if "habitat" in st.session_state:
        st.download_button(label="**Save Habitat as JSON**", use_container_width=True,
                           file_name="habitat_data.json", mime="application/json",
                           data=download_json_file(st.session_state))

    with st.expander(label="Load Habitat JSON file", icon=mat_icons["upload"], expanded=False):

        with st.form(key="upload_form", border=False, clear_on_submit=True):
            file = st.file_uploader(label="upload_json", label_visibility="collapsed",
                                    type="JSON", accept_multiple_files=False)
            submit = st.form_submit_button(label="Upload JSON", use_container_width=True)

            if file and submit:
                st.session_state.first_run = False
                upload_json_file(file)
                st.switch_page("sections/habitat_planner.py")
            elif submit:
                upload_json_file(None, error=True)

    st.title("")
    with st.expander(label="External links", icon=mat_icons["web"], expanded=True):
        st.page_link(label="Pavonis Interactive",
                     page="https://www.pavonisinteractive.com/",
                     icon=":material/link:",
                     use_container_width=True)

        st.page_link(label="Terra Invicta on Steam",
                     page="https://store.steampowered.com/app/1176470/Terra_Invicta/",
                     icon=":material/link:",
                     use_container_width=True)

        st.page_link(label="Github Repo",
                     page="https://github.com/mindcraft-90/pyc_ti_planner",
                     icon=":material/link:",
                     use_container_width=True)
