import streamlit as st
from audio_recorder_streamlit import audio_recorder


# Initialize session state variables if they don't exist
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False
if 'is_paused' not in st.session_state:
    st.session_state.is_paused = False
if 'words' not in st.session_state:
    st.session_state.words = []

# Define button callback functions
def start_streaming():
    st.session_state.is_streaming = True
    st.session_state.is_paused = False

def stop_streaming():
    st.session_state.is_streaming = False
    st.session_state.is_paused = False

def pause_streaming():
    st.session_state.is_paused = not st.session_state.is_paused

def add_word():
    if word:
        st.session_state.words.append(word)

def remove_word():
    if selected_word in st.session_state.words:
        st.session_state.words.remove(selected_word)

# Main layout
st.title("Streaming Control")

# Streaming buttons
col1, col2, col3 = st.columns(3)
with col1:
    if not st.session_state.is_streaming:
        st.button("Start Streaming", on_click=start_streaming)
with col2:
    if st.session_state.is_streaming:
        st.button("Stop Streaming", on_click=stop_streaming)
with col3:
    if st.session_state.is_streaming and not st.session_state.is_paused:
        st.button("Pause Streaming", on_click=pause_streaming)
    elif st.session_state.is_paused:
        st.button("Resume Streaming", on_click=pause_streaming)

# Word list management in sidebar
st.sidebar.title("Words")
word = st.sidebar.text_input("Enter a word", key="word_input")
st.sidebar.button("Add Word", on_click=add_word)

if st.session_state.words:
    selected_word = st.sidebar.selectbox("Select a word to remove", st.session_state.words, key="word_selector")
    st.sidebar.button("Remove Selected Word", on_click=remove_word)

# Log area
st.sidebar.title("Logs")
if st.session_state.is_paused:
    st.sidebar.text('Streaming is paused.')
elif st.session_state.is_streaming:
    st.sidebar.text('Streaming is active.')
else:
    st.sidebar.text('Streaming is stopped.')

audio_bytes = audio_recorder(
    text="Start streaming",
    recording_color="#e8b62c",
    neutral_color="#6aa36f",
    icon_name="user",
    icon_size="2x",
)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")
