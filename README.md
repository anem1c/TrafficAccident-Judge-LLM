# 교통사고 과실 비율 챗봇 (임시)

---

![](https://media2.dev.to/dynamic/image/width=800%2Cheight=%2Cfit=scale-down%2Cgravity=auto%2Cformat=auto/https%3A%2F%2Fdev-to-uploads.s3.amazonaws.com%2Fuploads%2Farticles%2Fkoksetkyx7t6m69m5rcr.png)

## 1. branch

```
main, develop, feature 브랜치가 있습니다! 각자 feature 에서 구현중인,구현하고 싶은 기능을
feature/~~~ <- 만드시면 됩니다!

< 예진님 코드는 뼈대가 되는 코드이므로 현재 develop 브랜치에 있습니다. >
< 창규님이 개발중이신 streamlit 은 feature/streamlit에 업로드하시면 테스트한 뒤 develop에 merge 하곘습니다>
```

예시로 음성인식 기능을 구현할 거라면 
> feature/음성인식

으로 branch 생성하여 작업하시면 됩니다!

### 요약

1. 각자 feature에서 개발을 하고
2. 개발 완료될 때마다 각자 develop으로 pull request해서 합치기
3. develop에서 main으로 갈 때는 큰 기능 다 완성되면 테스트 후에 pull request해서 합치기


- main
  
    최종 프로젝트 branch입니다. 저희는 배포 이후 서비스를 이어나가는 프로젝트가 아니므로
  
    최종적인 결과물, *develop* 브랜치 에서 완성된 것을 기준으로 업로드합니다.

- develop
  
    최종 main에 올리기 전 테스트용 브랜치입니다. 

- feature
  
    실제 개발할 때 쓰는 브랜치입니다.
    구현중인 작업들 *branch* 입니다. ex ) 이미지, streamlit 등

## 2. 환경 -> requirements.txt

    환경 및 버젼 통일은 데모 버젼 완성 이후 대표자가 테스트 한 뒤 모든 팀원이 클론하여
    정상 동작 확인 후 해당 환경으로 통일할 예정입니다!