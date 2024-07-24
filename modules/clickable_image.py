import base64
import numpy as np
import streamlit.components.v1 as components

from io import BytesIO
from pathlib import Path
from PIL import Image
from streamlit.elements.image import UseColumnWith

####
# Code borrowed and adapted from blackary.
# https://github.com/blackary/streamlit-image-coordinates
####

# Tell streamlit that there is a component called clickable_image,
# and that the code to display that component is in the "frontend" folder
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "streamlit_clickable_image", path=str(frontend_dir)
)


# Create the python function that will be called
def clickable_image(
    source: str | Path | np.ndarray | object,
    height: int | None = None,
    width: int | None = None,
    key: str | None = None,
    use_column_width: UseColumnWith | str | None = None,
    tooltip: str | None = None,
):
    """
    Display a clickable image and return a Unix timestamp when clicked.

    Parameters
    ----------
    source : str | Path | object
        The image source
    height : int | None
        The height of the image. If None, the original height will be used.
    width : int | None
        The width of the image. If None, the original width will be used.
    key : str | None = None
        An optional string to use as the unique key for the widget.
    use_column_width : "auto", "always", "never", or bool
        If "auto", set the image's width to its natural size,
        but do not exceed the width of the column.
        If "always" or True, set the image's width to the column width.
        If "never" or False, set the image's width to its natural size.
        Note: if set, `use_column_width` takes precedence over the `width` parameter.
    tooltip : str | None = None
        An optional string to use as a tooltip for the widget.

    Returns
    -------
    int
        Unix timestamp of when the image was clicked.
    """

    if isinstance(source, (Path, str)):
        if not str(source).startswith("http"):
            content = Path(source).read_bytes()
            src = "data:image/png;base64," + base64.b64encode(content).decode("utf-8")
        else:
            src = str(source)
    elif hasattr(source, "save"):
        buffered = BytesIO()
        source.save(buffered, format="PNG")  # type: ignore
        src = "data:image/png;base64,"
        src += base64.b64encode(buffered.getvalue()).decode("utf-8")  # type: ignore
    elif isinstance(source, np.ndarray):
        image = Image.fromarray(source)
        buffered = BytesIO()
        image.save(buffered, format="PNG")  # type: ignore
        src = "data:image/png;base64,"
        src += base64.b64encode(buffered.getvalue()).decode("utf-8")  # type: ignore
    else:
        raise ValueError(
            "Must pass a string, Path, numpy array or object with a save method"
        )

    return _component_func(
        src=src,
        height=height,
        width=width,
        use_column_width=use_column_width,
        key=key,
        tooltip=tooltip,
    )
