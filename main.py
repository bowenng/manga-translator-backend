from MangaTranslator.manga_translator import MangaTranslator


if __name__ == '__main__':
    MANGA_DIR = "/Users/bryan/Downloads/oops3.jpg"

    mange_translator = MangaTranslator()
    translated_blocks = mange_translator.translate(MANGA_DIR)
