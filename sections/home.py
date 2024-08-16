import os
import streamlit as st

from streamlit_extras.let_it_rain import rain
from PIL import Image

from modules.habitat_stats import get_base64_image


icon_path = "_resources/icons/title.png" \
    if os.path.exists("_resources/icons/title.png") else "data/misc/missing_icon.png"
icon = get_base64_image(stat="title" if "icons" in icon_path else "missing_icon",
                        path="_resources/icons" if "icons" in icon_path else "data/misc", height=40)

st.set_page_config(page_title="Terra Invicta Planner", page_icon=Image.open(icon_path), layout="centered")

st.write(f"### {icon} Terra Invicta Planner", unsafe_allow_html=True)
st.write("######")
st.write(
    """
    ##### Welcome, Earth's last hope! 👽🛸

    You've stumbled upon the **Terra Invicta Planner**, a tool crafted by a rookie programmer 
    with more enthusiasm than sleep. This is your one-stop shop for all your 
    alien-resistance planning needs!

    Whether you're a seasoned councilor or a fresh recruit, this planner is here to help you:
    - 🏗️ Design habitats that would make the aliens green(er) with envy
    - 🚀 Plan your space ship adventures without accidentally colonizing Uranus
    - 📄 Manage your habitats and ship designs with JSON files, like a retro admin with a filing cabinet

    Remember, in space, no one can hear you miscalculate!
    """
)

st.write("######")
st.info("Navigate through the sidebar faster than a UFO dodging Air Force jets! 🛸💨", icon="ℹ️")

st.write("######")
st.write(
    """
    **Disclaimer:** This planner is a fan-made tool for Terra Invicta. It's about as official as 
    your uncle's "authentic" alien abduction story.

    For the real deal, blast off to [Pavonis Interactive](https://www.pavonisinteractive.com/). 
    They're the masterminds behind this galactic chess game we're all addicted to.

    Now, go forth and save humanity! (No pressure or anything...)
    """
)

st.write("######")
st.caption(
    """
    **Humor Disclaimer:** The developer of this tool would like to confess that they're not 
    actually this funny in real life. The witty comments and space puns were crafted with the 
    help of an AI assistant. Any groans, eye-rolls, or spontaneous chuckles are the result of 
    a human-AI comedy collaboration. The developer's actual sense of humor is more... down to Earth.
    """
)


# Easter Egg
def invasion():
    rain(emoji="🛸", font_size=54, falling_speed=5, animation_length="infinite",)


st.write("#")
if st.button("❗ Don't Press This Button"):
    invasion()
    st.write("Oops! You've just alerted the aliens to our secret planning tool. Quick, act natural! 🕴️")
