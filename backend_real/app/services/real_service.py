import random
from datetime import datetime


def make_fake_data(number: int) -> dict:
    """DB 대신 화면에 보낼 가상 온도 데이터를 하나 만듭니다."""

    temperature = random.randint(18, 35)

    if temperature >= 30:
        status = "더움"
    else:
        status = "정상"

    return {
        "number": number,
        "temperature": temperature,
        "status": status,
        "created_at": datetime.now().strftime("%H:%M:%S"),
    }
