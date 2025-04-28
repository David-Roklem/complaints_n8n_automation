import httpx
from utils import translate
from config import settings


async def analyze_sentiment(text: str) -> dict:
    text_in_ru = await translate(text)
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.apilayer.com/sentiment/analysis",
                headers={"apikey": settings.SENTIMENT_API_KEY},
                data=text_in_ru,
            )
            response.raise_for_status()
            sentiment = response.json()
            if sentiment.get("sentiment") in {"positive", "negative", "neutral"}:
                return sentiment
            return "unknown"

    except httpx.HTTPStatusError as e:
        return e


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
            )
            response.raise_for_status()
            category = response.json()['choices'][0]['message']['content'].strip().lower()
            if category in {"техническая", "оплата"}:
                return category
            return "другое"

    except httpx.HTTPStatusError as e:
        return e


async def get_prompt_features(text: str) -> tuple[str | None]:
    return await analyze_sentiment(text), await analyze_category(text)
