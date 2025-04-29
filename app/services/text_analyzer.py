import httpx
from services.utils import translate
from config import settings


async def analyze_sentiment(text: str) -> dict:
    text_in_en = await translate(text)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.apilayer.com/sentiment/analysiss",
                headers={"apikey": settings.APILAYER_KEY},
                data=text_in_en,
                timeout=20,
            )
            response.raise_for_status()
            sentiment = response.json()
            if sentiment.get("sentiment") in {"positive", "negative", "neutral"}:
                return sentiment
            return "unknown"

    except httpx.HTTPStatusError:
        return "unknown"


async def analyze_category(text: str) -> str:
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


async def get_text_features(text: str) -> tuple[str | None]:
    return await analyze_sentiment(text), await analyze_category(text), await analyze_for_spam(text)


async def analyze_for_spam(text: str) -> bool:
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
