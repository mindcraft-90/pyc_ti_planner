import os
import streamlit as st

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

    The **Terra Invicta Planner** is a fan-made tool to help you plan habitats and ships
    without the existential dread of doing it in-game.

    - 🏗️ Design habitats and see their stats in real time
    - 🚀 Plan ship loadouts before committing to the build queue
    - 📄 Save and load your designs as JSON files

    Navigate using the sidebar. Try not to lose Earth while you're in here.
    """
)

st.write("######")
st.write(
    """
    For the real deal, visit [Pavonis Interactive](https://www.pavonisinteractive.com/).
    """
)
