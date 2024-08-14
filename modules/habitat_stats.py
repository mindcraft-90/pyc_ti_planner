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
        "weightedBuildMaterials": {"water": 0, "volatiles": 0, "metals": 0, "nobleMetals": 0, "fissiles": 0}
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


def construction_bonus(t3_count: int, t2_count: int, t1_count: int) -> float:
    bonuses = (
        (t3_count, 0.40, (1, 0.15, 0.06, 0.028)),
        (t2_count, 0.25, (1, 0.18, 0.08, 0.040)),
        (t1_count, 0.10, (1, 0.20, 0.10, 0.050)),
    )  # T3, T2, T1 bonus = 40%, 25%, 10%; diminishing returns tuple

    total_bonus = 0.0
    applied_bonuses = 0  # Track how many bonuses have been applied
    highest_tier_coeffs = None  # Store the coefficients of the highest tier applied

    for count, base_bonus, coeffs in bonuses:
        if count > 0 and highest_tier_coeffs is None:  # Determine the highest tier and use those coefficients
            highest_tier_coeffs = coeffs

        for _ in range(count):  # Highest module tier adds full bonus; subsequent bonuses are diminished
            coeff_index = min(applied_bonuses, len(highest_tier_coeffs) - 1)
            total_bonus += base_bonus * highest_tier_coeffs[coeff_index]
            applied_bonuses += 1

    return min(total_bonus, 0.50)  # Cap total bonus at 50%


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

            case "supportMaterials_month" | "weightedBuildMaterials":
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

    with st.popover(label="Habitat Build Costs", use_container_width=True):
        for k, v in hab_stats["weightedBuildMaterials"].items():
            icon = get_base64_image(k)
            st.write(f"{icon} {format_number(v * 30, precision=2)}", unsafe_allow_html=True)

    col_stats1, col_stats2, col_stats3, col_stats4, s = st.columns(c.ui_layouts["hab_stats"])
    cols_stats = [col_stats1, col_stats2, col_stats3, col_stats4]
    col_stats_index = 0

    for k in hab_stats:
        if ((hab_stats[k] != 0 or k == "incomeMoney_month") and k
                not in ("crew", "baseMass_tons", "weightedBuildMaterials")):

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
                    for sub_k in hab_stats[k]:
                        value = -1 *  hab_stats[k][sub_k]  # Flip the positive value to negative upkeep

                        # Calculate farm module discounts
                        farm_discount = sum(
                            (module in c.farm_supply.keys()) * c.farm_supply.get(module, 0) * c.pop_upkeep.get(sub_k, 0)
                            for module in module_list
                        )
                        # Add farming discounts as long as farm_discount <= -value, else add -value
                        value += min(int(sub_k in ("volatiles", "water")) * farm_discount, -value)

                        # Add site resources based on mining module tier
                        mining_bonuses = {3: 2, 2: 1.5, 1: 1, 0: 0}
                        tier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("tier", 0)
                        value += habitat_data.get("site", {}).get(sub_k, 0) * mining_bonuses[tier]

                        value = format_number(value)
                        with cols_stats[col_stats_index]:
                            if value == 0 or sub_k == "money":
                                continue
                            st.write(f"{get_base64_image(sub_k)} {value}", unsafe_allow_html=True)
                        col_stats_index = (col_stats_index + 1) % 4

                # case "supportMaterials_month":
                #     # Add farm module discounts for volatiles and water
                #     for sub_k in hab_stats[k]:
                #         if sub_k in ("volatiles", "water"):
                #             for module in module_list:
                #                 if module in c.farm_supply.keys():
                #                     discount = c.farm_supply[module] * c.pop_upkeep[sub_k]
                #                     hab_stats[k][sub_k] = hab_stats[k].get(sub_k, 0) - discount
                #             # Farms would be a net gain if not forced to 0
                #             hab_stats[k][sub_k] = 0 if hab_stats[k][sub_k] < 0 else hab_stats[k][sub_k]
                #
                #         # Add mined resources #branchless!
                #         # Sub_k is a positive number that gets flipped to a negative later.
                #         # Therefor, we substract the site resource if a mining module exists.
                #         mining_bonuses = {3: 2, 2: 1.5, 1: 1, 0: 0}
                #         tier = all_modules.get(habitat_data["cells"]["0_3"][-1], {}).get("tier", 0)
                #         # sub_k is positive, so we substract site resources and flip it later
                #         hab_stats[k][sub_k] -= habitat_data.get("site", {}).get(sub_k, 0) * mining_bonuses[tier]
                #
                #         value = format_number(-1 * hab_stats[k][sub_k])  # Flip the positive value to negative upkeep
                #         with cols_stats[col_stats_index]:
                #             if value == 0 or sub_k == "money":
                #                 continue
                #             st.write(f"{get_base64_image(sub_k)} {value}", unsafe_allow_html=True)
                #         col_stats_index = (col_stats_index + 1) % 4

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
                    t3_count = module_list.count("NanofacturingComplex")
                    t2_count = module_list.count("Nanofactory")
                    t1_count = module_list.count("ConstructionModule")
                    bonus = construction_bonus(t3_count, t2_count, t1_count)

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
