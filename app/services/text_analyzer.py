import httpx
from services.utils import translate
from config import settings


async def analyze_sentiment(text: str) -> str:
    """
    Анализирует настроение текста с использованием внешнего API.

    :param text: Текст, для которого необходимо определить настроение.
    :return: Строка с названием настроения.
    """
    text_in_en = await translate(text)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.apilayer.com/sentiment/analysis",
                headers={"apikey": settings.APILAYER_KEY},
                data=text_in_en,
                timeout=20,
            )
            response.raise_for_status()
            response_body = response.json()
            sentiment = response_body.get("sentiment")
            if sentiment in {"positive", "negative", "neutral"}:
                return sentiment
            return "unknown"

    except httpx.HTTPStatusError:
        return "unknown"


async def analyze_category(text: str) -> str:
    """
    Определяет категорию жалобы на основе текста.

    :param text: Текст жалобы, для которого необходимо определить категорию.
    :return: Категория жалобы (техническая, оплата или другое).
    """
    prompt = (
        f"Определи категорию жалобы: '{text}'. "
        "Варианты: техническая, оплата, другое. "
        "Ответ только одним словом."
    )

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://models.github.ai/inference/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "openai/gpt-4.1-mini",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0,
                },
                timeout=20,
            )
            response.raise_for_status()
            category = response.json()['choices'][0]['message']['content'].strip().lower()
            if category in {"техническая", "оплата"}:
                return category
            return "другое"

    except httpx.HTTPStatusError:
        return "другое"


async def get_text_features(text: str) -> tuple[str | bool]:
    """
    Получает характеристики текста, включая настроение, категорию и наличие спама.

    :param text: Текст, для которого необходимо получить характеристики.
    :return: Кортеж с результатами анализа: настроение, категория и наличие спама.
    """
    return await analyze_sentiment(text), await analyze_category(text), await analyze_for_spam(text)


async def analyze_for_spam(text: str) -> bool:
    """
    Проверяет текст на наличие спама с использованием внешнего API.

    :param text: Текст, который необходимо проверить на спам.
    :return: True, если текст является спамом, иначе False.
    """
    text_in_en = await translate(text)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.apilayer.com/spamchecker",
                headers={"apikey": settings.APILAYER_KEY},
                params={"threshold": 3.0},
                data=text_in_en,
                timeout=20,
            )
            response.raise_for_status()
            sentiment = response.json()
            if sentiment and sentiment.get("is_spam"):
                return True
            return False

    except httpx.HTTPStatusError:
        return False
