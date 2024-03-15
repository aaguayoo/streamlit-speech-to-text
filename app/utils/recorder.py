"""Take picture functions."""
import datetime
import logging
import os
import queue
import threading
import time

import av
import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

logger = logging.getLogger(__name__)
lock = threading.Lock()
audio_container = {"audio": None, "sample_rate": None}


def record_callback(frame: av.AudioFrame) -> av.AudioFrame:
    """Video callback function."""
    audio = frame.to_ndarray()
    with lock:
        audio_container["audio"] = audio
        audio_container["sample_rate"] = frame.sample_rate

    return frame


def take_record():
    """Take record."""
    st.session_state.mic_audio = audio_container["audio"]


def remove_audio():
    """Remove audio."""
    st.session_state.mic_audio = None
    st.session_state.mic_audio_filename = None


def save_audio():
    """Save audio."""
    if st.session_state.mic_audio_filename and st.session_state.mic_audio is not None:
        st.session_state.mic_audio.export(
            f"{st.session_state.mic_audio_filename}", format="wav"
        )
        st.session_state.audio = st.session_state.mic_audio
        st.session_state.mic_audio = None


def take_stream_audio():
    """Take stream audio record."""
    with st.sidebar:
        webrtc_ctx = webrtc_streamer(
            key="take_record",
            mode=WebRtcMode.SENDONLY,
            audio_receiver_size=256,
            rtc_configuration={
                "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
            },
            media_stream_constraints={"audio": True},
        )

    audio_placeholder = st.sidebar.empty()

    while webrtc_ctx.audio_receiver:
        audio_placeholder.info("Recording...")

        try:
            audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=1)
        except queue.Empty:
            logger.warning("Queue is empty. Abort.")
            break

        sound_chunk = pydub.AudioSegment.empty()
        for audio_frame in audio_frames:
            sound = pydub.AudioSegment(
                data=audio_frame.to_ndarray().tobytes(),
                sample_width=audio_frame.format.bytes,
                frame_rate=audio_frame.sample_rate,
                channels=len(audio_frame.layout.channels),
            )
            sound_chunk += sound

        if len(sound_chunk) > 0:
            if st.session_state.mic_audio is None:
                st.session_state.mic_audio = pydub.AudioSegment.empty()

            st.session_state.mic_audio += sound_chunk

    with st.sidebar:
        if st.session_state.mic_audio:
            st.write(st.session_state.mic_audio)

    with audio_placeholder:
        if st.session_state.mic_audio is not None:
            tmp_filename = f"""record-{
                    datetime.datetime.now().strftime('%d-%m-%Y-%H-%M-%S')
                    }.wav"""
            tmp_filename = st.text_input("Enter file name", tmp_filename)
            st.session_state.mic_audio_filename = os.path.join(
                os.environ["PATH_AUDIOS"], "tmp_recordings", tmp_filename
            )

        with st.sidebar:
            if (
                st.session_state.mic_audio_filename
                and st.session_state.mic_audio is not None
            ):
                col1, col2 = st.columns(2)
                if col1.button(
                    "💾", key=f"{time.time()+1}", type="secondary", on_click=save_audio
                ):
                    st.info("Audio saved.")
                if col2.button(
                    "Remove audio",
                    key=f"{time.time()+1}",
                    on_click=remove_audio,
                    type="secondary",
                ):
                    pass

    if (
        st.session_state.mic_audio is None
        and st.session_state.mic_audio_filename
        and webrtc_ctx.state.playing
    ):
        st.sidebar.warning("Stop record to continue.")
    elif (
        st.session_state.mic_audio is None
        and st.session_state.mic_audio_filename
        and not webrtc_ctx.state.playing
    ):
        audio = st.session_state.mic_audio_filename
        del st.session_state.mic_audio_filename
        return audio
