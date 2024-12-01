# 교통사고 과실 비율 챗봇
> [교통사고 주요 판례](https://xn--vb0b6f546cmsg6pn.com/sub/preced/preced01.asp)와 [교통사고 과실 비율](https://accident.knia.or.kr/example1#0) 학습을 통하여 사용자의 입력을 통해 사고상황 요약 및 과실을 책정해주는 챗봇입니다.


[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]

---

파손된 차량의 이미지를 분석해주는 기능도 추가되었습니다.

![TrafficAccident_Demo-ezgif com-optimize](https://github.com/user-attachments/assets/1afac55a-580a-4d42-b8b2-9ca599dd8d97)


## 실행 가이드

```sh
git clone https://github.com/anem1c/TrafficAccident-Judge-LLM.git

pip install -r requirements.txt
```

```sh
streamlit run main.py
```

## 사용 예시

작동 영상

## 업데이트 사항

* 0.2.1
    * CHANGE: Update docs (module code remains unchanged)
* 0.2.0
    * CHANGE: Remove `setDefaultXYZ()`
    * ADD: Add `init()`
* 0.1.1
    * FIX: Crash when calling `baz()` (Thanks @GenerousContributorName!)
* 0.1.0
    * The first proper release
    * CHANGE: Rename `foo()` to `bar()`
* 0.0.1
    * Work in progress

## Meta

Your Name – [@YourTwitter](https://twitter.com/dbader_org) – YourEmail@example.com

Distributed under the XYZ license. See ``LICENSE`` for more information.

[https://github.com/yourname/github-link](https://github.com/dbader/)

## 트러블 슈팅

1. Fork it (<https://github.com/yourname/yourproject/fork>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
