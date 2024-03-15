"""SpeechToText Streamlit App."""
import datetime
import os
import sys
import time

import streamlit as st
import whisperx
from audio_recorder_streamlit import audio_recorder

TASKS = {
    "transcribe": "Just transcribe",
    "translate": "Transcribe and translate",
}

if "audio_file" not in st.session_state:
    st.session_state["audio_file"] = None


def transcribe_audio(file_path, task_option, model):
    """
    Transcribe the audio file at the specified path.

    :param file_path: The path of the audio file to transcribe
    :return: The transcribed text
    """
    audio = whisperx.load_audio(file_path)
    return model.transcribe(audio, task=task_option)


def save_audio_file(audio_bytes, file_extension):
    """
    Save audio bytes to a file with the specified extension.

    :param audio_bytes: Audio data in bytes
    :param file_extension: The extension of the output audio file
    :return: The name of the saved audio file
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"audio_{timestamp}.{file_extension}"

    with open(file_name, "wb") as f:
        f.write(audio_bytes)

    return file_name


def set_audio_option(audio_option):
    """Set audio option."""
    if audio_option == "Audio File":
        if audio_file := st.sidebar.file_uploader(
            "Upload Audio", type=["mp3", "mp4", "wav", "m4a"]
        ):
            file_extension = audio_file.type.split("/")[1]
            st.session_state.audio_file = save_audio_file(
                audio_file.read(), file_extension
            )
    elif audio_option == "Microphone":
        with st.sidebar:
            if audio_bytes := audio_recorder():
                st.session_state.audio_file = save_audio_file(audio_bytes, "mp3")


def set_control_panel():
    """Set the control panel."""
    st.sidebar.title("Control panel")
    st.sidebar.markdown("---")

    st.sidebar.markdown("## STT model size")
    model_size = st.sidebar.selectbox(
        "Select the size of the STT model:",
        ["tiny", "base", "small", "medium", "large"],
        format_func=lambda x: x.capitalize(),
    )
    model = whisperx.load_model(
        model_size,
        device="cpu",
        compute_type="int8",
        download_root=f"{os.path.expanduser('~')}/.cache/whisper-models",
    )
    st.sidebar.markdown("---")

    st.sidebar.markdown("## Audio source")
    audio_option = st.sidebar.radio("Get audio from:", ["Audio File", "Microphone"])
    set_audio_option(audio_option)
    st.sidebar.markdown("---")

    st.sidebar.markdown("## Task")
    task_option = st.sidebar.radio(
        "Select the task to perform:",
        ["transcribe", "translate"],
        format_func=lambda x: TASKS[x],
    )
    st.sidebar.markdown("---")

    return model, task_option


def transcribe(transcript_text):
    """Transcribe."""
    st.header("Transcript")
    segments = list(transcript_text["segments"])

    def stream_data():
        for segment in segments:
            for word in segment["text"].split(" "):
                yield f"{word} "
                time.sleep(0.02)

    st.write_stream(stream_data)


def main():
    """Main function to run the Whisper Transcription app."""
    st.title("Speech To Text")
    st.markdown("---")

    model, task_option = set_control_panel()

    # Transcribe the audio file
    if st.session_state.audio_file:
        st.audio(st.session_state.audio_file)
        # Transcribe button action

        if st.button("Transcribe"):
            # Find the newest audio file
            transcript_text = transcribe_audio(
                st.session_state.audio_file, task_option, model
            )

            # Display the transcript
            transcribe(transcript_text)

            # Save the transcript to a text file
            with open("transcript.txt", "w") as f:
                f.write(
                    " ".join(
                        [segment["text"] for segment in transcript_text["segments"]]
                    )
                )

            # Provide a download button for the transcript
            st.download_button(
                "Download Transcript",
                " ".join([segment["text"] for segment in transcript_text["segments"]]),
            )


if __name__ == "__main__":
    # Set up the working directory
    working_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(working_dir)

    # Run the main function
    main()
