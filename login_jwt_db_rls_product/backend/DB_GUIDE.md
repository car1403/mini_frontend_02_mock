# Product RLS 설정 가이드

## 1. RLS란 무엇인가요?

RLS는 `Row Level Security`의 줄임말이며, 우리말로는 **행 수준 보안** 또는 **행 단위 접근 제어**라고 합니다.

- `Row`: 데이터베이스 테이블의 한 행
- `Level`: 보안을 적용하는 수준 또는 단위
- `Security`: 데이터 접근을 제한하는 보안 정책

일반적인 테이블 권한은 사용자가 테이블 전체를 조회하거나 수정할 수 있는지를 결정합니다. RLS는 같은 테이블 안에서도 사용자마다 접근할 수 있는 행을 다르게 제한합니다.

예를 들어 주문 테이블에 여러 사용자의 주문이 함께 저장되어 있어도 다음 정책을 적용하면 로그인한 사용자는 자신의 주문 행만 조회할 수 있습니다.

```sql
USING ((SELECT auth.uid()) = user_id)
```

RLS는 SQL이 실행될 때 PostgreSQL이 각 행의 조회·생성·수정·삭제 가능 여부를 정책으로 검사합니다. FastAPI에서 권한 검사를 빠뜨리더라도 데이터베이스가 다시 접근을 제한하는 방어 계층입니다.

이 프로젝트에서는 일반 사용자와 관리자 모두 상품을 조회할 수 있지만, 상품 생성·수정·삭제는 관리자만 할 수 있도록 RLS 정책을 적용합니다.

### RLS는 Supabase만의 기능인가요?

아닙니다. RLS는 PostgreSQL이 제공하는 데이터베이스 보안 기능입니다. Supabase는 Supabase Auth가 발급한 Access Token의 사용자 정보를 `auth.uid()`로 확인할 수 있게 연결해 주므로 RLS를 편리하게 적용할 수 있습니다.

PostgreSQL RLS는 다음과 같은 PostgreSQL 기반 환경에서도 사용할 수 있습니다.

- AWS RDS for PostgreSQL과 Amazon Aurora PostgreSQL
- Google Cloud SQL for PostgreSQL과 AlloyDB
- Azure Database for PostgreSQL
- Neon, Heroku Postgres, Render, Railway 등의 관리형 PostgreSQL
- 직접 설치하여 운영하는 PostgreSQL

다만 일반적인 PostgreSQL 서비스는 Supabase의 `auth.uid()` 연결을 그대로 제공하지 않을 수 있습니다. 이 경우 백엔드가 인증된 사용자나 테넌트 정보를 데이터베이스 세션에 안전하게 전달하고, RLS 정책이 그 값을 검사하도록 별도로 설계해야 합니다.

PostgreSQL 이외에도 비슷한 행 단위 접근 제어 기능이 있습니다.

- CockroachDB: Row-Level Security
- SQL Server와 Azure SQL: Row-Level Security
- Oracle Database: Virtual Private Database(VPD)
- Snowflake: Row Access Policy
- BigQuery: Row-level access policy

제품마다 정책 문법과 인증 정보 전달 방식이 다르지만, 사용자가 허용된 행만 조회하거나 변경하게 한다는 목적은 같습니다.

## 2. SQL 실행

Supabase Dashboard의 SQL Editor에서 `schema.sql` 전체를 실행합니다. 다음 항목이 생성됩니다.

- `user_profiles`: 로그인 사용자의 공개 프로필
- `user_roles`: `user` 또는 `admin` 역할
- `products`: 실제 상품 데이터
- 신규 가입자 프로필·역할 생성 트리거
- 일반 사용자 조회 및 관리자 변경 RLS 정책

## 3. Auth 설정

Supabase Dashboard의 Authentication 설정에서 Email 로그인을 활성화합니다.
수업에서 바로 로그인하려면 Confirm email을 끕니다. Confirm email을 켜면 사용자가 이메일 인증을 마친 뒤 로그인해야 합니다.

## 4. Access Token과 RLS의 연결

프론트엔드는 로그인할 때 Supabase Auth가 발급한 Access Token을 받고, Product 요청의 `Authorization` 헤더로 FastAPI에 전달합니다. FastAPI도 같은 토큰을 Supabase Data API에 전달합니다.

Supabase Data API가 토큰을 검증하면 PostgreSQL의 `auth.uid()`는 로그인한 사용자의 UUID를 반환합니다. RLS 정책은 이 값을 이용해 현재 사용자의 프로필과 역할만 조회하도록 제한합니다.

```sql
USING ((SELECT auth.uid()) = user_id)
```

## 5. RLS 정책 읽는 방법

- `TO authenticated`: 로그인한 사용자의 요청에 정책을 적용합니다.
- `USING`: 기존 행을 조회·수정·삭제할 수 있는지 검사합니다.
- `WITH CHECK`: 새로 생성되거나 수정된 행의 값이 허용되는지 검사합니다.
- 허용하는 정책이 없거나 정책 조건을 만족하지 않으면 해당 작업은 거부됩니다.

`GRANT`는 사용자가 SELECT, INSERT 같은 SQL 명령을 시도할 기본 권한을 부여하고, RLS는 실제로 어떤 행에 접근할 수 있는지 제한합니다. 작업하려면 `GRANT`와 RLS 정책을 모두 통과해야 합니다.

## 6. 환경변수

`backend/.env`를 만듭니다.

```env
SUPABASE_URL=https://프로젝트-ID.supabase.co
SUPABASE_PUBLISHABLE_KEY=publishable-key-또는-anon-key
```

Product CRUD는 publishable key와 사용자의 Access Token을 사용합니다. Service Role 키는 RLS를 우회할 수 있고 이 프로젝트에서 사용하지 않으므로 `.env`에 넣지 않습니다.

## 7. 최초 관리자 지정

먼저 프론트엔드에서 관리자용 계정을 일반 회원으로 가입합니다. Authentication > Users에서 UUID를 확인한 뒤 SQL Editor에서 역할을 변경합니다.

```sql
UPDATE public.user_roles
SET role = 'admin'
WHERE user_id = '관리자 사용자 UUID';
```

역할 변경 전에 발급된 로그인 화면 정보가 남아 있다면 로그아웃 후 다시 로그인합니다.

## 8. 화면에서 확인

1. 일반 사용자 계정으로 가입하고 로그인합니다.
2. Product 목록이 조회되는지 확인합니다.
3. 일반 사용자에게 입력·수정·삭제 UI가 보이지 않는지 확인합니다.
4. 관리자 계정으로 로그인합니다.
5. Product 생성·수정·삭제가 가능한지 확인합니다.
6. Supabase Table Editor에서 실제 `products` 데이터가 변경됐는지 확인합니다.

프론트엔드 버튼을 숨기는 것은 편의 기능입니다. 최종 보안은 FastAPI의 `require_admin`과 DB의 RLS 정책이 담당합니다.

## 9. RLS를 직접 확인

화면을 통한 테스트에서는 일반 사용자의 변경 요청을 FastAPI가 먼저 차단합니다. DB의 RLS도 독립적으로 차단하는지 확인하려면 일반 사용자의 Access Token으로 Supabase Data API를 직접 호출합니다.

```powershell
$supabaseUrl = "https://프로젝트-ID.supabase.co"
$publishableKey = "publishable-key-또는-anon-key"
$userAccessToken = "일반-사용자의-access-token"

$headers = @{
    apikey = $publishableKey
    Authorization = "Bearer $userAccessToken"
    "Content-Type" = "application/json"
    Prefer = "return=representation"
}

$body = @{ name = "RLS 테스트 상품"; price = 1000 } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri "$supabaseUrl/rest/v1/products" -Headers $headers -Body $body
```

일반 사용자 요청은 RLS 정책에 의해 거부되어야 합니다. 관리자 Access Token으로 같은 요청을 보내면 생성되어야 합니다. 테스트용 Access Token은 로그나 문서에 남기지 말고, 테스트가 끝나면 PowerShell 변수도 삭제합니다.
