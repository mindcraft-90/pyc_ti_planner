////
// Code borrowed and adapted from blackary.
// https://github.com/blackary/streamlit-image-coordinates
////
function rightClickEvent(value) {
    Streamlit.setComponentValue(0)
}

function leftClickEvent(value) {
    Streamlit.setComponentValue(value)
}

function onRender(event) {
    let {src, height, width, use_column_width, tooltip} = event.detail.args;
    const img = document.getElementById("image");

    if (img.src !== src) {
        img.src = src;
    }

    function resizeImage() {
        img.classList.remove("auto", "fullWidth");
        img.removeAttribute("width");
        img.removeAttribute("height");

        if (use_column_width === "always" || use_column_width === true) {
            img.classList.add("fullWidth");
        } else if (use_column_width === "auto") {
            img.classList.add("auto");
        } else {
            if (!width && !height) {
                width = img.naturalWidth;
                height = img.naturalHeight;
            } else if (!height) {
                height = width * img.naturalHeight / img.naturalWidth;
            } else if (!width) {
                width = height * img.naturalWidth / img.naturalHeight;
            }
            img.width = width;
            img.height = height;
        }

        Streamlit.setFrameHeight(img.height);
    }

    img.onload = resizeImage;
    window.addEventListener("resize", resizeImage);

    // Add event listeners for hover effect
    img.onmouseenter = function() {
        this.classList.add('highlight');
        this.title = tooltip || '';
    };
    img.onmouseleave = function() {
        this.classList.remove('highlight');
    };

    // When image is left clicked, send the timestamp to Python
    img.onclick = () => leftClickEvent(Date.now());

    // Prevent right-click context menu and send a null value
    img.oncontextmenu = function(e) {
        e.preventDefault();
        rightClickEvent();
        return false;
    };
}

// Render the component whenever python sends a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
