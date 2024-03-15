"""SpeechToText Streamlit App."""

import streamlit as st
from plot_app import plot_signal
from processing_app import clear_session_states, get_transcription
from utils_app import get_audio, initialize_session_state

initialize_session_state()

st.title("Demo SpeechToText")
st.markdown("---")

sidebar = st.session_state.sidebar = st.sidebar

sidebar.title("Control panel")
if st.session_state["source_state"] is None:
    get_option = sidebar.radio("Get audio from:", ["File", "Microphone"])
    get_audio(get_option, sidebar)


if st.session_state["source_state"] is not None:
    st.session_state.model = sidebar.selectbox(
        "Select the model", ["Offline", "Online"]
    )
    st.session_state.language = sidebar.selectbox(
        "Select the language", ["Spanish", "English"]
    )
    st.write(st.session_state.model)
    plot_signal()
    filename = st.session_state.source_file
    st.audio(filename)
    transcription_response, time = get_transcription(filename)
    transcription = transcription_response[0][0]["transcription"]

    st.header(f"Raw {st.session_state.model} Transcription")
    st.info(transcription)
    st.warning(f"Executed in {time} seconds.")

if sidebar.button("Add another audio", on_click=clear_session_states):
    pass

sidebar.info(
    """This app uses the Speech-to-Text API, for more information visit:
     https://LyticaMx.github.io/voiceutils-speechToText/"""
)
