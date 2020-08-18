from google.cloud import translate_v2 as translate


class Translator:
    def __init__(self):
        self.translate_client = translate.Client()

    def translate(self, text, target_language='eng'):
        translations = self.translate_client.translate(text, target_language=target_language)

        if isinstance(text, str):
            return translations['translatedText']
        else:
            return [translation['translatedText'] for translation in translations]