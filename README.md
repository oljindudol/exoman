엑조디아 관리 프로그램
===============


# 1. 카카오봇
## 1.1.일정관리봇
### 1.1.1.프로젝트 설명
**<기존 주간보스 일정 관리 프로세스>**
<details markdown="1">
<summary>사진 접기/펼치기</summary>

![RO0](https://user-images.githubusercontent.com/82567430/124717814-70e6b180-df40-11eb-87ae-09de3a0d3700.PNG)
</details>

        
        1.톡방 인원들은 주간보스 스케쥴을 공유한다.
        2.격수가 시간을 지정한후 투표를 주최하여  참여자의 참가 가/불가 여부를 묻는다
        3.투표가 끝나면 일정이 확정되고 톡방에 알린다.
        4. (3)을 담당자가 날짜별,시간별로 정렬,하여 마스터 일정과 병합시킨후 공지한다.
_4.<<의 프로세스가 필요하지만 단순 반복작업이고 한 사람이 담당하므로 부담이크다_   
*따라서 대체할 봇을 설계하기로한다.*


        
### 1.1.2.기능목록
####    일정등록
<details markdown="1">
<summary>사진 접기/펼치기</summary>

![GO1](https://user-images.githubusercontent.com/82567430/124719067-b657ae80-df41-11eb-9b13-d259d77da7b5.jpg)
</details>

####    일정조회(전체)
<details markdown="1">
<summary>사진 접기/펼치기</summary>

![GO2](https://user-images.githubusercontent.com/82567430/124719074-b8217200-df41-11eb-9d7c-6858266ee28f.jpg)
</details>

####    일정조회(조건:주최자)
<details markdown="1">
<summary>사진 접기/펼치기</summary>

![GO3](https://user-images.githubusercontent.com/82567430/124719073-b788db80-df41-11eb-89cc-39675c2a1486.jpg)
</details>

####    일정조회(조건:보스)
<details markdown="1">
<summary>사진 접기/펼치기</summary>

![GO4](https://user-images.githubusercontent.com/82567430/124719070-b6f04500-df41-11eb-93a9-fd6a7f57f1cf.jpg)
</details>

####    일정삭제


### 1.1.3.대략적 기술

        
    1.(javascript 봇)봇이깔린 기기에서 카카오톡 수신시 커맨드 인지 판별->
    2.(javascript 봇)커맨드인경우 해당문자열을 붙인 URL로 서버(django)에 html요청->
    3.(django서버)커맨드를 처리한후 봇이 발신할 메세지를 담아 \<pre\>태그로 감싼후(복수일 수 있음) html응답->
    4.(javascript 봇)html을 수신후 pre태그를 떼어내고 내용을 파싱하여 메세지 발신.
    
**★★★자바스크립트만으로도 봇구동이가능한데 굳이 파이썬 서버까지 사용한 이유**   
   ●스케쥴 등록을 위해 재대로된 DB를 사용하기 위함(변수사용하면 꺼질때마다 날라감 & 자바스크립트로 db파일관리 하면 귀찬음)   
   ●메인기능,커맨드 추가할때 폰에서 스크립트 추가 귀찬음!


### 1.1.4.사용툴 및 참고링크
리드미 작성   
　　　　[[github 마크다운 문법]](https://gist.github.com/ihoneymon/652be052a0727ad59601)
    
        
Python 3.9.6
        [[날짜 형변환・포매팅 ]](https://gonigoni.kr/posts/python-datetime-string-formatting/)

django     
　　　　[[django환경설정]](https://dev-yakuza.posstree.com/ko/django/installation/)   
　　　　[[django기본:egg-money블로그]](https://egg-money.tistory.com/80?category=811218)   
　　　　[[django API 만들기]](https://www.bezkoder.com/django-rest-api/)   
    
카카오봇   
　　　　[[카카오톡봇:공식문서]](https://kkotbot-docs.kro.kr/)    
　　　　[[카카오톡봇 소스참고:Dark Tornado블로그]](https://m.blog.naver.com/PostList.naver?blogId=dt3141592&categoryNo=65&currentPage=1)     
    
heroku   
　　　　[[환경설정:stackoverflow 환경설정 에러해결]](https://stackoverflow.com/questions/36665889/collectstatic-error-while-deploying-django-app-to-heroku)  
　　　　[[heroku서버 슬립방지:uptimerobot]](https://uptimerobot.com/)
    

## 1.2.아이템분석봇


# 2. 길드원 관리 사이트
## 2.1. 길드원 가입,탈퇴자 관리 페이지
## 2.2. 길드컨탠츠 관리 페이지