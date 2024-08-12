import base64
import streamlit as st

from modules import constants as c


def get_default_stats() -> c.ModuleData:
    """
    Retrieve a blank set of desired habitat stats.
    """
    return {
        "crew": 0,
        "baseMass_tons": 0,
        "power": 0,
        "incomeMoney_month": 0,
        "incomeInfluence_month": 0,
        "incomeOps_month": 0,
        "incomeResearch_month": 0,
        "incomeProjects": 0,
        "missionControl": 0,
        "supportMaterials_month": {"water": 0, "volatiles": 0, "metals": 0, "nobleMetals": 0, "fissiles": 0},
        "incomeAntimatter_month": 0,
        "allowsResupply": False,
        "CanFoundHabs": False,  # first nanofactory is 25%, second is 30% ...
        "allowsShipConstruction": False,
        "spaceCombatValue": 0,
        "techBonuses": {},
        "leoBonuses": {},
    }


def format_number(value: float, precision: int = 1) -> float | int:
    """
    Format float numbers to 3 decimals and strip trailing '0's and '.'s.
    """
    return value.__round__(precision) if value % 1 else int(value)


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


def update_habitat_stats(module: c.ModuleData, hab_stats: c.ModuleData, solar_body: str) -> c.ModuleData:
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


def display_habitat_stats(habitat_data: c.ModuleData, all_modules: dict[str, c.ModuleData]) -> None:
    """
    Display the habitat stats in the Streamlit app.
    """
    module_list = [m[1] for m in habitat_data["cells"].values() if m[1]]

    hab_stats = get_default_stats()
    solar_body = habitat_data["body"]
    for module in module_list:
        module_data = all_modules[module]
        update_habitat_stats(module_data, hab_stats, solar_body)

    st.markdown("**Habitat Stats**")
    st.write(f"Crew {hab_stats['crew']}, Mass {hab_stats['baseMass_tons']} tons")

    col_stats1, col_stats2, col_stats3, col_stats4, s = st.columns(c.ui_layouts["hab_stats"])
    cols_stats = [col_stats1, col_stats2, col_stats3, col_stats4]
    col_stats_index = 0

    for k in hab_stats:
        if (hab_stats[k] != 0 or k == "incomeMoney_month") and k not in ("crew", "baseMass_tons"):
            match k:

                case "power":
                    icon = get_base64_image(f"{k}_negative" if hab_stats[k] <= 0 else k)
                    with cols_stats[col_stats_index]:
                        st.write(f"{icon} {format_number(hab_stats[k])}", unsafe_allow_html=True)
                    col_stats_index = (col_stats_index + 1) % 4

                case "incomeProjects":
                    icon = get_base64_image(k)
                    with cols_stats[col_stats_index]:
                        st.write(f"{icon} {hab_stats[k] * 5}%", unsafe_allow_html=True)
                    col_stats_index = (col_stats_index + 1) % 4

                case "supportMaterials_month":
                    # Add farm module discounts for volatiles and water
                    for sub_k in hab_stats[k]:
                        if sub_k in ("volatiles", "water"):
                            for module in module_list:
                                if module in c.farm_supply.keys():
                                    discount = c.farm_supply[module] * c.pop_upkeep[sub_k]
                                    hab_stats[k][sub_k] = hab_stats[k].get(sub_k, 0) - discount
                            # Farms would be a net gain if not forced to 0
                            hab_stats[k][sub_k] = 0 if hab_stats[k][sub_k] < 0 else hab_stats[k][sub_k]

                        if any("Mining" in m for m in module_list):
                            # Sub_k is a positive number that gets flipped to a negative later.
                            # Therefor, we substract the site resource if a mining module exists.
                            hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0)

                        with cols_stats[col_stats_index]:
                            if hab_stats[k][sub_k] == 0 or sub_k == "money":
                                continue
                            icon = get_base64_image(sub_k)
                            value = -1 * hab_stats[k][sub_k]
                            st.write(f"{icon} {format_number(value)}", unsafe_allow_html=True)
                        col_stats_index = (col_stats_index + 1) % 4

                case "incomeAntimatter_month":
                    icon = get_base64_image(k)
                    prefixes = ['', 'µ', 'n', 'p', 'f', 'a']
                    prefix_values = [1e0, 1e-6, 1e-9, 1e-12, 1e-15, 1e-18]

                    if hab_stats[k] >= 0.1:
                        value = format_number(hab_stats[k], precision=2)
                    elif hab_stats[k] >= 0.001:
                        value = f".{f'.{hab_stats[k]:.3f}'.split('.')[-1]}"
                    elif 0.001 > hab_stats[k] > 0:
                        for val, prefix in zip(prefix_values, prefixes):
                            if abs(hab_stats[k]) >= val or prefix == 'a':
                                value = f"{hab_stats[k] / val:.3f}".rstrip('0').rstrip('.') + prefix
                                break
                    else:
                        value = hab_stats[k]

                    with cols_stats[col_stats_index]:
                        st.write(f"{icon} {value}", unsafe_allow_html=True)
                    col_stats_index = (col_stats_index + 1) % 4

                case "CanFoundHabs":
                    t3_count = len([m for m in module_list if m == "NanofacturingComplex"])
                    t2_count = len([m for m in module_list if m == "Nanofactory"])
                    t1_count = len([m for m in module_list if m == "ConstructionModule"])

                    bonuses = [(0.40, t3_count), (0.25, t2_count), (0.10, t1_count)]
                    sorted_bonuses = sorted(bonuses, reverse=True)

                    def get_next_bonus(previous_bonuses):
                        return next((b for b, count in sorted_bonuses if
                                     count > len(previous_bonuses) or (count > 0 and b not in previous_bonuses)), 0)

                    first_bonus = get_next_bonus([])
                    second_bonus = get_next_bonus([first_bonus])
                    third_bonus = get_next_bonus([first_bonus, second_bonus])

                    bonus = first_bonus + (second_bonus * 0.18) + (third_bonus * 0.0075)
                    print(bonus * 100)
                    print(f"{str(bonus * 100).split('.')[0]}%")

                    with cols_stats[col_stats_index]:
                        icon = get_base64_image(k)
                        st.write(f"{icon} {round(bonus * 100)}%", unsafe_allow_html=True)
                    col_stats_index = (col_stats_index + 1) % 4

                case "techBonuses":
                    if not hab_stats[k]:
                        continue
                    st.write("######")
                    st.markdown("""**Tech Bonuses**  
                       :gray[(Diminished past 50%)]""")
                    col_tech1, col_tech2, col_tech3, col_tech4, t = st.columns(c.ui_layouts["hab_stats"])
                    cols_tech = [col_tech1, col_tech2, col_tech3, col_tech4]
                    col_tech_index = 0

                    for sub_k in hab_stats[k]:
                        with cols_tech[col_tech_index]:
                            icon = get_base64_image(sub_k)
                            value = hab_stats[k][sub_k] * 100
                            st.write(f"{icon} {format_number(value)}%", unsafe_allow_html=True)
                        col_tech_index = (col_tech_index + 1) % 4

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

                case _:
                    with cols_stats[col_stats_index]:
                        icon = get_base64_image(k)
                        value = hab_stats[k] - hab_stats["supportMaterials_month"]["money"] \
                            if k == "incomeMoney_month" else hab_stats[k]

                        display = f"{icon} {format_number(value)}" if k not in (
                            "allowsResupply", "CanFoundHabs", "allowsShipConstruction") else f"{icon}"
                        st.write(display, unsafe_allow_html=True)
                    col_stats_index = (col_stats_index + 1) % 4
