# 초보자를 위한 JWT 로그인 설명

이 프로젝트는 로그인을 성공한 사용자만 Product API를 사용할 수 있도록 JWT를 사용합니다.

처음에는 JWT의 내부 구조를 모두 외울 필요가 없습니다. 다음 흐름부터 이해하면 됩니다.

```text
아이디와 비밀번호로 로그인
        ↓
백엔드가 JWT 발급
        ↓
프론트엔드가 JWT 보관
        ↓
Product 요청에 JWT를 함께 전송
        ↓
백엔드가 JWT 검사
        ↓
정상 JWT이면 Product 처리
```

## 1. JWT란 무엇인가요?

JWT는 `JSON Web Token`의 줄임말입니다.

쉽게 말하면 로그인에 성공했다는 사실을 증명하는 **임시 출입증**입니다.

회사 출입증을 예로 들어 보겠습니다.

- 사용자는 로그인할 때 아이디와 비밀번호를 제출합니다.
- 백엔드는 아이디와 비밀번호가 맞는지 확인합니다.
- 정보가 맞으면 백엔드가 사용자에게 출입증인 JWT를 발급합니다.
- 사용자는 보호된 기능을 요청할 때마다 JWT를 함께 보여 줍니다.
- 백엔드는 출입증이 위조되지 않았고 사용 시간이 지나지 않았는지 확인합니다.

JWT 자체가 로그인 기능은 아닙니다.  
로그인에 성공한 사용자가 이후 요청에서도 자신을 증명하기 위해 사용하는 값입니다.

## 2. 왜 JWT를 사용하나요?

기존 `login/backend`에서는 로그인 요청에 성공해도 사용자 정보만 반환했습니다.

```json
{
  "id": "id01",
  "name": "사용자"
}
```

하지만 이 정보만으로는 다음 Product 요청을 보낸 사람이 로그인한 사용자인지 확인할 수 없습니다.

JWT 방식에서는 로그인 성공 시 다음과 같은 토큰을 반환합니다.

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

사용자는 이 토큰을 Product 요청에 함께 보냅니다.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

백엔드는 토큰을 검사한 후에만 Product 기능을 실행합니다.

## 3. Bearer란 무엇인가요?

`Bearer`는 JWT의 일부분이 아니라 **인증 방식을 나타내는 이름**입니다.

Bearer는 영어로 `소지자`, 즉 어떤 것을 가지고 있는 사람이라는 뜻입니다.

Bearer 인증에서는 유효한 토큰을 가지고 있는 사람이 요청을 보낼 권한을 가진 것으로 판단합니다. 회사 출입증을 가지고 있는 사람이 출입할 수 있는 것과 비슷합니다.

HTTP 요청에서는 다음과 같이 사용합니다.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

각 부분의 의미는 다음과 같습니다.

```text
Authorization : 인증 정보를 전달하는 HTTP 헤더 이름
Bearer        : 지금 전달하는 인증 정보가 Bearer 토큰이라는 표시
eyJhbG...     : 로그인 후 백엔드에서 발급받은 실제 JWT
```

중요한 점은 `Bearer`와 JWT 사이에 공백이 하나 있어야 한다는 것입니다.

```text
Bearer JWT값
      ↑
    공백 한 칸
```

### Bearer는 JWT인가요?

아닙니다.

- JWT는 실제 사용자와 만료 시간 등이 들어 있는 토큰입니다.
- Bearer는 그 토큰을 HTTP 요청으로 전달하는 인증 방식입니다.

다음 응답을 살펴보겠습니다.

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

- `access_token`은 실제 JWT입니다.
- `token_type`은 이 토큰을 Bearer 방식으로 보내라는 안내입니다.

따라서 `access_token` 값 안에 `Bearer`라는 글자가 포함되어 있는 것은 아닙니다.

### 왜 그냥 JWT만 보내지 않나요?

`Authorization` 헤더는 여러 인증 방식을 지원합니다.

예를 들어 다음과 같은 인증 방식이 있을 수 있습니다.

```http
Authorization: Basic 사용자정보
Authorization: Bearer 토큰
```

앞에 `Bearer`를 붙이면 서버는 뒤에 오는 값이 Bearer 방식의 토큰이라는 것을 알 수 있습니다.

### 이 프로젝트에서는 어디에서 Bearer를 사용하나요?

백엔드의 `app/core/auth_dependency.py`에서 `HTTPBearer`를 사용합니다.

```python
bearer_scheme = HTTPBearer(auto_error=False)
```

FastAPI의 `HTTPBearer`는 다음 요청 헤더를 읽습니다.

```http
Authorization: Bearer JWT값
```

그리고 실제 JWT 부분만 꺼낼 수 있게 해 줍니다.

```python
token = credentials.credentials
```

프론트엔드의 `login_jwt/frontend/core/api_client.py`에서는 다음 코드로 헤더를 만듭니다.

```python
headers["Authorization"] = f"Bearer {access_token}"
```

따라서 사용자가 Product 기능을 실행하면 프론트엔드가 자동으로 `Bearer`와 JWT를 붙여서 전송합니다.

### Bearer 사용 시 주의할 점

Bearer 방식은 토큰을 가지고 있으면 사용할 수 있는 방식입니다. 따라서 JWT를 다른 사람에게 보여 주거나 외부에 공개하면 안 됩니다.

- JWT를 소스 코드에 직접 작성하지 않습니다.
- JWT를 로그나 화면에 불필요하게 출력하지 않습니다.
- 실제 서비스에서는 HTTPS를 사용합니다.
- 토큰이 노출되었다면 만료 전까지 악용될 가능성이 있다고 생각해야 합니다.
- 비밀번호와 마찬가지로 토큰도 안전하게 보관합니다.

JWT는 요청마다 전송되지만 HTTPS를 사용하면 네트워크 전송 내용이 암호화됩니다. 실제 서비스에서 HTTP만 사용하면 토큰이 노출될 위험이 있습니다.

## 4. JWT는 어떻게 생겼나요?

JWT는 점(`.`)으로 구분된 세 부분으로 이루어집니다.

```text
Header.Payload.Signature
```

예시는 다음과 같습니다.

```text
xxxxx.yyyyy.zzzzz
```

### Header

토큰을 만들 때 사용한 알고리즘 정보가 들어갑니다.

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload

사용자와 토큰에 관한 정보가 들어갑니다.

이 프로젝트에서는 다음 두 값을 저장합니다.

```json
{
  "sub": "id01",
  "exp": "토큰 만료 시간"
}
```

- `sub`: 토큰의 주인인 사용자 ID
- `exp`: 토큰을 사용할 수 있는 마지막 시간

### Signature

토큰이 백엔드에서 만들어졌는지 확인하기 위한 서명입니다.

백엔드는 비밀키를 이용해 서명을 만듭니다. 누군가 Payload의 사용자 ID를 임의로 바꾸면 서명이 맞지 않기 때문에 토큰 검증에 실패합니다.

> JWT의 Header와 Payload는 암호화된 비밀 정보가 아닙니다. 디코딩하면 내용을 볼 수 있으므로 비밀번호나 개인정보를 넣으면 안 됩니다.

## 5. 전체 로그인 흐름

### 첫 번째: 사용자가 로그인합니다

프론트엔드가 다음 요청을 보냅니다.

```http
POST /auth/login
Content-Type: application/json
```

```json
{
  "id": "id01",
  "pwd": "pwd01"
}
```

### 두 번째: 백엔드가 계정을 확인합니다

현재 예제에서는 학습을 위해 다음 계정을 코드에서 직접 확인합니다.

```text
아이디: id01
비밀번호: pwd01
```

실제 서비스에서는 데이터베이스에서 사용자를 찾고 암호화된 비밀번호를 비교해야 합니다.

### 세 번째: 백엔드가 JWT를 발급합니다

로그인에 성공하면 백엔드는 사용자 ID와 만료 시간이 들어 있는 JWT를 만듭니다.

이 프로젝트의 토큰 사용 시간은 30분입니다.

### 네 번째: 프론트엔드가 JWT를 보관합니다

`login_jwt/frontend`는 응답으로 받은 `access_token`을 Session Storage에 저장합니다.

### 다섯 번째: Product 요청에 JWT를 넣습니다

```http
GET /product/getall
Authorization: Bearer 발급받은_JWT
```

### 여섯 번째: 백엔드가 JWT를 검사합니다

백엔드는 다음 내용을 확인합니다.

- Authorization 헤더가 있는가?
- Bearer 토큰이 있는가?
- 백엔드의 비밀키로 만든 토큰인가?
- 토큰 내용이 변경되지 않았는가?
- 토큰 사용 시간이 지나지 않았는가?
- 사용자 ID인 `sub`가 들어 있는가?

모두 정상일 때만 Product API를 실행합니다.

## 6. 프로젝트 코드 읽는 순서

### 1단계: 로그인 요청 받기

파일: `app/routers/auth_router.py`

```python
@auth_router.post("/auth/login")
def login(auth: AuthLogin) -> TokenResponse:
    return login_process(auth)
```

사용자가 보낸 아이디와 비밀번호를 받아 서비스 함수에 전달합니다.

### 2단계: JWT 만들기

파일: `app/services/auth_service.py`

```python
def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    payload = {
        "sub": user_id,
        "exp": expire,
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm="HS256")
```

- `sub`에 사용자 ID를 넣습니다.
- `exp`에 만료 시간을 넣습니다.
- `jwt.encode()`로 서명된 JWT를 만듭니다.

### 3단계: JWT 설정 확인하기

파일: `app/core/jwt_config.py`

```python
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "beginner-jwt-secret-key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_MINUTES = 30
```

- `JWT_SECRET_KEY`: 토큰을 만들고 검사할 때 사용하는 비밀키
- `JWT_ALGORITHM`: 서명을 만드는 방식
- `JWT_EXPIRE_MINUTES`: 토큰을 사용할 수 있는 시간

### 4단계: 요청에서 JWT 검사하기

파일: `app/core/auth_dependency.py`

```python
payload = jwt.decode(
    token,
    JWT_SECRET_KEY,
    algorithms=[JWT_ALGORITHM],
)
```

`jwt.decode()`가 서명과 만료 시간을 검사합니다.

정상 토큰이면 Payload를 반환하고, 잘못된 토큰이면 예외가 발생합니다.

### 5단계: Product API 보호하기

파일: `app/routers/product_router.py`

```python
product_router = APIRouter(
    tags=["Product"],
    dependencies=[Depends(get_current_user)],
)
```

`dependencies`에 `get_current_user`를 등록했기 때문에 이 라우터의 모든 Product API를 실행하기 전에 JWT 검사가 먼저 실행됩니다.

따라서 create, get, getall, update, delete 함수마다 인증 코드를 반복해서 작성할 필요가 없습니다.

### Product 함수마다 인증을 따로 적용하려면?

현재 코드는 다음과 같이 `product_router` 전체에 인증을 적용합니다.

```python
product_router = APIRouter(
    tags=["Product"],
    dependencies=[Depends(get_current_user)],
)
```

이 방식에서는 Product 라우터에 포함된 모든 API가 자동으로 보호됩니다.

만약 전체에 적용하지 않고 원하는 함수마다 인증을 적용하려면 먼저 라우터의 `dependencies`를 제거합니다.

```python
product_router = APIRouter(tags=["Product"])
```

그다음 보호하려는 함수의 매개변수에 `Depends(get_current_user)`를 작성합니다.

```python
@product_router.post("/product/create")
def create(
    product: ProductPublic,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_create(product)
```

요청이 들어오면 Product 생성 함수보다 `get_current_user()`가 먼저 실행됩니다.

- 토큰이 정상이면 사용자 ID가 `current_user`에 들어옵니다.
- 토큰이 없거나 잘못되면 `401` 응답을 반환하고 `product_create()`는 실행되지 않습니다.

현재 `get_current_user()`는 JWT의 `sub` 값을 반환하므로 로그인 계정이 `id01`이면 다음 값이 들어옵니다.

```python
current_user == "id01"
```

모든 Product 함수를 개별적으로 보호하면 다음과 같이 작성할 수 있습니다.

```python
from fastapi import APIRouter, Depends

from app.core.auth_dependency import get_current_user
from app.schemes.product_scheme import ProductPublic, ProductUpdate
from app.services.product_service import (
    product_create,
    product_delete,
    product_get,
    product_get_all,
    product_update,
)


product_router = APIRouter(tags=["Product"])


@product_router.post("/product/create")
def create(
    product: ProductPublic,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_create(product)


@product_router.get("/product/get/{product_id}")
def get(
    product_id: int,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_get(product_id)


@product_router.get("/product/getall")
def get_all(
    current_user: str = Depends(get_current_user),
) -> list[ProductPublic]:
    return product_get_all()


@product_router.delete("/product/delete/{product_id}")
def delete(
    product_id: int,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_delete(product_id)


@product_router.put("/product/update/{product_id}")
def update(
    product_id: int,
    product: ProductUpdate,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_update(product_id, product)
```

이 예제에서는 아직 `current_user`를 Product 서비스에 전달하지 않습니다. 인증에 성공했는지만 확인하기 위해 매개변수로 받고 있습니다.

로그인한 사용자의 ID를 서비스에서 사용하고 싶다면 다음과 같이 전달할 수 있습니다.

```python
@product_router.post("/product/create")
def create(
    product: ProductPublic,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_create(product, current_user)
```

서비스 함수도 사용자 ID를 받을 수 있도록 변경합니다.

```python
def product_create(
    product: ProductPublic,
    current_user: str,
) -> ProductPublic:
    print("상품을 등록한 사용자:", current_user)
    return product
```

### 일부 API만 보호하는 예제

함수별 방식을 사용하면 일부 API는 공개하고 일부 API만 보호할 수도 있습니다.

```python
# 로그인하지 않아도 상품 목록을 볼 수 있습니다.
@product_router.get("/product/getall")
def get_all() -> list[ProductPublic]:
    return product_get_all()


# 로그인한 사용자만 상품을 만들 수 있습니다.
@product_router.post("/product/create")
def create(
    product: ProductPublic,
    current_user: str = Depends(get_current_user),
) -> ProductPublic:
    return product_create(product)
```

### 두 방식의 차이

| 적용 방식 | 장점 | 주의할 점 |
|---|---|---|
| 라우터 전체에 적용 | 코드가 짧고 인증을 빠뜨릴 가능성이 작음 | 해당 라우터의 모든 API가 보호됨 |
| 함수마다 적용 | 공개 API와 보호 API를 자유롭게 구분할 수 있음 | 새 함수를 만들 때 `Depends`를 빠뜨릴 수 있음 |

현재 프로젝트처럼 Product API를 모두 로그인 이후에만 사용해야 한다면 라우터 전체에 적용하는 현재 방식이 더 간단하고 안전합니다.

상품 목록은 누구나 볼 수 있지만 생성, 수정, 삭제만 로그인 사용자에게 허용하려면 함수별 적용 방식이 더 적합합니다.

> 라우터 전체와 함수에 `Depends(get_current_user)`를 동시에 작성할 필요는 없습니다. 동시에 작성하면 같은 요청에서 인증 함수가 중복으로 선언되어 코드의 의도를 이해하기 어려워집니다.

## 7. 정상 요청과 실패 요청

### 토큰이 없는 경우

```http
GET /product/getall
```

응답:

```json
{
  "detail": "로그인이 필요합니다."
}
```

HTTP 상태 코드는 `401 Unauthorized`입니다.

### 토큰이 잘못된 경우

```http
Authorization: Bearer wrong-token
```

응답:

```json
{
  "detail": "올바르지 않은 토큰입니다."
}
```

### 토큰이 만료된 경우

응답:

```json
{
  "detail": "토큰 사용 시간이 만료되었습니다."
}
```

### 정상 토큰인 경우

Product API가 정상적으로 실행됩니다.

## 8. Swagger에서 직접 확인하기

### 서버 실행

```powershell
cd login_jwt/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

브라우저에서 다음 주소를 엽니다.

```text
http://127.0.0.1:8000/docs
```

### 테스트 순서

1. `POST /auth/login`을 엽니다.
2. **Try it out**을 누릅니다.
3. 다음 로그인 정보를 입력합니다.

```json
{
  "id": "id01",
  "pwd": "pwd01"
}
```

4. **Execute**를 누릅니다.
5. 응답의 `access_token` 값만 복사합니다.
6. Swagger 오른쪽 위의 **Authorize** 버튼을 누릅니다.
7. 복사한 토큰을 입력하고 **Authorize**를 누릅니다.
8. `GET /product/getall`을 실행합니다.

현재 FastAPI의 Bearer 인증 입력창에는 일반적으로 토큰 값만 입력하면 됩니다. Swagger가 요청을 보낼 때 `Bearer`를 자동으로 붙입니다.

## 9. 프론트엔드와 함께 실행하기

백엔드와 프론트엔드는 각각 실행해야 합니다.

터미널 1:

```powershell
cd login_jwt/backend
uvicorn app.main:app --reload
```

터미널 2:

```powershell
cd login_jwt/frontend
streamlit run app.py
```

프론트엔드 로그인 이후 Product 요청에는 다음 헤더가 자동으로 추가됩니다.

```http
Authorization: Bearer 발급받은_JWT
```

## 10. 로그아웃하면 JWT가 즉시 무효가 되나요?

현재 예제에서 로그아웃은 프론트엔드가 보관하던 JWT를 삭제하는 방식입니다.

JWT는 서버가 세션으로 보관하는 값이 아니므로, 토큰 자체의 만료 시간이 남아 있다면 기술적으로는 아직 유효할 수 있습니다.

학습용 프로젝트에서는 다음 방식으로 충분합니다.

- 로그인: JWT 저장
- 로그아웃: 저장한 JWT 삭제
- 30분 후: JWT 자동 만료

실제 서비스에서 토큰을 즉시 무효화해야 한다면 차단 목록, 짧은 Access Token, Refresh Token 등의 추가 설계가 필요합니다.

## 11. 실제 서비스로 발전시킬 때 필요한 것

현재 코드는 JWT의 기본 흐름을 쉽게 이해하기 위한 학습용 코드입니다.

실제 서비스에서는 다음 내용을 추가해야 합니다.

- 사용자를 데이터베이스에서 조회
- 비밀번호를 평문으로 저장하지 않고 해시 처리
- 충분히 길고 무작위인 비밀키 사용
- 비밀키를 코드가 아닌 환경 변수로 관리
- HTTPS 사용
- 짧은 Access Token과 Refresh Token 사용 검토
- 사용자 권한에 따른 API 접근 제어
- 로그아웃한 토큰을 즉시 차단해야 하는지 검토

## 12. 비밀키 설정

현재 기본 비밀키는 학습과 실행 편의를 위한 값입니다.

```python
"beginner-jwt-secret-key"
```

실제 서비스에서는 이 값을 사용하면 안 됩니다.

PowerShell에서 환경 변수를 설정하는 예시는 다음과 같습니다.

```powershell
$env:JWT_SECRET_KEY="길고-복잡하며-외부에-공개되지-않는-임의의-값"
uvicorn app.main:app --reload
```

비밀키가 외부에 알려지면 다른 사람이 정상 토큰처럼 보이는 JWT를 만들 수 있습니다.

## 13. Chat에서 로그인 사용자 ID 사용하기

Chat 요청에는 `user_id`를 직접 넣지 않습니다.

```json
{
  "prompt": "안녕"
}
```

대신 다음 Bearer 헤더를 함께 보냅니다.

```http
Authorization: Bearer 로그인할_때_받은_JWT
```

`get_current_user()`가 JWT의 `sub`에서 사용자 ID를 꺼내 Chat 서비스에 전달합니다.

```python
def chat_gemini(
    chat_request: ChatRequest,
    current_user: str = Depends(get_current_user),
) -> ChatResponse:
    return call_gemini(chat_request, current_user)
```

이렇게 해야 사용자가 요청 Body의 ID를 바꿔 다른 사용자인 것처럼 요청하는 것을 막을 수 있습니다. 나중에 대화를 저장할 때는 다음 정보를 함께 저장할 수 있습니다.

```text
current_user + prompt + answer + created_at
```

## 14. 꼭 기억할 내용

- JWT는 로그인 성공을 증명하는 임시 출입증입니다.
- Bearer는 JWT 자체가 아니라 토큰을 전달하는 인증 방식입니다.
- 요청에서는 `Authorization: Bearer JWT값` 형태로 사용합니다.
- 로그인 성공 시 백엔드가 JWT를 발급합니다.
- 보호된 API를 호출할 때 JWT를 Authorization 헤더에 넣습니다.
- 백엔드는 JWT의 서명과 만료 시간을 검사합니다.
- JWT Payload에 비밀번호나 개인정보를 넣으면 안 됩니다.
- JWT 비밀키는 외부에 공개하면 안 됩니다.
- 현재 프로젝트에서는 Product API와 Chat API를 JWT로 보호합니다.
