from MangaTranslator.translator import Translator
from MangaTranslator.image_processor import ImageProcessor
from MangaTranslator.ocr import Recognizer


class MangaTranslator:
    def __init__(self, config=r'--oem 3 --psm 6', language='kor'):
        self.translator = Translator()
        self.image_processor = ImageProcessor()
        self.recognizer = Recognizer(config=config, language=language)

    def translate(self, manga_uri):
        manga = self.image_processor.start_processing_image(manga_uri).get_grayscale().finish()
        blocks = self.recognizer.perform_ocr(manga)
        self.recognizer.process(blocks)
        translated_blocks = self.translator.translate_blocks(blocks)
        print(translated_blocks)