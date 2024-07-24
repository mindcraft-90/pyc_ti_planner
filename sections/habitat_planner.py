import json
import streamlit as st
from typing import Any, Dict, List

from modules.clickable_image import clickable_image
from modules.constants import habitat_layouts, solar_modifiers, ui_layouts
from modules.habitat_stats import display_habitat_stats
from modules.habitat_module import module_image, module_tooltip


st.set_page_config(page_title="Terra Invicta Planner", page_icon="🛰️",
                   layout="wide", initial_sidebar_state="expanded")

ModuleData = Dict[str, Any]
st_state = st.session_state


def get_raw_module_data() -> Dict[str, ModuleData]:
    """
    Import raw module data and filter out undesired modules.
    Returns a dictionary of module data.
    """
    excluded_module_types: List[str] = ["alienModule", "destroyed", "automated"]

    with open("data/TIHabModuleTemplate.json", "r") as file:
        return {d["dataName"]: d for d in json.load(file)
                if not any(d.get(k, False) for k in excluded_module_types)}


def filter_modules(core: ModuleData, tier_filters: List[str]) -> Dict[str, ModuleData]:
    """
    Filter out modules based on core tier and user choice.
    Returns a dictionary of filtered modules.
    """
    if not tier_filters or "All Modules" in tier_filters:
        tiers = range(1, core["tier"] + 1)
    else:
        tiers = {int(f.split()[-1]) for f in tier_filters if f.startswith("Tier")}

    return {k: v for k, v in all_modules.items()
            if (v["habType"] in (core["habType"], "Any")
                and v["tier"] in tiers
                and not v.get("coreModule", False))
            }


def generate_habitat_layout(core: ModuleData) -> None:
    """
    Generate the visual layout of the habitat based on the core module.c
    """
    habitat_layout = habitat_layouts[core["habType"]][core["tier"]]

    for row_idx, row in enumerate(habitat_layout):
        if row_idx == 0 and core["habType"] == "Base":
            cell_module = st_state.habitat["cells"].get("0_3", [3, None])[-1]
            is_mining_module = isinstance(cell_module, str) and "Mining" in cell_module

            cols = st.columns([1, 0.25, 0.25, 4, 0.25, 0.25, 1], gap="small") \
                if is_mining_module else st.columns(len(row), gap="small")
        else:
            cols = st.columns(len(row), gap="small")

        for col_idx, col in ((i, c) for i, c in enumerate(cols) if row[i] != 0):
            with col:
                label = f"{row_idx}_{col_idx}"
                if label not in st_state.habitat["cells"]:
                    st_state.habitat["cells"][label] = [row[col_idx], None]
                clickable_image(key=label, use_column_width="always",
                                source=module_image(core, label, st_state, all_modules),
                                tooltip=module_tooltip(core, label, st_state, all_modules))


row_prefix = ("0_", "1_", "2_", "3_", "4_", "5_", "6_")
click_timestamps = {k: v for k, v in st_state.items() if k.startswith(row_prefix) and v}
st_state.clicked_cell = max(click_timestamps, key=click_timestamps.get) if click_timestamps else None

if st_state.clicked_cell and st_state.module_choice:
    st_state.habitat["cells"][st_state.clicked_cell][-1] = st_state.module_choice
    st_state.module_choice = None
    st_state.clicked_cell = None

col_stats, col_habitat, empty = st.columns(ui_layouts["hab_main"], gap="small")


with col_habitat:
    sub_layout = ui_layouts["hab_sub"]
    col_core_choice, col_habitat_type, col_solar_body \
        = st.columns(sub_layout, gap="small")
    col_module_filters, col_module_select \
        = st.columns([sub_layout[0], sub_layout[1] + sub_layout[2]], gap="small")

    habitat_type: str = col_habitat_type.radio(
        label="Habitat Type",
        options=("station", "base"),
        format_func=str.title,
        index=("station", "base").index(st_state.get("habitat", {}).get("type", "station")))

    solar_body: str = col_solar_body.selectbox(
        label="System Body",
        options=list(solar_modifiers.keys()),
        index=list(solar_modifiers.keys()).index(
            st_state.get("habitat", {}).get("body", list(solar_modifiers.keys())[0])))

    all_modules: Dict[str, ModuleData] = get_raw_module_data()
    cores: Dict[str, ModuleData] = {k: v for k, v in all_modules.items()
                                    if v["coreModule"] and v["habType"] == habitat_type.title()}

    core_choice = col_core_choice.selectbox(
        label="Select a habitat core:",
        options=list(cores.keys()),
        format_func=lambda x: f"Tier {cores[x]['tier']} - {cores[x]['friendlyName']}",
        index=list(cores.keys()).index(st_state.get("habitat", {}).get("core"))
        if st_state.get("habitat", {}).get("core") in cores else 0,
        placeholder="Select a habitat core...")

    if not core_choice:
        st.stop()

    active_core = cores[core_choice]

    # Loading a JSON file before opening the Habitat Planner causes an error, when selecting a module
    # Error: "module_choice" is not initialized in st_session_state
    # Placeholder fix for now
    if "module_choice" not in st_state:
        st_state.module_choice = None

    # 🤷 shrug off habitat tier and type changes...
    if "first_run" not in st_state \
            or active_core["tier"] != st_state.habitat["tier"]\
            or habitat_type.lower() != st_state.habitat["type"]:
        st_state.habitat = {"cells": {}}
        st_state.clicked_cell = None
        st_state.module_choice = None
        st_state.first_run = False
    st_state.habitat["core"] = active_core["dataName"]
    st_state.habitat["tier"] = active_core["tier"]
    st_state.habitat["type"] = habitat_type.lower()
    st_state.habitat["body"] = solar_body

    generate_habitat_layout(active_core)

    with col_module_filters:
        available_tiers: List[str] = [f"Tier {i}" for i in range(1, active_core["tier"] + 1)]
        active_filters: List[str] = st.multiselect(
            label="user_filters",
            label_visibility="collapsed",
            placeholder="Filter modules...",
            options=(["All Modules"] + available_tiers))

    with col_module_select:
        if st_state.clicked_cell and st_state.habitat["cells"][st_state.clicked_cell][0] != 2:
            available_modules = filter_modules(active_core, active_filters)

            cell_key = st_state.clicked_cell
            st.selectbox(
                label=f"Select a new module for cell {cell_key}:",
                label_visibility="collapsed",
                options=available_modules,
                format_func=lambda x: available_modules[x]["friendlyName"],
                placeholder=f"Editing: {module_tooltip(active_core, cell_key, st_state, all_modules)}",
                key="module_choice")

    with col_stats:
        display_habitat_stats(st_state.habitat, all_modules)
