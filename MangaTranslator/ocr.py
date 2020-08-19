from google.cloud import vision
import io


class Recognizer:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()


    def perform_ocr(self, content):
        """Detects text in the file."""

        image = vision.types.Image(content=content)

        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return Blocks.from_ocr_annotations(response.full_text_annotation)


class Block:

    def __init__(self, text, bounding_box, confidence):
        self.text = text
        self.bounding_box = bounding_box
        self.confidence = confidence

    def __repr__(self):
        return f"text: {self.text} confidence: {self.confidence}"


class Blocks:

    def __init__(self, blocks):
        self.blocks = blocks

    @staticmethod
    def from_ocr_annotations(ocr_annotations):

        def extract_text(block):
            text_list = []
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        text_list.append(symbol.text)
            return ''.join(text_list)

        blocks = []

        for page in ocr_annotations.pages:
            for block in page.blocks:
                text = extract_text(block)
                bounding_box = block.bounding_box
                confidence = block.confidence
                blocks.append(Block(text, bounding_box, confidence))

        return Blocks(blocks)

    def translated(self, translations):
        blocks = []
        for i in range(len(translations)):
            text = translations[i]
            bounding_box = self.blocks[i].bounding_box
            confidence = self.blocks[i].confidence
            blocks.append(Block(text, bounding_box, confidence))
        return Blocks(blocks)

    def text_list(self):
        return [block.text for block in self.blocks]

    def __repr__(self):
        description = '[\n'
        for block in self.blocks:
            description += f'\t{block}\n'
        description += ']'
        return description

    def __iter__(self):
        return iter(self.blocks)

