import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
from gTTS import gTTS
import base64
import numpy as np


def STT(audio):
    filename = "input.mp3"
    wav_file = open(filename, "wb")
    wav_file.write(audio.tobytes())
    wav_file.close()

    audio_file = open(filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    audio_file.close()

    os.remove(filename)
    return transcript["text"]

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model = model, messages = prompt)
    sysem_message = response["choices"][0]["message"]
    return sysem_message["content"]

def TTS(response):
    filename = "output.mp3"
    tts = gTTS(text = response, lang="ko")
    tts.save(filename)

    with open(filename, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay = "True">
            <source src = "data:audio/mp3;base64, {b64}" type = "audio/mp3">
            </audio>
        """
        st.markdown(md, unsafe_allow_html=True,)
    os.remove(filename)

def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")
    
    flag_start = False

st.header("음성비서 프로그램")
st.markdown("---")
with st.expander("음성 비서 프로그램에 관하여", expanded=True):
    st.write(
        """
        -음성비서 프로그램 UI 스트림릿 이용 제작.
        -STT는 OpenAI의 Whisper AI를 이용, 제작.
        -답변은 Open AI의 GPT모델 활용 제작.
        -TTS는 구글의 Google Translate TTS 활용.
        """
    )
    st.markdown("")
    with st.sidebar:
        openai.api_key = st.text_input(label="OPENAI API 키", 
                                       placeholder="Enter Your API Key", value="", type="password")
        st.markdown("---")

        if st.button(label="초기화"):
            model = st.button(label="초기화")

col1, col2 = st.columns(2)
with col1:
    st.subheader("질문하기")
with col2:
    st.subheader("질문/답변")

    if flag_start:
        response = ask_gpt(st.session_state["messages"], model)
        st.session_state["messages"] = st.session_state["messages"] + [{"role":"system", "content":response}]
        now = datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"] + [("bot", now, response)]

for sender, time, message in st.session_state["chat"]:
    if sender == "user":
        st.write(f'<div style="display:flex;align-items:center;">
                 <div style= "background-color:007AFF;
                 color:white;
                 border-radius: 12px;
                 padding:8px 12px;
                 margin-right:8px; ">
                 {message}</div><div style="font-size:0.8rem;
                 color:gray;">
                 {time}</div></div>', unsafe_allow_html=True)
        st.write("")
    else:
        st.write(f'<div style="display:flex;align-items:center;
                 justify-content:flex-end;">
                 <div style= color:lightgray;
                 border-radius: 12px;
                 padding:8px 12px;
                 margin-left:8px;">
                 {message}</div><div style="font-size:0.8rem;
                 color:gray;">
                 {time}</div></div>', unsafe_allow_html=True)
        st.write("")

        TTS(response)

audio = audiorecorder ("클릭하여 녹음하기", "녹음 중...")
if len(audio) > 0 and not np.array_equal(audio, st.session_state["check_audio"]):
    st.audio(audio.tobytes())
    question = STT(audio)
    now = datetime.now().strftime("%H:%M")
    st.session_state["chat"] = st.session_state["chat"] + [("user", now, question)]
    st.session_state["messages"] = st.session_state["messages"] + [{"role":"user","content":question}]
    st.session_state["check_audio"] = audio
    flag_start = True
    
if __name__=="main":
    main()