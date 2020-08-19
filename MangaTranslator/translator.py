from google.cloud import translate_v2 as translate
from typing import List
import html


class Translator:
    def __init__(self):
        self.translate_client = translate.Client()

    def translate(self,
                  texts: List[str],
                  target_language: str = 'eng') -> List[str]:
        """ Translates a batch of texts

        :param texts: a list of strings to translate
        :param target_language: language to be translated into
        :return: a list of translated strings
        """

        # TODO: Skip English
        if texts is None or len(texts) == 0:
            return []

        translations = self.translate_client.translate(texts, target_language=target_language)

        return [html.unescape(translation['translatedText']) for translation in translations]
