# Retriever를 invoke() 메서드로 래핑하는 클래스 정의

def retriever__init__(self, retriever):
    self.retriever = retriever

def retriever_invoke(self, inputs):
    if isinstance(inputs, dict):
        query = inputs.get("question", "")
    else:
        query = inputs
    # 검색 수행
    response_docs = self.retriever.get_relevant_documents(query)
    return response_docs