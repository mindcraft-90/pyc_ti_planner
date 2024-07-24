from PIL import Image
from typing import Any, Union, Dict

ModuleData = Dict[str, Any]


def add_frame(module_sprite: Image, wide: bool = False) -> Image:
    """
    Add a frame over the module sprite, to indicate it is selected.
    """
    frame_square = "data/misc/frame.png"
    frame_wide = "data/misc/frame_wide.png"
    frame = Image.open(frame_wide if wide else frame_square).resize(module_sprite.size)

    return Image.alpha_composite(frame, module_sprite)


def module_image(core: ModuleData, label: str, st_state, all_modules) -> Union[Image, str]:
    """
    Determine the appropriate image for a module based on its state.
    Returns a numpy array of the image.
    """
    cell = st_state.habitat["cells"][label]

    try:
        if cell[-1] is None:
            if cell[0] == 2:
                image_file = f"{st_state.habitat['type']}_T{core['tier']}_{core['dataName']}"
                st_state.habitat["cells"][label][-1] = core["dataName"]
                image_path = f"_resources/sprites/{image_file}.png"
            else:
                image_path = f"_resources/sprites/T{core['tier']}_Empty_Module.png"

        else:
            sprite = f"{st_state.habitat['type']}_T{all_modules[cell[-1]]['tier']}_{cell[-1]}.png"
            image_path = f"_resources/sprites/{sprite}"

        module_sprite = Image.open(image_path)
    except FileNotFoundError:
        image_path = "data/misc/missing_sprite.png"
        module_sprite = Image.open(image_path)

    if not image_path.endswith("_Empty_Module.png") and cell[0] != 3 and core["tier"] != 3:
        if label.startswith("0_"):
            module_sprite = module_sprite.rotate(180)
        elif label in ["1_0", "1_1", "1_2"]:
            module_sprite = module_sprite.rotate(270)
        elif label in ["1_4", "1_5", "1_6"]:
            module_sprite = module_sprite.rotate(90)

    if label == st_state.clicked_cell and cell[0] != 2:
        return add_frame(module_sprite, wide=True if cell[0] == 3 and cell[-1] else False)
    return module_sprite


def module_tooltip(core: ModuleData, label: str, st_state, all_modules) -> str:
    if st_state.habitat["cells"][label][-1] is None:
        if st_state.habitat["cells"][label][0] == 2:
            return core["friendlyName"]
        return "Empty Module"

    module_name = st_state.habitat["cells"][label][-1]
    return f"{all_modules[module_name]['friendlyName']}"
