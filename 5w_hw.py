import streamlit as st
from audiorecorder import audiorecorder
import openai
import os
from datetime import datetime
import numpy as np

def STT(audio):
    # STT function remains unchanged
    pass

def ask_gpt(prompt, model):
    response = openai.ChatCompletion.create(model=model, messages=prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]

def TTS(response):
    st.write(response)

def main():
    st.set_page_config(
        page_title="음성 비서 프로그램",
        layout="wide")

    flag_start = False

    if "chat" not in st.session_state:
        st.session_state["chat"] = []

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "system", "content":"You are a thoughtful assistent. Respond to all input in 25 words and answer in korea"}]

    if "check_audio" not in st.session_state:
        st.session_state["check_audio"] = []

    st.header("음성 비서 프로그램")

    st.markdown("---")

    with st.expander("음성 비서 프로그램에 관하여", expanded=True):
        st.write(
        """     
        - 음성비서 프로그램의 UI는 스트림릿을 활용했습니다.
        - STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다. 
        - 답변은 OpenAI의 GPT 모델을 활용했습니다. 
        - 202204248 이동현
        """
        )

    st.markdown("")

    with st.sidebar:
        openai.api_key = st.text_input(label="OPENAI API 키", placeholder="Enter Your API Key", value="", type="password")
        
        st.markdown("---")

        model = st.radio(label="GPT 모델", options=["GPT-4", "GPT-3.5-turbo"])

        st.markdown("---")

        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role":"system", "content":"You are a thought aasistant. Respond to all in 25 words and answer in korea"}]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("음성 질문")
        audio = audiorecorder("음성 질문", "녹음 중...")
        if len(audio) > 0 and not np.array_equal(audio, st.session_state["check_audio"]):
            st.audio(audio.tobytes())

            question = STT(audio)

            now = datetime.now().strftime("%H:%M")

            st.session_state["chat"] = st.session_state["chat"] + [("user", now , question)]
            st.session_state["messages"] = st.session_state["messages"] + [{"role":"user", "content": question}]
            st.session_state["check_audio"] = audio
            flag_start = True
            
    with col1:
        st.subheader("텍스트 질문")
        text_question = st.text_area("텍스트를 입력하세요", "")
        if st.button("텍스트 질문"):
            if text_question.strip() != "":
                st.session_state["chat"] = st.session_state["chat"] + [("user", datetime.now().strftime("%H:%M"), text_question)]
                st.session_state["messages"] = st.session_state["messages"] + [{"role":"user", "content": text_question}]
                flag_start = True

    with col2:
        st.subheader("질문/답변")
        if flag_start:
            if text_question.strip() != "":
                response = ask_gpt(st.session_state["messages"], model)
                text_question = ""
            else:
                response = ask_gpt(st.session_state["messages"], model)

            system_response = f"I'm not just an assistant, I'm your virtual buddy! Here's what I think: {response}"

            st.session_state["messages"] = st.session_state["messages"] + [{"role":"system", "content": system_response}]

            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("bot", now, system_response)]

            for sender, time, message in st.session_state["chat"]:
                if sender == "user":
                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
                else:
                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)
                    st.write("")
            TTS(system_response)

if __name__=="__main__":
    main()
