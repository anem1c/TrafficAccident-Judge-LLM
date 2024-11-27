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