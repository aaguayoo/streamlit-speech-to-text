"""Real Time."""
import logging
import os
import queue
import threading

import faster_whisper
import numpy as np
import pydub
import streamlit as st
from streamlit_webrtc import WebRtcMode, webrtc_streamer

logger = logging.getLogger(__name__)
lock = threading.Lock()
audio_container = {"audio": None, "sample_rate": None}


model = faster_whisper.WhisperModel(
    "tiny",
    device="cpu",
    compute_type="int8",
    download_root=f"{os.path.expanduser('~')}/.cache/whisper-models",
)

if "mic_audio" not in st.session_state:
    st.session_state["mic_audio"] = None


webrtc_ctx = webrtc_streamer(
    key="take_record",
    mode=WebRtcMode.SENDONLY,
    audio_receiver_size=2048,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}],
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
            frame_rate=8000,  # audio_frame.sample_rate,
            channels=len(audio_frame.layout.channels),
        )
        sound_chunk += sound

        data = audio_frame.to_ndarray().flatten().astype(np.float32)

        transcription, info = model.transcribe(
            data,
            beam_size=1,
            language="es",
            condition_on_previous_text=True,
        )
        if list(transcription):
            for segment in transcription:
                st.write(segment.text)

    if len(sound_chunk) > 0:
        if st.session_state.mic_audio is None:
            st.session_state.mic_audio = pydub.AudioSegment.empty()

        st.session_state.mic_audio += sound_chunk
