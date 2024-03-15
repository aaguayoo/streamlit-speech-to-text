"""Init functions."""
import streamlit as st


def init_session_state() -> None:
    """Initialize session state."""
    variables = ["audio", "mic_audio", "mic_audio_filename"]

    for variable in variables:
        if variable not in st.session_state:
            st.session_state[variable] = None
