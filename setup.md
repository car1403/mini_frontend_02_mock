# 통합 설치 및 실행 가이드

이 문서는 다음 두 프로젝트의 설치와 실행 방법을 하나로 정리한 문서다.

- `frontend`: Streamlit 사용자 화면
- `backend`: FastAPI API 서버

두 프로젝트는 의존성을 독립적으로 관리할 수 있도록 각각 별도의 가상환경을 사용한다.

## 1. 사전 준비

필요한 프로그램:

- Python 3.11 이상
- Windows PowerShell
- Gemini 채팅 기능을 사용할 경우 Gemini API 키

프로젝트 루트:

```text
C:\mini_frontend_sam\mini_frontend_02_mock
```

Python 설치 여부를 확인한다.

```powershell
python --version
```

`python` 명령을 찾지 못하면 Python을 설치한 뒤 터미널을 다시 연다.

## 2. 전체 실행 순서

```text
1. 백엔드 가상환경 생성 및 패키지 설치
2. 백엔드 환경 변수 설정
3. 첫 번째 PowerShell에서 FastAPI 실행
4. 프론트엔드 가상환경 생성 및 패키지 설치
5. 두 번째 PowerShell에서 Streamlit 실행
6. 브라우저에서 화면과 API 연결 확인
```

최초 한 번만 가상환경 생성과 패키지 설치를 진행한다. 이후에는 각 가상환경을 활성화하고 서버만 실행하면 된다.

## 3. 백엔드 설치

PowerShell을 열고 프로젝트 루트에서 백엔드 디렉터리로 이동한다.

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\backend
```

백엔드 전용 가상환경을 생성하고 활성화한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

가상환경이 활성화되면 터미널 입력 줄 앞에 `(.venv)`가 표시된다.

패키지 설치 도구를 업데이트하고 백엔드 의존성을 설치한다.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. 백엔드 환경 변수 설정

`backend` 디렉터리 안에 `.env` 파일을 생성한다.

```text
mini_frontend_02_mock/
└─ backend/
   ├─ .env
   ├─ requirements.txt
   └─ app/
```

`.env` 파일에 다음 내용을 입력한다.

```env
GEMINI_API_KEY=발급받은_Gemini_API_키
GEMINI_MODEL=gemini-2.5-flash-lite
```

주의 사항:

- 실제 API 키를 따옴표로 감쌀 필요는 없다.
- `.env` 파일과 API 키를 Git에 올리지 않는다.
- Gemini 채팅을 사용하지 않더라도 서버는 실행할 수 있지만, 채팅 요청은 실패할 수 있다.

## 5. 백엔드 실행

백엔드 가상환경이 활성화된 첫 번째 PowerShell에서 실행한다.

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

정상 실행 후 확인 주소:

- API 문서: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- OpenAPI 문서: [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json)

현재 구현된 주요 API:

| 메서드 | 경로 | 설명 |
|---|---|---|
| POST | `/chat/gemini` | Gemini 질문 전송 |
| POST | `/product/create` | 상품 생성 |
| GET | `/product/get/{product_id}` | 상품 단건 조회 |
| GET | `/product/getall` | 상품 전체 조회 |
| PUT | `/product/update/{product_id}` | 상품 수정 |
| DELETE | `/product/delete/{product_id}` | 상품 삭제 |

> 프론트엔드의 서버 상태 확인 화면은 `/health`를 요청하지만 현재 백엔드에는 해당 API가 없다. `plan.md`의 1단계 개발에서 추가할 예정이다.

백엔드 서버를 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누른다.

## 6. 프론트엔드 설치

백엔드는 실행 상태로 두고 두 번째 PowerShell을 연다.

프론트엔드 디렉터리로 이동한다.

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\frontend
```

프론트엔드 전용 가상환경을 생성하고 활성화한다.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

패키지 설치 도구를 업데이트하고 프론트엔드 의존성을 설치한다.

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 7. 프론트엔드 실행

프론트엔드 가상환경이 활성화된 두 번째 PowerShell에서 실행한다.

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\frontend
python -m streamlit run app.py
```

Streamlit이 정상 실행되면 기본 브라우저가 자동으로 열린다. 자동으로 열리지 않으면 다음 주소에 접속한다.

- 프론트엔드: [http://localhost:8501](http://localhost:8501)

프론트엔드 서버를 종료하려면 실행 중인 터미널에서 `Ctrl+C`를 누른다.

## 8. 다음 실행부터 사용하는 명령

패키지 설치가 끝난 뒤에는 가상환경을 다시 만들 필요가 없다.

### 첫 번째 PowerShell — 백엔드

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 두 번째 PowerShell — 프론트엔드

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\frontend
.\.venv\Scripts\Activate.ps1
python -m streamlit run app.py
```

## 9. 테스트 실행

백엔드 가상환경이 활성화된 PowerShell에서 실행한다.

```powershell
cd C:\mini_frontend_sam\mini_frontend_02_mock\backend
python -m pytest
```

Gemini 라우터 테스트는 실제 Gemini API 대신 모의 응답을 사용한다.

## 10. 현재 화면 확인 방법

프론트엔드의 현재 로그인 테스트 계정:

```text
ID: id01
PWD: pwd01
```

현재 상태에서 확인할 수 있는 기능:

- 홈 화면
- 고정 테스트 계정을 이용한 로그인과 로그아웃
- 회원가입 입력 화면
- Open-Meteo를 이용한 날씨 조회
- FastAPI 서버 상태 확인 화면

현재 제한 사항:

- 회원가입 정보는 저장되지 않는다.
- 상품 API는 고정 예시 데이터를 반환하며 데이터베이스에 저장하지 않는다.
- 프론트엔드에는 상품 및 Gemini 채팅 화면이 아직 없다.
- `/health` API가 아직 없어 서버 상태 확인 화면에서 정상 결과가 나오지 않는다.

## 11. 문제 해결

### PowerShell에서 가상환경을 활성화할 수 없는 경우

현재 PowerShell 창에만 실행 정책을 적용한 뒤 다시 활성화한다.

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### `python` 명령을 찾을 수 없는 경우

Windows 환경에 따라 다음 명령을 대신 사용할 수 있다.

```powershell
py --version
```

이 경우 문서의 `python`을 `py`로 바꾸어 실행한다.

### 포트가 이미 사용 중인 경우

기존 FastAPI 또는 Streamlit 서버가 실행 중인지 확인하고 해당 터미널에서 `Ctrl+C`로 종료한다.

백엔드 포트를 변경하면 프론트엔드의 `API_BASE_URL`도 같은 주소로 변경해야 한다. 현재 주소는 다음 파일에 직접 설정되어 있다.

```text
frontend/app_pages/04_health.py
```

### Gemini 요청이 실패하는 경우

다음 항목을 확인한다.

1. `backend/.env` 파일이 존재하는지
2. `GEMINI_API_KEY` 값이 올바른지
3. 백엔드를 `backend` 디렉터리에서 실행했는지
4. 인터넷 연결과 Gemini API 사용량 제한에 문제가 없는지

### 패키지 충돌이 발생하는 경우

프론트엔드와 백엔드가 서로 다른 가상환경을 사용 중인지 확인한다.

```text
frontend/.venv
backend/.venv
```

하나의 가상환경에 두 `requirements.txt`를 함께 설치하지 않는 것을 권장한다.

## 12. 개발 완료 후 갱신할 항목

아래 기능이 구현되면 이 문서도 함께 수정한다.

- `/health` API 주소
- 인증 및 회원가입 환경 변수
- 데이터베이스 연결 정보
- 프론트엔드 API 기본 주소 환경 변수
- 상품과 채팅 화면 사용 방법
- 운영 환경 실행 및 배포 방법

