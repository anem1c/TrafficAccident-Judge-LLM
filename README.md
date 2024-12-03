# 교통사고 과실 비율 챗봇

2024-11-20 ~ 2024-12-04

> [교통사고 주요 판례](https://xn--vb0b6f546cmsg6pn.com/sub/preced/preced01.asp) 와 [교통사고 과실 비율](https://accident.knia.or.kr/example1#0) 학습을 통하여 사용자의 입력을 통해 사고상황 요약 및 과실을 책정해주는 챗봇

<div align="left">
    <img src="https://img.shields.io/badge/OpenAI-412991?style=flat&logo=OpenAI&logoColor=white"/>
    <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white">
    <img src="https://img.shields.io/badge/Python-3776AB?style=flat&logo=Python&logoColor=white">
</div>


## 목차

## 파일 구조
<details>
<div markdown="1">

📦TrafficAccident-Judge-LLM
 ┣ 📂.git
 ┃ ┣ 📂hooks
 ┃ ┃ ┣ 📜applypatch-msg.sample
 ┃ ┃ ┣ 📜commit-msg.sample
 ┃ ┃ ┣ 📜fsmonitor-watchman.sample
 ┃ ┃ ┣ 📜post-update.sample
 ┃ ┃ ┣ 📜pre-applypatch.sample
 ┃ ┃ ┣ 📜pre-commit.sample
 ┃ ┃ ┣ 📜pre-merge-commit.sample
 ┃ ┃ ┣ 📜pre-push.sample
 ┃ ┃ ┣ 📜pre-rebase.sample
 ┃ ┃ ┣ 📜pre-receive.sample
 ┃ ┃ ┣ 📜prepare-commit-msg.sample
 ┃ ┃ ┣ 📜push-to-checkout.sample
 ┃ ┃ ┣ 📜sendemail-validate.sample
 ┃ ┃ ┗ 📜update.sample
 ┃ ┣ 📂info
 ┃ ┃ ┗ 📜exclude
 ┃ ┣ 📂logs
 ┃ ┃ ┣ 📂refs
 ┃ ┃ ┃ ┣ 📂heads
 ┃ ┃ ┃ ┃ ┣ 📜develop
 ┃ ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┃ ┗ 📂remotes
 ┃ ┃ ┃ ┃ ┗ 📂origin
 ┃ ┃ ┃ ┃ ┃ ┣ 📜HEAD
 ┃ ┃ ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┗ 📜HEAD
 ┃ ┣ 📂objects
 ┃ ┃ ┣ 📂c4
 ┃ ┃ ┃ ┗ 📜6a26f28f1968136a99ca09231db4a1a5b7f5a5
 ┃ ┃ ┣ 📂f9
 ┃ ┃ ┃ ┗ 📜7456a3a9872842a223a1444ca6e49bb0eab4dd
 ┃ ┃ ┣ 📂ff
 ┃ ┃ ┃ ┗ 📜2f69bd21a3e0b4975b9511724ce5fed2cfb159
 ┃ ┃ ┣ 📂info
 ┃ ┃ ┗ 📂pack
 ┃ ┃ ┃ ┣ 📜pack-3a27b503cdd27c62b8045dd0eea8a9edc37e66d5.idx
 ┃ ┃ ┃ ┣ 📜pack-3a27b503cdd27c62b8045dd0eea8a9edc37e66d5.pack
 ┃ ┃ ┃ ┗ 📜pack-3a27b503cdd27c62b8045dd0eea8a9edc37e66d5.rev
 ┃ ┣ 📂refs
 ┃ ┃ ┣ 📂heads
 ┃ ┃ ┃ ┣ 📜develop
 ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┣ 📂remotes
 ┃ ┃ ┃ ┗ 📂origin
 ┃ ┃ ┃ ┃ ┣ 📜HEAD
 ┃ ┃ ┃ ┃ ┗ 📜main
 ┃ ┃ ┗ 📂tags
 ┃ ┣ 📜COMMIT_EDITMSG
 ┃ ┣ 📜FETCH_HEAD
 ┃ ┣ 📜HEAD
 ┃ ┣ 📜config
 ┃ ┣ 📜description
 ┃ ┣ 📜index
 ┃ ┗ 📜packed-refs
 ┣ 📂.streamlit
 ┃ ┗ 📜config.toml
 ┣ 📂History
 ┃ ┣ 📜history16.json
 ┃ ┣ 📜history17.json
 ┃ ┣ 📜history18.json
 ┃ ┗ 📜history19.json
 ┣ 📂Modules
 ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜ContextToPrompt.cpython-311.pyc
 ┃ ┃ ┣ 📜ImageDetect.cpython-311.pyc
 ┃ ┃ ┣ 📜ModuleImport.cpython-311.pyc
 ┃ ┃ ┣ 📜RetrieverWrapper.cpython-311.pyc
 ┃ ┃ ┣ 📜Speech.cpython-311.pyc
 ┃ ┃ ┣ 📜VectorStore.cpython-311.pyc
 ┃ ┃ ┗ 📜prompt.cpython-311.pyc
 ┃ ┣ 📜ContextToPrompt.py
 ┃ ┣ 📜ImageDetect.py
 ┃ ┣ 📜ModuleImport.py
 ┃ ┣ 📜RetrieverWrapper.py
 ┃ ┣ 📜Speech.py
 ┃ ┣ 📜VectorStore.py
 ┃ ┗ 📜prompt.py
 ┣ 📂Resources
 ┃ ┣ 📂pdf_files
 ┃ ┃ ┣ 📜2013가합15831_판결문_검수완료.pdf
 ┃ ┃ ┣ 📜2013가합18908_판결문_검수완료.pdf
 ┃ ┃ ┣ 📜2013나6636.pdf
 ┃ ┃ ┣ 📜2014가단5297401.pdf
 ┃ ┃ ┣ 📜2014나101062.pdf
 ┃ ┃ ┣ 📜2014나10885.pdf
 ┃ ┃ ┣ 📜2014나7827.pdf
 ┃ ┃ ┣ 📜2015__819.pdf
 ┃ ┃ ┣ 📜2015나304202 손해배상(자) (151127).pdf
 ┃ ┃ ┣ 📜2015나9736 채무부존재확인.pdf
 ┃ ┃ ┣ 📜2016노186_판결문.pdf
 ┃ ┃ ┣ 📜[민사]수원지방법원(2016나50686).pdf
 ┃ ┃ ┣ 📜page_1_file_17.pdf
 ┃ ┃ ┣ 📜page_1_file_18.pdf
 ┃ ┃ ┣ 📜page_1_file_19.pdf
 ┃ ┃ ┣ 📜page_1_file_20.pdf
 ┃ ┃ ┣ 📜page_1_file_21.pdf
 ┃ ┃ ┣ 📜page_1_file_22.pdf
 ┃ ┃ ┣ 📜page_1_file_23.pdf
 ┃ ┃ ┣ 📜page_1_file_24.pdf
 ┃ ┃ ┣ 📜page_1_file_25.pdf
 ┃ ┃ ┣ 📜page_2_file_1.pdf
 ┃ ┃ ┣ 📜page_2_file_10.pdf
 ┃ ┃ ┣ 📜page_2_file_11.pdf
 ┃ ┃ ┣ 📜page_2_file_12.pdf
 ┃ ┃ ┣ 📜page_2_file_13.pdf
 ┃ ┃ ┣ 📜page_2_file_14.pdf
 ┃ ┃ ┣ 📜page_2_file_15.pdf
 ┃ ┃ ┣ 📜page_2_file_16.pdf
 ┃ ┃ ┣ 📜page_2_file_18.pdf
 ┃ ┃ ┣ 📜page_2_file_19.pdf
 ┃ ┃ ┣ 📜page_2_file_2.pdf
 ┃ ┃ ┣ 📜page_2_file_20.pdf
 ┃ ┃ ┣ 📜page_2_file_21.pdf
 ┃ ┃ ┣ 📜page_2_file_22.pdf
 ┃ ┃ ┣ 📜page_2_file_23.pdf
 ┃ ┃ ┣ 📜page_2_file_24.pdf
 ┃ ┃ ┣ 📜page_2_file_25.pdf
 ┃ ┃ ┣ 📜page_2_file_3.pdf
 ┃ ┃ ┣ 📜page_2_file_4.pdf
 ┃ ┃ ┣ 📜page_2_file_5.pdf
 ┃ ┃ ┣ 📜page_2_file_6.pdf
 ┃ ┃ ┣ 📜page_2_file_7.pdf
 ┃ ┃ ┣ 📜page_2_file_9.pdf
 ┃ ┃ ┣ 📜page_3_file_1.pdf
 ┃ ┃ ┣ 📜page_3_file_10.pdf
 ┃ ┃ ┣ 📜page_3_file_11.pdf
 ┃ ┃ ┣ 📜page_3_file_12.pdf
 ┃ ┃ ┣ 📜page_3_file_13.pdf
 ┃ ┃ ┣ 📜page_3_file_14.pdf
 ┃ ┃ ┣ 📜page_3_file_15.pdf
 ┃ ┃ ┣ 📜page_3_file_16.pdf
 ┃ ┃ ┣ 📜page_3_file_17.pdf
 ┃ ┃ ┣ 📜page_3_file_18.pdf
 ┃ ┃ ┣ 📜page_3_file_19.pdf
 ┃ ┃ ┣ 📜page_3_file_2.pdf
 ┃ ┃ ┣ 📜page_3_file_20.pdf
 ┃ ┃ ┣ 📜page_3_file_21.pdf
 ┃ ┃ ┣ 📜page_3_file_22.pdf
 ┃ ┃ ┣ 📜page_3_file_23.pdf
 ┃ ┃ ┣ 📜page_3_file_24.pdf
 ┃ ┃ ┣ 📜page_3_file_25.pdf
 ┃ ┃ ┣ 📜page_3_file_3.pdf
 ┃ ┃ ┣ 📜page_3_file_4.pdf
 ┃ ┃ ┣ 📜page_3_file_5.pdf
 ┃ ┃ ┣ 📜page_3_file_6.pdf
 ┃ ┃ ┣ 📜page_3_file_7.pdf
 ┃ ┃ ┣ 📜page_3_file_8.pdf
 ┃ ┃ ┣ 📜page_3_file_9.pdf
 ┃ ┃ ┣ 📜page_4_file_1.pdf
 ┃ ┃ ┣ 📜page_4_file_10.pdf
 ┃ ┃ ┣ 📜page_4_file_11.pdf
 ┃ ┃ ┣ 📜page_4_file_12.pdf
 ┃ ┃ ┣ 📜page_4_file_13.pdf
 ┃ ┃ ┣ 📜page_4_file_14.pdf
 ┃ ┃ ┣ 📜page_4_file_15.pdf
 ┃ ┃ ┣ 📜page_4_file_16.pdf
 ┃ ┃ ┣ 📜page_4_file_17.pdf
 ┃ ┃ ┣ 📜page_4_file_18.pdf
 ┃ ┃ ┣ 📜page_4_file_19.pdf
 ┃ ┃ ┣ 📜page_4_file_2.pdf
 ┃ ┃ ┣ 📜page_4_file_20.pdf
 ┃ ┃ ┣ 📜page_4_file_21.pdf
 ┃ ┃ ┣ 📜page_4_file_22.pdf
 ┃ ┃ ┣ 📜page_4_file_23.pdf
 ┃ ┃ ┣ 📜page_4_file_24.pdf
 ┃ ┃ ┣ 📜page_4_file_25.pdf
 ┃ ┃ ┣ 📜page_4_file_3.pdf
 ┃ ┃ ┣ 📜page_4_file_4.pdf
 ┃ ┃ ┣ 📜page_4_file_5.pdf
 ┃ ┃ ┣ 📜page_4_file_6.pdf
 ┃ ┃ ┣ 📜page_4_file_7.pdf
 ┃ ┃ ┣ 📜page_4_file_8.pdf
 ┃ ┃ ┣ 📜page_4_file_9.pdf
 ┃ ┃ ┣ 📜page_5_file_10.pdf
 ┃ ┃ ┣ 📜page_5_file_11.pdf
 ┃ ┃ ┣ 📜page_5_file_12.pdf
 ┃ ┃ ┣ 📜page_5_file_13.pdf
 ┃ ┃ ┣ 📜page_5_file_14.pdf
 ┃ ┃ ┣ 📜page_5_file_15.pdf
 ┃ ┃ ┣ 📜page_5_file_16.pdf
 ┃ ┃ ┣ 📜page_5_file_17.pdf
 ┃ ┃ ┣ 📜page_5_file_18.pdf
 ┃ ┃ ┣ 📜page_5_file_2.pdf
 ┃ ┃ ┣ 📜page_5_file_21.pdf
 ┃ ┃ ┣ 📜page_5_file_22.pdf
 ┃ ┃ ┣ 📜page_5_file_23.pdf
 ┃ ┃ ┣ 📜page_5_file_24.pdf
 ┃ ┃ ┣ 📜page_5_file_25.pdf
 ┃ ┃ ┣ 📜page_5_file_3.pdf
 ┃ ┃ ┣ 📜page_5_file_4.pdf
 ┃ ┃ ┣ 📜page_5_file_5.pdf
 ┃ ┃ ┣ 📜page_5_file_6.pdf
 ┃ ┃ ┣ 📜page_5_file_7.pdf
 ┃ ┃ ┣ 📜page_5_file_8.pdf
 ┃ ┃ ┣ 📜page_5_file_9.pdf
 ┃ ┃ ┣ 📜page_6_file_1.pdf
 ┃ ┃ ┣ 📜대구지방법원2016_나09440판결.pdf
 ┃ ┃ ┣ 📜대구지방법원_2014가단53940.pdf
 ┃ ┃ ┣ 📜대구지방법원_2014나305420.pdf
 ┃ ┃ ┣ 📜대구지법2015나306505.pdf
 ┃ ┃ ┣ 📜서울고등법원 2015나2008818.pdf
 ┃ ┃ ┣ 📜서울동부지방법원2014가단32855.pdf
 ┃ ┃ ┣ 📜서울중앙지방법원_2014가단25076.pdf
 ┃ ┃ ┣ 📜서울중앙지방법원_2014가단5094121.pdf
 ┃ ┃ ┗ 📜울산지방법원 2014나5289.pdf
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
 ┃ ┗ 📜image_demo.cpython-311.pyc
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


## 이렇게 사용하세요 !

( 대충 챗봇 질문 넣고 답변 받는 GIF)



## 실행 가이드
```sh
git clone https://github.com/anem1c/TrafficAccident-Judge-LLM.git

cd TrafficAccident-Judge-LLM

pip install -r requirements.txt
```

```sh
streamlit run main.py
```

## 사용 예시

작동 영상

## 프로젝트 진행 요약 및 업데이트 사항
* 2024-11-20 프로젝트 시작
* 2024-11-21 Streamlit 데모 구현 및 챗봇 구현
* 2024-11-22 vectorDB 로컬 호출 & 챗봇 Streamlit 통합
* 2024-11-25 기능 별 모듈화 진행
* 2024-11-26 파손된 차량의 이미지를 분석해주는 기능 추가
* 2024-11-27 프롬프트 개선
* 2024-11-28 차량 파손 이미지 요약 및 분석 기능 추가
    
    ![TrafficAccident_Demo-ezgif com-optimize](https://github.com/user-attachments/assets/1afac55a-580a-4d42-b8b2-9ca599dd8d97)

* 2024-12-01 기능 별 사이드바 페이지 분리



## 트러블 슈팅

## 회고

> 팀 프로젝트로써 깃 충돌이 많이 일어나 관리에 시간을 많이 들임.
> 기존 코드에서 

## 맴버

이시헌 – [@](https://twitter.com/dbader_org)

최창규 – [@YourTwitter](https://twitter.com/dbader_org)

한예진 – [@YourTwitter](https://twitter.com/dbader_org)

이명혜 – [@YourTwitter](https://twitter.com/dbader_org)

