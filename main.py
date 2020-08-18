from MangaTranslator.manga_translator import MangaTranslator


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MANGA_DIR = "/Users/bryan/Downloads/oops5.jpg"
    CONFIG = r'--oem 3 --psm 6'
    LANGUAGE = 'kor'
    THRESHOLD = 60

    mange_translator = MangaTranslator(config=CONFIG, language=LANGUAGE, threshold=THRESHOLD)
    translated_blocks = mange_translator.translate(MANGA_DIR)
