import json
import streamlit as st

from modules.clickable_image import clickable_image
from modules.constants import ModuleData, habitat_layouts, solar_modifiers, ui_layouts, pretty_stats
from modules.habitat_stats import display_habitat_stats, get_base64_image
from modules.habitat_module import module_image, module_tooltip

state = st.session_state

st.set_page_config(page_title="Terra Invicta Planner", page_icon="🛰️",
                   layout="wide", initial_sidebar_state="expanded")


@st.cache_resource
def get_raw_module_data() -> dict[str, ModuleData]:
    """
    Import raw module data and filter out undesired modules.
    Returns a dictionary of module data.
    """
    excluded_module_types: list[str] = ["alienModule", "destroyed", "automated"]

    with open("data/TIHabModuleTemplate.json", "r") as file:
        return {d["dataName"]: d for d in json.load(file)
                if not any(d.get(k, False) for k in excluded_module_types)}


def filter_modules(core: ModuleData, tier_filters: list[str], mining_cell=False) -> dict[str, ModuleData]:
    """
    Filter out modules based on core tier and user choice.
    Returns a dictionary of filtered modules.
    """
    income_filters = [pretty_stats[f] for f in tier_filters if not f.startswith("Tier")]
    tier_filters = [f for f in tier_filters if f.startswith("Tier")]
    if not tier_filters or "All Modules" in tier_filters:
        tiers = range(1, core["tier"] + 1)
    else:
        tiers = {int(f.split()[-1]) for f in tier_filters if f.startswith("Tier")}

    mods = {k: v for k, v in all_modules.items()
            if (v["habType"] in (core["habType"], "Any")
                and v["tier"] in tiers
                and not v.get("coreModule", False))
            }

    if income_filters:
        mods = {k: v for k, v in mods.items() if any(v[income] > 0 for income in income_filters)}
    return {k: v for k, v in mods.items() if v.get("mine", False)} if mining_cell else mods


def generate_habitat_layout(core: ModuleData) -> None:
    """
    Generate the visual layout of the habitat based on the core module.c
    """
    habitat_layout = habitat_layouts[core["habType"]][core["tier"]]

    for row_idx, row in enumerate(habitat_layout):
        if row_idx == 0 and core["habType"] == "Base":
            cell_module = state.habitat["cells"].get("0_3", [3, None])[-1]
            is_mining_module = isinstance(cell_module, str) and "Mining" in cell_module

            cols = st.columns([1, 0.25, 0.25, 4, 0.25, 0.25, 1]) \
                if is_mining_module else st.columns(len(row))
        else:
            cols = st.columns(len(row))

        for col_idx, col in ((i, c) for i, c in enumerate(cols) if row[i] != 0):
            with col:
                label = f"{row_idx}_{col_idx}"
                if label not in state.habitat["cells"]:
                    state.habitat["cells"][label] = [row[col_idx], None]
                clickable_image(key=label, use_column_width="always",
                                source=module_image(core, label, state, all_modules),
                                tooltip=module_tooltip(label, state, all_modules))


row_prefix = ("0_", "1_", "2_", "3_", "4_", "5_", "6_")
click_timestamps = {k: v for k, v in state.items() if k.startswith(row_prefix) and v}
state.clicked_cell = max(click_timestamps, key=click_timestamps.get) if click_timestamps else None

if state.clicked_cell and state.module_choice:
    state.habitat["cells"][state.clicked_cell][-1] = state.module_choice
    state.module_choice = None
    state.clicked_cell = None


col_stats, col_habitat, empty = st.columns(ui_layouts["hab_main"], vertical_alignment="top")
with col_habitat:
    sub_layout = ui_layouts["hab_sub"]
    col_core_choice, col_habitat_type, col_solar_body \
        = st.columns(sub_layout, vertical_alignment="center")
    col_module_filters, col_module_select \
        = st.columns([sub_layout[0], sub_layout[1] + sub_layout[2]], vertical_alignment="center")

    habitat_type: str = col_habitat_type.radio(
        label="Habitat Type",
        options=("station", "base"),
        format_func=str.title,
        index=("station", "base").index(state.get("habitat", {}).get("type", "station")))

    solar_body: str = col_solar_body.selectbox(
        label="System Body",
        options=list(solar_modifiers.keys()),
        index=list(solar_modifiers.keys()).index(
            state.get("habitat", {}).get("body", list(solar_modifiers.keys())[0])))

    all_modules: dict[str, ModuleData] = get_raw_module_data()
    cores: dict[str, ModuleData] = {k: v for k, v in all_modules.items()
                                    if v["coreModule"] and v["habType"] == habitat_type.title()}

    core_choice = col_core_choice.selectbox(
        label="Select a habitat core:",
        options=list(cores.keys()),
        format_func=lambda x: f"Tier {cores[x]['tier']} - {cores[x]['friendlyName']}",
        index=list(cores.keys()).index(state.get("habitat", {}).get("core"))
        if state.get("habitat", {}).get("core") in cores else None,
        placeholder="Select a habitat core...")

    if not core_choice:
        st.stop()

    active_core = cores[core_choice]

    # Loading a JSON file before opening the Habitat Planner causes an error, when selecting a module
    # Error: "module_choice" is not initialized in st_session_state
    # Placeholder fix for now
    if "module_choice" not in state:
        state.module_choice = None

    # 🤷 shrug off habitat tier and type changes...
    if "first_run" not in state \
            or active_core["tier"] != state.habitat["tier"] \
            or habitat_type.lower() != state.habitat["type"]:
        state.habitat = {"cells": {}}
        state.clicked_cell = None
        state.module_choice = None
        state.first_run = False
    state.habitat["core"] = active_core["dataName"]
    state.habitat["tier"] = active_core["tier"]
    state.habitat["type"] = habitat_type.lower()
    state.habitat["body"] = solar_body

    generate_habitat_layout(active_core)

    with col_module_filters:
        available_tiers: list[str] = [f"Tier {i}" for i in range(1, active_core["tier"] + 1)]
        stat_incomes: list[str] = list(pretty_stats.keys())
        active_filters: list[str] = st.multiselect(
            label="user_filters",
            label_visibility="collapsed",
            placeholder="Filter modules...",
            options=(["All Modules"] + available_tiers + stat_incomes))

    with col_module_select:
        if state.clicked_cell and state.habitat["cells"][state.clicked_cell][0] != 2:
            is_mining_cell = state.habitat["cells"][state.clicked_cell][0] == 3
            available_modules = filter_modules(active_core, active_filters, is_mining_cell)

            cell_key = state.clicked_cell
            st.selectbox(
                label=f"Select a new module for cell {cell_key}:",
                label_visibility="collapsed",
                options=available_modules,
                format_func=lambda x: available_modules[x]["friendlyName"],
                placeholder=f"Editing: {module_tooltip(cell_key, state, all_modules)}",
                key="module_choice")


with col_stats:
    st.text_input(label="Habitat name:", label_visibility="visible", placeholder="Habitat name...", max_chars=40,
                  key="hab_name",
                  value=state.get("habitat", {}).get("name", ""),
                  on_change=lambda: state.setdefault("habitat", {}).update({"name": state.hab_name}))

    if state.habitat["type"] == "base":
        with st.popover(label="Base Site Resources", use_container_width=True):
            num_input_kwargs = {"label_visibility": "collapsed", "min_value": 0.00, "step": 1.00}

            for res in ["water", "volatiles", "metals", "nobleMetals", "fissiles"]:
                popover_col1, popover_col2 = st.columns([0.5, 5])
                with popover_col1:
                    st.write(get_base64_image(res), unsafe_allow_html=True)
                with popover_col2:
                    st.number_input(label=res, key=f"site_{res}", **num_input_kwargs,
                                    value=state.get("habitat", {}).get("site", {}).get(res, 0.00),
                                    on_change=lambda r=res: state.setdefault("habitat", {}).setdefault(
                                        "site", {}).update({r: state[f"site_{r}"]}))

    display_habitat_stats(state.habitat, all_modules)
