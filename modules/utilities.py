import smtplib
import time
import json
import zlib
import base64
import streamlit as st


def download_json_file(st_state):
    return json.dumps(st_state.habitat, separators=(',', ':'))


def upload_json_file(file, error=False):
    if error:
        message = st.empty()
        message.error("No file selected.")
        time.sleep(2)
        message.empty()
        return

    try:
        file_contents = file.getvalue().decode("utf-8")
        loaded_data = json.loads(file_contents)
        st.session_state.habitat = loaded_data
        st.session_state.first_run = False
        st.session_state.pending_core = loaded_data.get("core")  # prevent reset trigger

        message = st.empty()
        message.success("Success! Redirecting...")
        time.sleep(1)
        message.empty()

    except json.JSONDecodeError:
        st.error("Error: Invalid JSON file. Please upload a valid JSON file.")
    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")


def send_email(message):
    host = "smtp.gmail.com"
    port = 587
    username = st.secrets.email.username
    password = st.secrets.email.password
    receiver = username
    # context = ssl.create_default_context()

    with smtplib.SMTP(host, port) as server:
        # server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(username, receiver, message)
        server.quit()


def format_solar_modifier(value: float) -> str:
    s = f"{value:.3f}".rstrip('0')
    return s if s.endswith('.') is False else s + '0'


def habitat_to_url(habitat: dict) -> str:
    """Compress and encode habitat state for URL."""
    json_str = json.dumps(habitat, separators=(',', ':'))
    compressed = zlib.compress(json_str.encode('utf-8'), level=9)
    return base64.urlsafe_b64encode(compressed).decode('utf-8')

def url_to_habitat(param: str) -> dict:
    """Decode and decompress habitat state from URL."""
    compressed = base64.urlsafe_b64decode(param.encode('utf-8'))
    json_str = zlib.decompress(compressed).decode('utf-8')
    return json.loads(json_str)
