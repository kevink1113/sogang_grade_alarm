# sogang-grade-alarm

## 서강대학교 SAINT 중간, 기말 성적 텔레그램 알림 서비스

Mobile SAINT 크롤링을 통해 서버에 부담이 가지 않는 선에서 주기적으로 성적 업데이트를 확인하여  
텔레그램으로 성적 업로드 알림을 주는 Python 스크립트. CSPRO와 같은 서버에서 실행.

> [!Note]
> Works with Python version over 3.5.2  
> cspro (뒤에 숫자 없는 그냥 cspro)에서 실행 가능

### 요구사항 설치

```
pip3 install -r requirments.txt
```

### 백그라운드 실행

nohup을 이용하여 셸 창을 닫아도 백그라운드에서 실행되도록 설정 가능하다.  
실제 정상 실행 여부 확인을 위해 그냥 `python3 main.py`로 확인.

```
nohup python3 main.py &
```

### Telegram 챗봇, 사용자 인증

텔레램 챗봇 API와 채팅방 ID 얻는 방법은 하단 링크 참조.  
[텔레그램 챗봇 생성 방법](https://technfin.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC%EC%9C%BC%EB%A1%9C-%ED%85%94%EB%A0%88%EA%B7%B8%EB%9E%A8-%EB%A9%94%EC%84%B8%EC%A7%80-%EB%B3%B4%EB%82%B4%EA%B8%B0)

코드 상단 부분: 토큰, 채팅방 ID, 알림을 받고 싶은 학기와 SAINT 아이디, 비번 입력

```
TELEGRAM_TOKEN = '부여받은_토큰'   # 처음 받은 HTTP API
CHAT_ID = '채팅방_ID'   # 채팅방 ID: 확인 방법은 문서 참조

SEMESTER = '2023020'    # 2023년도 1학기이면: 2023010과 같이 표현됨
SAINT_ID = '20xxxxxx'   # 학번
SAINT_PW = 'xxxx'       # SAINT 비밀번호

...
```

### 실제 실행

```
성적알림을 시작합니다. 5분마다 변경사항을 확인합니다.
확인중인 학기: 2023020
...
```

위와 같이 시작하는 텔레그램 메시지가 수신되었다면 정상 작동하는 것이다.
