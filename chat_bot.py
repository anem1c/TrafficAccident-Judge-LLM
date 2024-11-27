from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain.chains import LLMChain
from difflib import SequenceMatcher

load_dotenv()

# 모델 설정
model = ChatOpenAI(model="gpt-4o-mini")

# FAISS 벡터 스토어 로드
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")

# 로컬에서 로드
vector_store_law = FAISS.load_local(
    'vector_store_law', embeddings, allow_dangerous_deserialization=True)
vector_store_situation = FAISS.load_local(
    'vector_store_situation', embeddings, allow_dangerous_deserialization=True)
vector_store_rate = FAISS.load_local(
    'vector_store_rate', embeddings, allow_dangerous_deserialization=True)

# 유사성 검색 리트리버 정의
retriever = vector_store_law.as_retriever(
    search_type="similarity", search_kwargs={"k": 5})

retriever1 = vector_store_situation.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})

retriever2 = vector_store_rate.as_retriever(
    search_type="similarity", search_kwargs={"k": 1})

# 프롬프트 템플릿 정의
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", '''
귀하는 교통사고 과실 비율을 판단하는 챗봇입니다.
다음으로 제공되는 context는 사용자 입력 상황과 연관된 법률이며, 이 법률을 근거로 하여 과실 비율을 판단하세요. 
    context1은 비슷한 사고에 관한 법원의 "판결문"이므로 사고 과실 비율 판단에 참고하세요.
    또한, context2는 비슷한 사고에 관한 법원에서 인정된 "과실 비율"입니다. 사고 상황에 대한 비율만 나와있을 뿐 어떤 누가 어떤 과실인지는 나와있지 않으니
    벏률을 기반으로 내린 판단과 함께 Question에 대한 과실 비율 판단에 참고하세요.

준수해야 할 규칙:
1. 사용자가 입력한 사고 상황을 이해한 후, 이해한 상황을 사용자에게 안내하세요.
2. 제공된 법률을 근거로 하여 판단해야 합니다.
3. 판결 결과를 안내하면서 동시에 실제 판레도 같이 언급하세요. (되도록 context1의 법원의 판단, context2의 과실 비율 모두 언급하세요.)
4. 판단이 올바르지 않을 가능성이 있으므로 전문가와 상의하여 보다 상세하고 신뢰할 수 있는 판단을 내릴 수 있도록 안내해 주시기 바랍니다.
5. 판단을 내려야 할 상황에서 사용자의 입장이 불확실하다면 반드시 사용자에게 확인하세요.
6. 주어진 상황에 관련된 법률에 대한 정보가 없다면 모른다고 대답하세요.
7. 만일 context2의 사고 상황이 입력된 사고 상황과 유사하지 않다고 판단된다면, 관련 사례가 없음을 안내한 뒤 context1의 판결문을 참고해 과실 비율을 판단하세요.
8. 응답을 시작할 때, 사고 상황을 겪은 사용자를 위로해주는 말로 대화를 시작하세요.
9. context2의 과실 비율에는 가해자와 피해자가 나뉘어있지 않으니, 입력된 상황에 대해 더 과실이 큰 대상을 판단한 뒤 그 대상에게 더 큰 과실 비율을 부여하세요.

주의할 규칙:
1. 사고 상황에 대해 정리할 때에는 반드시 question의 내용으로만 정리하세요.
2. 과실 비율에 대해 판단 할 때에는 기본적으로 context1과 context2의 정보 모두 "참고"하세요. (상황이 유사하지 않은 경우, 정보 없는 경우와 같은 부득이한 경우 제외)
3. context, context1, context2, question이라는 단어 자체를 언급하지 마세요.
4. 청구인, 피청구인이라는 표현을 자제하고 입력된 상황에서의 입장으로 안내하세요. (예시: 후진한 차량은 90%, 직진한 차량은 10%로 판단됩니다.)

예시 응답:
- "제공된 사고 상황에서 귀하께선 어떠한 입장이십니까?"
- "사고 상황 : 고속도로에서 갑작스럽게 후진으로 인한 사고

    가능한 과실 비율 : 귀하의 경우에는 고속도로에서 갑작스럽게 후진하셨으므로 과실 비율은 1 : 9로 귀하가 최대 1,000,000원의 합의금을 내야할 수 있습니다.

    실제 판례 : [상황] 고속도로에서의 후진으로 인한 사고 [청구인의 과실 비율] 10% [피청구인의 과실 비율] 90%"

- "죄송합니다. 사고와 관련된 법률에 대한 정보가 없기 때문에 판단이 불가능합니다."
    
응답 형태:
    
    '''),
    ("user",
    "Context: {context}\\n\\Context1: {context1}\\n\\Context2: {context2}\\n\\nQuestion: {question}")
])

class SimplePassThrough:
    def invoke(self, inputs, **kwargs):
        return inputs

class ContextToPrompt:
    def __init__(self, prompt_template):
        self.prompt_template = prompt_template

    def invoke(self, inputs):
        # 문서 내용을 텍스트로 변환
        if isinstance(inputs, list):
            context_text = "\n".join([doc.page_content for doc in inputs])
        else:
            context_text = inputs

        # 프롬프트 템플릿에 적용
        formatted_prompt = self.prompt_template.format_messages(
            context=context_text,
            question=inputs.get("question", "")
        )
        return formatted_prompt

# Retriever를 invoke() 메서드로 래핑하는 클래스 정의
class RetrieverWrapper:
    def __init__(self, retriever):
        self.retriever = retriever

    def invoke(self, inputs):
        if isinstance(inputs, dict):
            query = inputs.get("question", "")
        else:
            query = inputs
        # 검색 수행
        response_docs = self.retriever.get_relevant_documents(query)
        return response_docs

# RAG 체인 구성
rag_chain_debug = {
    "context": RetrieverWrapper(retriever),
    "context1": RetrieverWrapper(retriever1),
    'context2': RetrieverWrapper(retriever2),
    "prompt": ContextToPrompt(contextual_prompt),
    "llm": model
}

# 비슷한 상황에서 판결된 과실 비율 문서 검색
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

def run_chatbot(prompt):
    # 챗봇 구동

    # 1. Retriever로 관련 법률 검색
    response_docs = rag_chain_debug["context"].invoke({"question": query})

    # 1-1. Retriever로 관련 상황 문서 검색
    response_docs1 = rag_chain_debug["context1"].invoke({"question": query})

    # 1-2. 관련 문서와 관련된 과실 비율 문서 검색
    response_docs2 = find_most_similar_doc(
        response_docs1[0].metadata['summary'].content)

    # 2. 문서를 프롬프트로 변환
    prompt_messages = contextual_prompt.format_messages(
        context=response_docs[0].page_content,
        context1=response_docs1[0].page_content,
        context2=response_docs2.page_content,
        question=query
    )
    # 3. LLM으로 응답 생성
    response = rag_chain_debug["llm"].invoke(prompt_messages)
    return response.content 