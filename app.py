import streamlit as st
import soundfile as sf
import noisereduce as nr
import tempfile
from pydub import AudioSegment
import numpy as np

st.set_page_config(page_title="🎧 Online Noise Reducer")
st.title("🎧 Online Noise Reducer (MP3 & WAV)")

uploaded_file = st.file_uploader("Upload WAV or MP3 audio file", type=["wav","mp3"])

if uploaded_file:
    st.audio(uploaded_file, start_time=0)
    st.write("Processing... Please wait ⏳")

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
        if uploaded_file.name.endswith(".mp3"):
            audio = AudioSegment.from_file(uploaded_file, format="mp3")
            audio.export(tmp_wav.name, format="wav")
        else:
            tmp_wav.write(uploaded_file.read())
        tmp_path = tmp_wav.name

    # Load audio
    audio_data, sr = sf.read(tmp_path)
    if len(audio_data.shape) > 1:
        audio_data = audio_data.mean(axis=1)  # convert stereo to mono

    # Apply noise reduction
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sr)

    # Save cleaned audio
    output_path = tmp_path.replace(".wav","_clean.wav")
    sf.write(output_path, reduced_noise, sr)

    st.success("Noise reduction complete ✅")
    st.audio(output_path)
    st.download_button(
        label="⬇️ Download Cleaned Audio",
        data=open(output_path,"rb").read(),
        file_name="cleaned_audio.wav",
        mime="audio/wav"
    )
