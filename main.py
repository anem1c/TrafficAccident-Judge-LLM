import streamlit as st
import os
from pages.chatbot_main import chatbot_main
from pages.image_main import image_main
from streamlit_option_menu import option_menu

def init():
    # 경로가 없으면 생성
    if not os.path.exists("History"):
        os.makedirs("History")

    # session_state 변수 초기화
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o-mini"
    if "messages" not in st.session_state:  # 입력값에 대한 메시지
        st.session_state["messages"] = []
    if "active" not in st.session_state:    # 선택한 대화방
        st.session_state["active"] = ""
    if "side_data" not in st.session_state: # 사이드바에 표시하기위한 데이터
        st.session_state["side_data"] = []
    if 'rerun' not in st.session_state:
        st.session_state["rerun"] = False
    if 'menu' not in st.session_state:
        st.session_state["menu"] = ""

# streamlit 기본 설정버튼 비활성화
st.markdown(
    """
    <style>
        div[data-testid="stToolbar"] {
            display:none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.title("🚘 과시리")

# 사이드바
with st.sidebar:
    def on_change(key):
        st.session_state["menu"] = key

    selected = option_menu(None, ["홈", '차량 파손 이미지'], 
        icons=['house', 'camera'], menu_icon="cast", key="menu_key", default_index=0, on_change=on_change)

init()

# 메뉴클릭시 호출할 함수
menu_dict = {
    "홈" : {"fn": chatbot_main},
    "차량 파손 이미지" : {"fn": image_main},
}
# menu_key 값이 바뀔 경우 페이지 변경
if 'menu_key' in st.session_state and st.session_state["menu_key"]:
    menu_dict[st.session_state["menu_key"]]["fn"]()
else:
    chatbot_main()    
