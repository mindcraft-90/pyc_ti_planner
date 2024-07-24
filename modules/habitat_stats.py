import base64
import streamlit as st
from typing import Dict, Any

from modules import constants as c


def get_default_stats() -> Dict[str, Any]:
    """
    Retrieve a blank set of desired habitat stats.
    """
    return {
        "crew": 0,
        "power": 0,
        "incomeMoney_month": 0,
        "incomeInfluence_month": 0,
        "incomeOps_month": 0,
        "incomeResearch_month": 0,
        "incomeProjects": 0,
        "missionControl": 0,
        "spaceCombatValue": 0,
        "incomeAntimatter_month": 0,
        "allowsShipConstruction": False,
        "allowsResupply": False,
        "CanFoundHabs": False,
        "supportMaterials_month": {},
        "techBonuses": {},
        "leoBonuses": {},
    }


def format_number(value: float) -> str:
    """
    Format float numbers to 3 decimals and strip trailing '0's and '.'s.
    """
    return f"{value:.3f}".rstrip('0').rstrip('.')


def get_base64_image(stat: str, path="_resources/icons", width=20, height=20) -> str:
    """
    Create an icon image to display inline with text.
    """
    try:
        with open(f"{path}/{stat}.png", "rb") as f:
            encoded_data = base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        # with open(f"data/misc/missing_icon.png", "rb") as f:
        #     encoded_data = base64.b64encode(f.read()).decode()
        return stat
    return f"<img src='data: image/png; base64, {encoded_data}' style='width: {width}px; height: {height}px; '>"


def update_habitat_stats(module: Dict[str, Any], hab_stats: Dict[str, Any], solar_body: str) -> Dict[str, Any]:
    """
    Update the habitat_stats dictionary based on the given module and solar body.
    """
    for k in hab_stats:
        match k:

            case "crew":
                hab_stats[k] += module[k]
                sub_d = "supportMaterials_month"
                for sub_k in c.pop_upkeep:
                    res_upkeep = float(module[k]) * c.pop_upkeep[sub_k]
                    hab_stats[sub_d][sub_k] = hab_stats[sub_d].get(sub_k, 0) + res_upkeep

            case "power":
                modifier = c.solar_modifiers[solar_body] \
                    if "Solar_Power_Variable_Output" in module.get("specialRules", []) else 1
                hab_stats[k] += module[k] * modifier

            case "supportMaterials_month":
                for sub_k, sub_v in module.get(k, {}).items():
                    hab_stats[k][sub_k] = hab_stats[k].get(sub_k, 0) + sub_v

            case "techBonuses":
                for tech in module.get(k, []):
                    category, bonus = tech["category"], tech["bonus"]
                    hab_stats[k][category] = hab_stats[k].get(category, 0) + bonus

            case "leoBonuses":
                if module["friendlyName"] in c.leo_bonuses and solar_body == "Earth (LEO)":
                    bonus = c.leo_bonuses[module["friendlyName"]]
                    hab_stats[k][bonus["category"]] = hab_stats[k].get(bonus["category"], 0) + bonus["bonus"]

            case "CanFoundHabs":
                if any(v.startswith("CanFoundTier") for v in module.get("specialRules", [])):
                    hab_stats["CanFoundHabs"] = True

            case _:
                hab_stats[k] += module.get(k, 0)

    return hab_stats


def display_habitat_stats(habitat_data: Dict[str, Any], all_modules: Dict[str, Dict[str, Any]]) -> None:
    """
    Display the habitat stats in the Streamlit app.
    """
    module_list = [m[1] for m in habitat_data["cells"].values() if m[1]]

    hab_stats = get_default_stats()
    for module in module_list:
        module_data = all_modules[module]
        solar_body = habitat_data["body"]
        update_habitat_stats(module_data, hab_stats, solar_body)

    st.markdown("**Habitat Stats**")
    col_stats1, col_stats2, s = st.columns(c.ui_layouts["hab_stats"], gap="small")
    cols_stats = [col_stats1, col_stats2]
    col_stats_index = 0

    for k in hab_stats:
        if hab_stats[k] != 0:
            match k:

                case "power":
                    icon = get_base64_image(f"{k}_negative" if hab_stats[k] <= 0 else k)
                    with cols_stats[col_stats_index]:
                        st.write(f"{icon}: {format_number(hab_stats[k])}", unsafe_allow_html=True)
                    col_stats_index = 1 - col_stats_index  # Toggle between column 0 and 1

                case "supportMaterials_month":
                    st.write("######")
                    st.markdown("**Monthly Upkeep**")
                    col_upkeep1, col_upkeep2, u = st.columns(c.ui_layouts["hab_stats"], gap="small")
                    cols_upkeep = [col_upkeep1, col_upkeep2]
                    col_upkeep_index = 0

                    # Add farm module discounts for volatiles and water/
                    for sub_k in hab_stats[k]:
                        match sub_k:
                            case res if res in ("volatiles", "water"):
                                for module in module_list:
                                    if module in c.farm_supply.keys():
                                        discount = c.farm_supply[module] * c.pop_upkeep[res]
                                        hab_stats[k][res] = hab_stats[k].get(res, 0) - discount

                        with cols_upkeep[col_upkeep_index]:
                            if hab_stats[k][sub_k] <= 0:
                                continue
                            icon = get_base64_image(sub_k)
                            value = hab_stats[k][sub_k]
                            st.write(f"{icon}: {format_number(value)}", unsafe_allow_html=True)
                        col_upkeep_index = 1 - col_upkeep_index

                case "techBonuses":
                    if not hab_stats[k]:
                        continue
                    st.write("######")
                    st.markdown("""**Tech Bonuses**  
                       :gray[(Diminished past 50%)]""")
                    col_tech1, col_tech2, u = st.columns(c.ui_layouts["hab_stats"], gap="small")
                    cols_tech = [col_tech1, col_tech2]
                    col_tech_index = 0

                    for sub_k in hab_stats[k]:
                        with cols_tech[col_tech_index]:
                            icon = get_base64_image(sub_k)
                            value = hab_stats[k][sub_k] * 100
                            st.write(f"{icon}: {format_number(value)}%",
                                     unsafe_allow_html=True)
                        col_tech_index = 1 - col_tech_index

                case "leoBonuses":
                    if not hab_stats[k]:
                        continue
                    st.write("######")
                    st.markdown("**LEO Bonuses**")

                    for sub_k in hab_stats[k]:
                        # noinspection SpellCheckingInspection
                        if sub_k == "Miltech":
                            st.write(f"{sub_k.title()}: {hab_stats[k][sub_k]} :gray[(Max: 0.3)]")
                        elif sub_k in ("Public Campaign", "Alien Detection"):
                            st.write(f"{sub_k.title()}: {hab_stats[k][sub_k]} :gray[(Max: 9)]")
                        else:
                            st.write(f"{sub_k.title()}: {hab_stats[k][sub_k]}% :gray[(Max: 30%)]")

                case "CanFoundHabs":
                    if hab_stats["CanFoundHabs"]:
                        icon = get_base64_image(k)
                        st.write(f"{icon}", unsafe_allow_html=True)

                case _:
                    with cols_stats[col_stats_index]:
                        icon = get_base64_image(k)
                        if k in ("allowsShipConstruction", "allowsResupply"):
                            st.write(f"{icon}", unsafe_allow_html=True)
                        else:
                            st.write(f"{icon}: {hab_stats[k]}", unsafe_allow_html=True)
                    col_stats_index = 1 - col_stats_index  # Toggle between column 0 and 1
