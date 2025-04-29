from translate import Translator


async def translate(text: str) -> str:
    """
    Переводит текст с русского языка на английский

    :param text: Текст, который необходимо перевести с русского языка на английский.
    :return: Переведенный на английский язык текст.
    """
    translator = Translator(from_lang="ru", to_lang="en")
    translation = translator.translate(text)
    return translation
