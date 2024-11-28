from Modules.ModuleImport import *  # 모든 모듈을 불러옵니다.
from Modules.VectorStore import *
from Modules.prompt import contextual_prompt
from Modules.ContextToPrompt import ContextToPrompt
from Modules.RetrieverWrapper import RetrieverWrapper


load_dotenv()
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
now_dir = os.getcwd()

# 실시간 스트리밍을 지원하는 모델 설정
mode = openai.ChatCompletion  # OpenAI의 ChatCompletion을 사용

st.title("Chat bot test")

placeholder = st.empty()

# 벡터스토어,리트리버 잘 불러옴
# 프롬프트 템플릿 잘 불러옴

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
    

# 음성 입력을 위한 함수
def get_audio_input():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio = r.listen(source)

    # 구글 웹 음성 API로 인식하기 
    try:
        print("Google Speech : " + r.recognize_google(audio, language='ko'))
        return r.recognize_google(audio, language='ko')
    except sr.UnknownValueError as e:
        print("Google Speech ".format(e))
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

def text_to_speech(text):       # TTS 
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

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

    # RAG 체인 정의
    rag_chain_debug = {
        "context": RetrieverWrapper(retriever),
        "context1": RetrieverWrapper(retriever1),
        'context2': RetrieverWrapper(retriever2),
        "prompt": ContextToPrompt(contextual_prompt),
        "llm": mode  # mode는 이제 OpenAI의 ChatCompletion 객체
    }

    def make_rag_chain(query):
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

    

    # 메시지를 'role'과 'content'로 변환하여 전달
    with st.chat_message("assistant"):  # 답변 채팅 표시 - stream 실시간 채팅
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            # 생성된 프롬프트 메시지에 기존 대화 메시지들을 포함시킴
            messages=[
                *[
                    # 기존 대화 메시지 추가
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                *[
                    # 시스템 메시지로 모든 생성된 프롬프트 메시지 추가
                    {"role": "system", "content": make_rag_chain(query)[0].content},
                    {"role": "system", "content": make_rag_chain(query)[1].content}
                ],
            ],
            stream=True,
        )
        response = st.write_stream(stream)

        data = {"role":"assistant", "content":response}
        st.session_state.messages.append({"role":"assistant", "content":response})
        
        session_save(data)

        if isVoice:     # isVoice 파라미터에 따라 읽기
            text_to_speech(response)

if st.button("마이크"):             # 마이크 입력시 보이스 재생
    user_input = get_audio_input()
    if user_input is not None:
        text_to_speech(user_input)
        chatbot(user_input, True)

if query := st.chat_input("Say something"):        # 채팅 입력시
    chatbot(query, False)
