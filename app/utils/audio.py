"""Audio utilities."""
from tempfile import NamedTemporaryFile

import pydub
import streamlit as st

from app.utils.recorder import take_stream_audio


def get_audio(audio_option: str) -> None:
    """Upload audio."""
    if audio_option == "File":
        if uploaded_audio := st.sidebar.file_uploader(
            "Select audio",
            type=["mp3", "wav", "flac"],
            accept_multiple_files=False,
        ):
            with NamedTemporaryFile(suffix=".wav") as temp_file:
                temp_file.write(uploaded_audio.getvalue())
                st.session_state["audio"] = pydub.AudioSegment.from_file(temp_file.name)
    elif audio_option == "Microphone":
        take_stream_audio()
