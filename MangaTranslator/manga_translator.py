from MangaTranslator.translator import Translator
from MangaTranslator.image_processor import ImageProcessor
from MangaTranslator.ocr import Recognizer
import cv2


class MangaTranslator:
    def __init__(self, config=r'--oem 3 --psm 6', language='kor', threshold=71):
        self.translator = Translator()
        self.image_processor = ImageProcessor()
        self.recognizer = Recognizer(config=config, language=language, threshold=threshold)

    def translate(self, manga_uri):
        ocr_blocks = self.recognizer.perform_ocr(manga_uri)
        translations = self.translator.translate(ocr_blocks.text_list())
        translated_blocks = ocr_blocks.translated(translations)
        print(translated_blocks)
