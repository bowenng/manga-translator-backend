from google.cloud import translate_v2 as translate


class Translator:
    def __init__(self):
        self.translate_client = translate.Client()

    def translate(self, text, target_language='eng', output_text_only=True):
        result = self.translate_client.translate(text, target_language=target_language)
        if output_text_only:
            return result['translatedText']

    def translate_blocks(self, blocks, target_language='eng'):
        # TODO: Deep copy
        for block in blocks.blocks:
            block.text = self.translate(block.text, target_language=target_language)
        return blocks

