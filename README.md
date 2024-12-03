# 🚘 과시리 (교통사고 과실 비율 챗봇)

> [교통사고 주요 판례](https://xn--vb0b6f546cmsg6pn.com/sub/preced/preced01.asp) 와 [교통사고 과실 비율](https://accident.knia.or.kr/example1#0) 학습을 통하여 사용자의 입력을 통해 사고상황 요약 및 과실을 책정해주는 챗봇

<div align="left">
    <img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=OpenAI&logoColor=white"/>
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white">
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white">
</div>


![ezgif-4-7b23355265](https://github.com/user-attachments/assets/76244717-c0d3-417c-ab2c-47fff863fb79)

## 📖 목차

- [🚘 과시리 (교통사고 과실 비율 챗봇)](#-과시리-교통사고-과실-비율-챗봇)
  - [📖 목차](#-목차)
  - [✅ 이럴 때 사용해보세요!](#-이럴-때-사용해보세요)
  - [💾 파일 구조](#-파일-구조)
  - [🏃‍♂️ 실행 가이드](#️-실행-가이드)
  - [📈 프로젝트 진행 요약 및 업데이트 사항](#-프로젝트-진행-요약-및-업데이트-사항)
  - [🥅 트러블 슈팅](#-트러블-슈팅)
  - [✍️ 회고](#️-회고)





## ✅ 이럴 때 사용해보세요!
  * 교통사고 상황에 따른 과실 비율이 궁금할 때
  * 사고 차량 파손 부위가 궁금할 때

## 💾 파일 구조
<details>
<div markdown="1">

📦TrafficAccident-Judge-LLM
 ┣ 📂.git
 ┣ 📂.streamlit
 ┃ ┗ 📜config.toml
 ┣ 📂Modules
 ┃ ┣ 📂__pycache__
 ┃ ┣ 📜ContextToPrompt.py
 ┃ ┣ 📜ImageDetect.py
 ┃ ┣ 📜ModuleImport.py
 ┃ ┣ 📜RetrieverWrapper.py
 ┃ ┣ 📜Speech.py
 ┃ ┣ 📜VectorStore.py
 ┃ ┗ 📜prompt.py
 ┣ 📂Resources
 ┃ ┣ 📂pdf_files
 ┃ ┣ 📂vector_store_law
 ┃ ┃ ┣ 📜index.faiss
 ┃ ┃ ┗ 📜index.pkl
 ┃ ┣ 📂vector_store_rate
 ┃ ┃ ┣ 📜index.faiss
 ┃ ┃ ┗ 📜index.pkl
 ┃ ┣ 📂vector_store_situation
 ┃ ┃ ┣ 📜index.faiss
 ┃ ┃ ┗ 📜index.pkl
 ┃ ┣ 📜231107_과실비율인정기준_온라인용.pdf
 ┃ ┣ 📜accident_data_all_pages.json
 ┃ ┣ 📜best.onnx
 ┃ ┣ 📜crawling_1.ipynb
 ┃ ┣ 📜crawling_2.ipynb
 ┃ ┗ 📜vector-store.ipynb
 ┣ 📂__pycache__
 ┣ 📂vector_store_rate
 ┃ ┣ 📜index.faiss
 ┃ ┗ 📜index.pkl
 ┣ 📜.DS_Store
 ┣ 📜.env
 ┣ 📜.gitignore
 ┣ 📜image_demo.py
 ┣ 📜main.py
 ┗ 📜requirements.txt
</div>
</details>



## 🏃‍♂️ 실행 가이드
```sh
git clone https://github.com/anem1c/TrafficAccident-Judge-LLM.git

cd TrafficAccident-Judge-LLM

pip install -r requirements.txt
```

```sh
streamlit run main.py
```

## 📈 프로젝트 진행 요약 및 업데이트 사항
* 2024-11-20 프로젝트 시작
* 2024-11-21 Streamlit 데모 구현 및 챗봇 구현
* 2024-11-22 vectorDB 로컬 호출 & 챗봇 Streamlit 통합
* 2024-11-25 기능 별 모듈화 진행
* 2024-11-26 파손된 차량의 이미지를 분석해주는 기능 추가
* 2024-11-27 프롬프트 개선
* 2024-11-28 차량 파손 이미지 요약 및 분석 기능 추가
    
    ![TrafficAccident_Demo-ezgif com-optimize](https://github.com/user-attachments/assets/1afac55a-580a-4d42-b8b2-9ca599dd8d97)

* 2024-12-01 기능 별 사이드바 페이지 분리



## 🥅 트러블 슈팅

* 음성 재생중 새로고침시 재생중인 음성이 중지되게 하고 싶었지만 streamlit lifecycle 추적 방법을 찾지못함
* rag 체인에 모델 입력까지 넣을 때 stream 형식으로 보여줄 수 없는 문제
* rag 체인 형식을 수정해 모델 입력은 따로 받아 stream으로 진행 가능하도록 수정 


## ✍️ 회고

[이시헌](https://github.com/anem1c) – PM
> 첫 팀 프로젝트로써 팀장을 맡게 되어 기뻤습니다. 문서 정리, git 이슈 및 에러 핸들링에서 많은 어려움이 있었지만, 하나 하나 해결해나가면서 프로젝트를 완성시켜갈 때 느껴지는 행복감이 잊혀지지 않습니다.

[최창규](https://github.com/choichangkyu) – PL
> streamlit 위주로 개발했는데 커스텀이 안되다 보니까 상당히 답답했구요. 팀원분들이 너무 잘해주시고 소통이 잘돼서 재밌었습니다.

[한예진](https://github.com/yejingksdpwls) – PE
> 초반에는 열정이 넘쳤었던 저였지만, 후반으로 갈 수록 스스로 느껴질 정도로 열정이 떨어진 모습에 제 자신에게 아쉬웠습니다. 하지만 모든 팀원 분들이 열심히 해주시고 부족한 부분들을 잘 채워주셔서 재밌고 만족스럽게 프로젝트를 마무리 할 수 있었던 것 같습니다.

[이명혜](https://github.com/LeeMyunghye) – QA

