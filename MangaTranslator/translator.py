from google.cloud import translate_v2 as translate
import html


class Translator:
    def __init__(self):
        self.translate_client = translate.Client()

    def translate(self, text, target_language='eng'):
        # TODO: Skip English
        if text is None or len(text) == 0:
            return []

        translations = self.translate_client.translate(text, target_language=target_language)

        if isinstance(text, str):
            return [html.unescape(translations['translatedText'])]
        else:
            return [html.unescape(translation['translatedText']) for translation in translations]