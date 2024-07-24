import streamlit as st

from modules.utilities import send_email


st.set_page_config(page_title="Terra Invicta Planner", page_icon="ℹ️",
                   layout="centered", initial_sidebar_state="expanded")

st.write("### ℹ️ Info and Support")
st.write("(Or: 'Houston, We Have a Problem')")

st.write("######")
st.write("#### 📋 File a Report")
with st.expander(label="Got a burning question? Aliens stole your homework? Use this form!", icon="✉️"):
    with st.form(key="email_form", clear_on_submit=True):
        user_email = st.text_input("Your Earth email address (or nearest exoplanet equivalent)")
        user = user_email.split("@")[0]
        topic = st.selectbox(label="What's the cosmic issue?",
                             options=["Brilliant Suggestion",
                                      "Pesky Bug",
                                      "Existential Question",
                                      "Other Earthly Concerns"])

        raw_message = st.text_area("Your message (please no alien languages, our translator is on coffee break)")
        message = f"""Subject:[{topic}] Terra Invicta Planner - Transmission from {user}

        Cosmic Topic: {topic}
        From: {user_email}

        {raw_message}
        """

        button = st.form_submit_button("Launch Message into Space")
        if button:
            send_email(message)
            st.success("Message successfully beamed to our orbital station!")


st.write("######")
st.write("#### 🐞 Features in Disguise")
st.write(
    """
    - Mining module power isn't adjusted for solar bodies
    - Habitat airlocks occasionally jam. Have you tried turning it off and on again?
    """
)


st.write("######")
st.write("#### 📜 Release Notes")
with st.expander(label="Version 0.1 - 'The Big Bang'"):
    st.write(
        """
        - Initial release! If the universe can start with a bang, so can we.
        - Habitat planner added. Now you can build space houses without the space mortgage.
        - Implemented JSON save/load feature. Now your space plans can survive a wormhole or two.
        """
    )
