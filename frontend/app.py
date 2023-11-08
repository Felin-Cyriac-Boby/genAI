

import streamlit as st
import json
import requests



st.sidebar.title("Sidebar")
page = st.sidebar.selectbox("Select Page",["Chatbot", "Transcribe"])

def generate_response(input):
        body = {"prompt": input}

        res = requests.post(url = "http://127.0.0.1:8000/ask", data=json.dumps(body))
        return res.text

if page == 'Chatbot':
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content":"How may I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message['content'])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)



import pandas as pd
import numpy as np
import io
import whisper
import ffmpeg

def load_audio(file: (str, bytes), sr: int = 16000):

    if isinstance(file, bytes):
        inp = file
        file = 'pipe:'
    else:
        inp = None

    try:
        # This launches a subprocess to decode audio while down-mixing and resampling as necessary.
        # Requires the ffmpeg CLI and `ffmpeg-python` package to be installed.
        out, _ = (
            ffmpeg.input(file, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=sr)
            .run(cmd="ffmpeg", capture_stdout=True, capture_stderr=True, input=inp)
        )
    except ffmpeg.Error as e:
        raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e

    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

if page == "Transcribe":


    uploaded_file = st.file_uploader("Choose a file", type=['.wav', '.mp3'])


    if uploaded_file is not None:
        # To read file as bytes:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/wav')

        buffer = io.BytesIO(audio_bytes)
        # you need to set the name with the extension
        buffer.name = 'fname'

        audio = load_audio(audio_bytes)
    
        model = whisper.load_model("base")
        result = model.transcribe(audio)
        st.write(result["text"])
        print(result["text"])
