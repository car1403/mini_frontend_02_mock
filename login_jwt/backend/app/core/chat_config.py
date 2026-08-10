"""백엔드의 .env 파일을 환경변수로 불러오는 설정 파일입니다."""

from pathlib import Path

from dotenv import load_dotenv

# 현재 파일에서 두 단계 위인 backend 폴더의 절대 경로를 구합니다.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
# .env에 저장된 JWT 비밀키와 Gemini API 키 등을 읽습니다.
load_dotenv(PROJECT_ROOT / ".env")
