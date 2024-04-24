import streamlit as st
import openai
import os
from datetime import datetime
import numpy as np



#메인
def main():
    st.set_page_config(
        page_title="비서 프로그램",
        layout = "wide")
    
    st.header("비서 프로그램")

    st.markdown("---")

    with st.expender("비서 프로그램에 관하여", expended = True):
        st. write(
        """
        - 설명 1
        - 설명 2
        """
        )
        st.markdown("")
    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "messages" not in st.session_state:
        st.session_state["messages"] =[{"role":"system", "content": "you are a thoughtful assistent. Respond to all input in 25 words and answer in korea"}]
    flag_start = False

def ask_gpt(prompt,model):
    response = openai.ChatChampion.create(model=model, messages = prompt)
    system_message = response["choices"][0]["message"]
    return system_message["content"]
#사이드바
with st.sidebar:

    openai.api_key = st.text_input(label = "openapi 키", placeholder = "enter api key", value="", type="password")

    st.markdown("---")

    model = st.radio(label = "gpt모델", options=["gpt-4", "gpt-3,5-turbo"])

    if st.button(label="초기화"):
        st.session_state["chat"] = []
        st.session_state["messages"] = [{"role": "system", "content": "you are a thoughtful assistant. Respond to all input in 25 words and answer in korea"}]

col1, col2 = st.columns(2)
with col1:
    st.subheader("질문/답변")

    flag_start = True
    if flag_start:
        response = ask_gpt(st.session_state["messages", model])

        st.session_state["messages"] = st.session_state["messages"]+[{"role": "system", "content": response}]

        now = datetime.now().strftime("%H, %M")
        st.session_state["chat"] = st.session_state["chat"] +[("bot", now, response)]

        for sender, time, message in st.session_state["chat"]:

            if sender == "user":

                st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                st.write("")

            else:

                st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                st.write("")

with col2:
    st.subheader("버튼")


if __name__=="__main__":
    main()






