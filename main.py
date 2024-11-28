from Modules.ModuleImport import *  # 모든 모듈을 불러옵니다.
from Modules.VectorStore import *
from Modules.prompt import contextual_prompt
from Modules.ContextToPrompt import ContextToPrompt
from Modules.RetrieverWrapper import RetrieverWrapper
import Modules.Speech as Speech

load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
now_dir = os.getcwd()
chat_model = ChatOpenAI(model="gpt-4o-mini")

# 실시간 스트리밍을 지원하는 모델 설정
# mode = openai.ChatCompletion  # OpenAI의 ChatCompletion을 사용

st.title("교통사고 과실 비율 챗봇")

placeholder = st.empty()

class SimplePassThrough:
    def invoke(self, inputs, **kwargs):
        return inputs


def find_most_similar_doc(user_accident):
    """
    사용자가 제공한 사고 정보와 가장 유사한 문서를 FAISS 벡터 스토어에서 검색합니다.

    Args:
        user_accident (str): 사용자가 입력한 사고 상황 텍스트.
        vector_store (FAISS): FAISS 벡터 스토어 객체.
        embeddings (OpenAIEmbeddings): 임베딩 모델 객체.

    Returns:
        dict: 가장 유사한 문서의 정보 (텍스트와 메타데이터).
    """
    # 사용자 입력 텍스트의 임베딩 계산
    query_embedding = embeddings.embed_query(user_accident)

    # 벡터 DB에서 유사한 문서 검색
    search_results = vector_store_rate.similarity_search_by_vector(
        query_embedding, k=1)

    # 결과 반환 (가장 유사한 문서 1개)
    if search_results:
        return search_results[0]  # 첫 번째 결과 반환
    else:
        return None  # 검색 결과가 없을 경우

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
    if 'rerun' not in st.session_state:
        st.session_state.rerun = False

    # 대화내역 불러오기 위한 데이터 초기화
    if os.path.isdir(now_dir + "/History"):
        prompt_file = os.listdir(now_dir + "/History")

        prompt_file = sorted(prompt_file, key=lambda x: int(x.split('.')[0].replace("history", "")), reverse=True)

        if len(prompt_file) > 0 and len(st.session_state.side_data) == 0:
            for file in prompt_file:
                with open(now_dir + "/History/" + file, 'r', encoding='UTF8') as f:
                    json_data = json.load(f)
                    side_title = json_data[0]["content"][0:10]
                    st.session_state.side_data.append({side_title:file})
init()

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
            cols = st.columns([4, 1])  # 버튼과 작업 버튼을 나누기 위해 컬럼 사용
            with cols[0]:
                # type - 선택된 버튼 다른 타입으로 표시 (보류)
                if st.button(room_name, key=f"{room_name}_{file_name}{i}"):  # 각 대화방 이름을 버튼으로 출력
                    st.session_state["messages"] = []
                    st.session_state["active"] = file_name
                    with placeholder.container():
                        with open(os.path.join(now_dir, "History", file_name), 'r', encoding='UTF8') as f:
                            json_data = json.load(f)
                            for message in json_data:
                                st.session_state.messages.append({"role":message["role"], "content":message["content"]})
                                with st.chat_message(message["role"]):
                                    st.write(message["content"])
            with cols[1]:
                if st.button("🗑️", key=f"delete_{room_name}_{i}"):
                    # 삭제 로직
                    file_path = os.path.join("History", file_name)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    del st.session_state["side_data"][i]

                    if file_name == st.session_state["active"]:
                        st.session_state["messages"] = []
                        st.session_state["active"] = ""

                    st.session_state["rerun"] = True

if st.session_state["rerun"]:
    print("rerun")
    st.session_state["rerun"] = False
    st.rerun()

# 채팅 내역 session_state 저장
def session_save(data):
    now_dir = os.getcwd()
    history_dir = now_dir + "/History/"
    # History 폴더에 파일이 있는지 확인
    if os.path.isdir(history_dir):
        prompt_file = os.listdir(history_dir)

        # 마지막 파일을 기준으로 넘버링
        sorted_file_list = natsort.natsorted(prompt_file)
        if len(sorted_file_list) > 0:
            last_file = sorted_file_list[len(sorted_file_list)-1].split(".")[0]
            file_cnt = int(last_file.replace("history", "")) + 1
        else:
            file_cnt = 1

        file_name = "history" + str(file_cnt) + ".json"

        active = st.session_state.active
        active_file = now_dir + "/History/" + active 

        # 첫 질문 - active 값 없음 - dump로 생성
        if active == "":
            with open(history_dir + file_name, 'w', encoding='UTF8') as f:
                json.dump([data], f)

                room_name = data["content"][0:10]
                st.session_state["active"] = file_name
                st.session_state.side_data.insert(0,{room_name:file_name})
                
                with sidebar_placeholder.container():
                    button_key = f"{room_name}_{file_name}{len(st.session_state.side_data)}"  
                    # 동적으로 버튼 추가시 - 클릭이벤트 비정상 작동 - (보류)
                    if st.button(room_name, key=button_key):  # 각 대화방 이름을 버튼으로 출력
                        st.session_state["rerun"] = True
                        print("new btn")
        # 두번째는 - session_state 값 있음 - update
        elif os.path.isfile(active_file):
            with open(active_file, 'r', encoding='UTF8') as f:
                try:
                    # 기존 대화 불러오기
                    json_data = json.load(f)
                    if not isinstance(json_data, list):
                        json_data = []  # 파일에 리스트가 없으면 초기화
                except json.JSONDecodeError:
                    json_data = []  # 파일이 비어있으면 초기화
                    
                json_data.append(data)
            with open(active_file, 'w', encoding='UTF8') as f:
                json.dump(json_data, f)

def make_rag_chain(query):
        # RAG 체인 정의
    rag_chain_debug = {
        "context": RetrieverWrapper(retriever),
        "context1": RetrieverWrapper(retriever1),
        'context2': RetrieverWrapper(retriever2),
        "prompt": ContextToPrompt(contextual_prompt),
        "llm": chat_model  # mode는 이제 OpenAI의 ChatCompletion 객체
    }

    # 1. 검색 단계: context, context1, context2로부터 관련 정보 검색
    response_docs = rag_chain_debug["context"].invoke({"question": query})
    response_docs1 = rag_chain_debug["context1"].invoke({"question": query})
    response_docs2 = find_most_similar_doc(
        response_docs1[0].metadata['summary'].content)

    # 'contextual_prompt'를 사용하여 프롬프트를 생성합니다.
    prompt_messages = contextual_prompt.format_messages(
        context=response_docs,  # 검색된 context 데이터
        context1=response_docs1,  # 검색된 context1 데이터
        context2=response_docs2,  # 검색된 context2 데이터
        question=query  # 사용자의 질문
    )
    return prompt_messages

def chatbot(query, isVoice):
    # 기본 메시지 화면에 표시
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    data = {"role": "user", "content": query}
    st.session_state.messages.append(data)
    session_save(data)

    with st.chat_message("user"):  # 사용자 채팅 표시
        st.write(query)
    
    # 메시지를 'role'과 'content'로 변환하여 전달
    with st.chat_message("assistant"):  # 답변 채팅 표시 - stream 실시간 채팅
        prompt_message = make_rag_chain(query)
        llm_response = chat_model.invoke(prompt_message)
        response = llm_response.content
        print(response)
        st.write(response)

        # stream = client.chat.completions.create(
        #     model=st.session_state["openai_model"],
        #     messages = [
        #         {"role": m["role"], "content": m["content"]}
        #         for m in st.session_state.messages
        #     ],
        #     stream=True,
        # )
        # response = st.write_stream(stream)

        data = {"role":"assistant", "content":response}
        st.session_state.messages.append({"role":"assistant", "content":response})
        
        session_save(data)

        if isVoice:     # isVoice 파라미터에 따라 읽기
            Speech.text_to_speech(response)

if st.button("마이크"):             # 마이크 입력시 보이스 재생
    user_input = Speech.get_audio_input()
    if user_input is not None:
        chatbot(user_input, True)

if query := st.chat_input("메시지를 입력해주세요 "):        # 채팅 입력시
    chatbot(query, False)
