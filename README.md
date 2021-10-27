# 온보딩 게시판 CRUD
## 구현 기술 스택
Python 프로그래밍 언어와 Django 프레임워크 기술 스택으로 구현 하였습니다.
### 서버 실행 방법
```python
python manage.py runserver
```
해당 디렉토리에서 위 명령어를 입력하여 서버를 실행한다.(localhost에서 실행)

## 회원가입
- bcyrpt를 사용하여 비밀번호 암호화
- email, 비밀번호(숫자, 영어, 특수문자 포함)의 정규식을 사용

endpoint : http://localhost:8000/users/signin

## 로그인
- JWT를 사용하여 인증, 인가를 통해 권한 부여

endpoint : http://localhost:8000/users/login
## 글 작성(create)
- 로그인 하여 토큰이 발행되어 권한이 있는 유저만 작성가능하다.
- 권한이 없을 경우 `INVALID_TOKEN` 에러 메세지 반환한다.
- 사용자가 글을 작성하지 않을 시 `WRITE_A_TEXT` 에러 메세지 반환한다.

### 응답요청
endpoint : http://localhost:8000/postings<br/>
method : `POST`
```json
{   
    "text" : "내일도 날씨가 좋습니다."
}
```
status code : `201`
```json
{   
    "message" : "SUCCESS"
}
```
## 글 목록확인(read)
- 쿼리 파라미터로 pagination 기능을 사용하여 한 페이지에 3개의 게시물을 출력한다.
- user_id를 사용 할 겨우 경우는 user_id에 해당유저의 게시물만 출력한다.
- page에 정수가 아닌 값을 입력하거나 게시물의 없는 페이지를 입력하였을 경우 첫번째 페이지를 반환한다.

### 응답요청
endpoint : http://localhost:8000/postings/list?page={page}&user_id={user_id}<br/>
method : `GET`<br/>
status code : `200`
```json
{
    "page": "1",
    "all_post": [
        {
            "id": 1,
            "user_id": 1,
            "name": "김훈태",
            "text": "안녕",
            "created_at": "2021-10-26T18:25:29.150"
        },
        {
            "id": 3,
            "user_id": 1,
            "name": "김훈태",
            "text": "오하이요",
            "created_at": "2021-10-26T21:13:08.823"
        },
        {
            "id": 4,
            "user_id": 1,
            "name": "김훈태",
            "text": "오하이요",
            "created_at": "2021-10-26T21:14:05.285"
        }
    ]
}
```

## 글 확인(read)
- path파라미터를 사용하여 해당 게시물만 확인 가능하다.
- 존재하지 않는 게시물의 id값을 입력 할 경우 `NOT_POSTING` 에러 메세지를 반환한다.

### 응답요청
endpoint : http://localhost:8000/postings/{posting_id}<br/>
method : `GET`<br/>
status code : `200`
```json
{
    "results": [
        {
            "id": 1,
            "user_id": 1,
            "name": "김훈태",
            "text": "안녕",
            "created": "2021-10-26T18:25:29.150"
        }
    ]
}
```
## 글 수정(update)
- 권한이 있는 유저만 자신의 게시물을 수정 할 수 있으며 권한이 없거나 게시물이 없을 시 `NOT_EXISTS` 에러 메세지를 반환한다.
- 수정시 빈 값을 입력할 경우 `WRITE_A_TEXT` 에러 메세지를 반환한다.

### 응답요청
endpoint : http://localhost:8000/postings/{posting_id}<br/>
method : `PATCH`
```json
{   
    "text" : "안녕하세요!!!."
}
```
status code : `200`
```json
{   
    "message" : "UPDATE_SUCCESS"
}
```
![](https://images.velog.io/images/kim-hoontae/post/0574eee2-bbdc-4a69-9e00-829ba80a3652/%E1%84%89%E1%85%B3%E1%84%8F%E1%85%B3%E1%84%85%E1%85%B5%E1%86%AB%E1%84%89%E1%85%A3%E1%86%BA%202021-10-27%20%E1%84%8B%E1%85%A9%E1%84%92%E1%85%AE%201.09.29.png)
글 확인에서 id가 1번인 유저가 1번 게시물을  위 이미지의 내용과 같이 변경된 걸 확인할 수 있습니다.
## 글 삭제(delete)
- 권한이 있는 유저만 자신의 게시물을 삭제 할 수 있으며 권한이 없거나 게시물이 없을 시 `NOT_EXISTS` 에러 메세지를 반환한다.

### 응답요청
endpoint : http://localhost:8000/postings/{posting_id}<br/>
method : `DELETE`
<br/>
status code : `200`
```json
{   
    "message" : "DELETE_SUCCESS"
}
```
