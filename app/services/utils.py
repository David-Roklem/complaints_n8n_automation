from translate import Translator


async def translate(text: str) -> str:
    translator = Translator(from_lang="ru", to_lang="en")
    translation = translator.translate(text)
    return translation
