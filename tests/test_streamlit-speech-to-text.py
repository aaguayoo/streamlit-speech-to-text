"""Package related tests."""
from streamlit-speech-to-text import __version__


def test_streamlit-speech-to-text_version():
    """Checks correct package version."""
    assert __version__ == "0.1.0"
