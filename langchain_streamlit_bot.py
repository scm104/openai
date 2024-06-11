import os
import streamlit as st
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOpenAI

# Streamlit 앱 타이틀 설정
st.title("Document QA with LangChain and OpenAI")
st.write("PDF 문서를 불러와서 질문에 답변하는 시스템입니다.")

# OpenAI API Key 입력 받기
openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.warning("OpenAI API 키를 입력하세요.")
    st.stop()

# PDF 문서 로드 및 벡터 스토어 생성
@st.cache_data
def load_documents():
    pdf_loader = DirectoryLoader('.', glob="*.pdf")
    documents = pdf_loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_documents(documents)
    return texts

texts = load_documents()

# OpenAI 임베딩 초기화
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)
vectordb = Chroma.from_documents(documents=texts, embedding=embedding)
retriever = vectordb.as_retriever()

# QA 체인 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model_name="gpt-4o", temperature=0, openai_api_key=openai_api_key),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 세션 상태 초기화
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# 사용자 입력 받기
input_text = st.text_input("질문을 입력하세요:")
if st.button("전송") and input_text:
    chatbot_response = qa_chain.invoke(input_text)
    st.session_state.chat_history.append({"user": input_text, "bot": chatbot_response['result'].strip()})
    st.session_state.input_text = ""

# 채팅 내역 표시
st.write("### 채팅 내역")
for chat in st.session_state.chat_history:
    st.write(f"**User:** {chat['user']}")
    st.write(f"**Bot:** {chat['bot']}")
    st.write("---")
