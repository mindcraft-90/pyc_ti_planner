from PIL import Image

from modules.habitat_stats import format_number
from modules.constants import ModuleData


def add_frame(module_sprite: Image, wide: bool = False) -> Image:
    """
    Add a frame over the module sprite, to indicate it is selected.
    """
    frame_square = "data/misc/frame.png"
    frame_wide = "data/misc/frame_wide.png"
    frame = Image.open(frame_wide if wide else frame_square).resize(module_sprite.size)

    return Image.alpha_composite(frame, module_sprite)


def module_image(core: ModuleData, label: str, state, all_modules):
    """
    Determine the appropriate image for a module based on its state.
    Returns a numpy array of the image.
    """
    cell = state.habitat["cells"][label]

    if label in state:
        cell[-1] = None if state[label] == 0 else cell[-1]

    try:
        if cell[-1] is None:
            if cell[0] == 2:
                image_file = f"{state.habitat['type']}_T{core['tier']}_{core['dataName']}"
                state.habitat["cells"][label][-1] = core["dataName"]
                image_path = f"_resources/sprites/{image_file}.png"
            else:
                image_path = f"_resources/sprites/T{core['tier']}_Empty_Module.png"

        else:
            sprite = f"{state.habitat['type']}_T{all_modules[cell[-1]]['tier']}_{cell[-1]}.png"
            image_path = f"_resources/sprites/{sprite}"

        module_sprite = Image.open(image_path)
    except FileNotFoundError:
        image_path = "data/misc/missing_sprite.png"
        module_sprite = Image.open(image_path)

    # if not image_path.endswith("_Empty_Module.png") and cell[0] != 3 and core["tier"] != 3:
    #     if label.startswith("0_"):
    #         module_sprite = module_sprite.rotate(180)
    #     elif label in ["1_0", "1_1", "1_2"]:
    #         module_sprite = module_sprite.rotate(270)
    #     elif label in ["1_4", "1_5", "1_6"]:
    #         module_sprite = module_sprite.rotate(90)

    base_size = (512, 128) if cell[0] == 3 and cell[-1] else (128, 128)
    sprite_base = Image.new('RGBA', base_size, (0, 0, 0, 0))

    # Resize Module Sprite based on Tier
    tier_sizes = {
        1: {1: 1.0},
        2: {1: 0.7, 2: 1.0},
        3: {1: 0.4, 2: 0.7, 3: 1.0}
    }

    module_tier = all_modules[cell[-1]]['tier'] if cell[-1] else core['tier']
    max_dimension = int(base_size[0] * tier_sizes[core["tier"]][module_tier])
    scale = min(max_dimension / module_sprite.width, max_dimension / module_sprite.height)
    new_size = (int(module_sprite.width * scale), int(module_sprite.height * scale))

    module_sprite = module_sprite.resize(new_size)

    x = (base_size[0] - module_sprite.width) // 2
    y = (base_size[1] - module_sprite.height) // 2
    sprite_base.paste(im=module_sprite, box=(x, y), mask=module_sprite)

    if label == state.clicked_cell and cell[0] != 2:
        return add_frame(sprite_base, wide=True if cell[0] == 3 and cell[-1] else False)

    return sprite_base


def module_tooltip(label: str, state, all_modules) -> str:
    if state.habitat["cells"][label][-1] is None:
        return "Empty Module"

    pretty_names = {
        "power": "Power",
        "money": "Money",
        "incomeResearch_month": "Research",
        "boost": "Boost",
        "missionControl": "Mission Control",
        "water": "Water",
        "volatiles": "Volatiles",
        "metals": "Metals",
        "nobleMetals": "Noble Metals",
        "fissiles": "Fissiles",
        "incomeMoney_month": "Money",
        "incomeAntimatter_month": "Antimatter",
        "incomeProjects": "Projects",
        "incomeInfluence_month": "Influence",
        "incomeOps_month": "Ops",
    }

    module_name = state.habitat["cells"][label][-1]
    module_stat = all_modules[module_name]

    # Tooltip bit: Monthly Incomes and Bonuses
    relevant_items = [(k, v) for k, v in module_stat.items() if k in pretty_names and v > 0]
    sorted_incomes = sorted(relevant_items, key=lambda x: list(pretty_names.keys()).index(x[0]))
    incomes_bonuses = ", ".join([f"{pretty_names[k]}: {v if k == 'incomeAntimatter_month' else format_number(v)}"
                                 for k, v in sorted_incomes if v > 0])

    tech_bonuses = ", ".join([f"{tech['category']}: {format_number(tech['bonus'] * 100)}%"
                              for tech in module_stat.get("techBonuses", [])])
    if tech_bonuses:
        incomes_bonuses += ", " + tech_bonuses if incomes_bonuses else tech_bonuses

    # Tooltip bit: Monthly Support Costs
    power_cost = f"Power: {module_stat['power']}, " if module_stat["power"] < 0 else ""

    crew_costs = (module_stat["crew"] * 7 / 240)
    total_costs = module_stat["supportMaterials_month"].copy()
    total_costs["water"] = total_costs.get("water", 0) + crew_costs
    total_costs["volatiles"] = total_costs.get("volatiles", 0) + crew_costs

    sorted_costs = sorted(total_costs.items(), key=lambda x: list(pretty_names.keys()).index(x[0]))
    support_costs = ", ".join([f"{pretty_names[k]}: -{format_number(v)}" for k, v in sorted_costs if v != 0])

    # Main tooltip
    tooltip = f"""\
{module_stat['friendlyName']}
Tier {module_stat['tier']} module, {module_stat['crew']} crew, {module_stat['baseMass_tons']} tons

Monthly Incomes and Bonuses:
{incomes_bonuses}
Monthly Support Costs:
{power_cost}{support_costs}"""

    return tooltip
