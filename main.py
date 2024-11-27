import streamlit as st
from streamlit_chat import message
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import Modules.speech as speech

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
now_dir = os.getcwd()

st.title("Chat bot test")

placeholder = st.empty()

def init():
    # 경로가 없으면 생성
    if not os.path.exists("History"):
        os.makedirs("History")

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "messages" not in st.session_state:  # 입력값에 대한 메시지
        st.session_state["messages"] = []
    if "active" not in st.session_state:    # 선택한 대화방
        st.session_state["active"] = ""
    if "side_data" not in st.session_state: # 사이드바에 표시하기위한 데이터
        st.session_state["side_data"] = []
    if "transcript" not in st.session_state: # 음성 번역
        st.session_state["transcript"] = ""

    # 대화내역 불러오기 위한 데이터 초기화
    if os.path.isdir(now_dir + "/History"):
        prompt_file = os.listdir(now_dir + "/History")

        prompt_file = sorted(prompt_file, key=lambda x: int(x.split('.')[0].replace("history", "")), reverse=True)

        if len(prompt_file) > 0 and len(st.session_state.side_data) == 0:
            for file in prompt_file:
                with open(now_dir + "/History/" + file, 'r', encoding='UTF8') as f:
                    json_data = json.load(f)
                    side_title = json_data[0]["content"][0:20]
                    st.session_state.side_data.append({side_title:file})
init()
print(st.session_state)

# 사이드바
with st.sidebar:
    # 대화방 추가
    if st.button("새로운 방", type="primary"):
        st.session_state["messages"] = []
        st.session_state["active"] = ""

    st.title('Chat Rooms')
    sidebar_placeholder = st.sidebar.empty() # 사이드바에 다른 요소 추가시키기 위함        
    for i, room in enumerate(st.session_state.side_data):
        for room_name, file_name in room.items():
            button_key = f"{room_name}_{file_name}{i}"  
            # 선택된 버튼 다른 타입으로 표시 (보류)
            if st.button(room_name, key=button_key):  # 각 대화방 이름을 버튼으로 출력
                st.session_state["messages"] = []
                st.session_state["active"] = now_dir + "/History/" + file_name
                with placeholder.container():
                    with open(os.path.join(now_dir, "History", file_name), 'r', encoding='UTF8') as f:
                        json_data = json.load(f)
                        for message in json_data:
                            st.session_state.messages.append({"role":message["role"], "content":message["content"]})
                            with st.chat_message(message["role"]):
                                st.write(message["content"])
                 
# 채팅 내역 session_state 저장
def session_save(data):
    now_dir = os.getcwd()
    history_dir = now_dir + "/History/"
    # History 폴더에 파일이 있는지 확인
    if os.path.isdir(history_dir):
        prompt_file = os.listdir(history_dir)
        file_cnt = len(prompt_file)+1

        file_name = "history" + str(file_cnt) + ".json"

        active = st.session_state.active
        # 첫 질문 - active 값 없음 - dump로 생성
        if active == "":
            with open(history_dir + file_name, 'w', encoding='UTF8') as f:
                json.dump([data], f)

                room_name = data["content"][0:20]
                st.session_state["active"] = f.name
                st.session_state.side_data.insert(0,{room_name:file_name})
                
                with sidebar_placeholder.container():
                    button_key = f"{room_name}_{file_name}{len(st.session_state.side_data)}"  
                    # 동적으로 버튼 추가시 - 클릭이벤트 비정상 작동 - (보류)
                    if st.button(room_name, key=button_key):  # 각 대화방 이름을 버튼으로 출력
                        print("new btn")
        # 두번째는 - session_state 값 있음 - update
        elif os.path.isfile(active):
            with open(active, 'r', encoding='UTF8') as f:
                try:
                    # 기존 대화 불러오기
                    json_data = json.load(f)
                    if not isinstance(json_data, list):
                        json_data = []  # 파일에 리스트가 없으면 초기화
                except json.JSONDecodeError:
                    json_data = []  # 파일이 비어있으면 초기화
                    
                json_data.append(data)
            with open(active, 'w', encoding='UTF8') as f:
                json.dump(json_data, f)
    

def chatbot(prompt, isVoice):
    # 기본 메시지 화면에 표시
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    data = {"role":"user", "content":prompt}
    st.session_state.messages.append(data)
    session_save(data)

    with st.chat_message("user"):  # 사용자 채팅 표시
        st.write(prompt)
    
    with st.chat_message("assistant"):      # 답변 채팅 표시 - stream 실시간 채팅
        stream = client.chat.completions.create(
            model = st.session_state["openai_model"],
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream = True,
        )
        response = st.write_stream(stream)

        data = {"role":"assistant", "content":response}
        st.session_state.messages.append({"role":"assistant", "content":response})
        
        session_save(data)
        
        if isVoice:     # isVoice 파라미터에 따라 읽기
            speech.text_to_speech(response)

if st.button("마이크"):             # 마이크 입력시 보이스 재생
    user_input = speech.get_audio_input()
    if user_input is not None:
        chatbot(user_input, True)

if prompt := st.chat_input("Say something"):        # 채팅 입력시
    chatbot(prompt, False)


