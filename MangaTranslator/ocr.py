from google.cloud import vision


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

    def add_padding(self, max_width, max_height):
        PADDING_SCALE = (
            (-1, -1),
            (1, -1),
            (1, 1),
            (-1, 1)
        )
        padding = min(max_width // 100 * 2, max_height // 100 * 2)
        for block in self.blocks:
            vertices = block.bounding_box.vertices
            for i, vertex in enumerate(vertices):
                new_x = vertex.x + PADDING_SCALE[i][0] * padding
                new_y = vertex.y + PADDING_SCALE[i][0] * padding
                if 0 <= new_x <= max_width:
                    vertex.x = new_x
                if 0 <= new_y <= max_height:
                    vertex.y = new_y




    def __repr__(self):
        description = '[\n'
        for block in self.blocks:
            description += f'\t{block}\n'
        description += ']'
        return description

    def __iter__(self):
        return iter(self.blocks)


class Recognizer:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()

    def perform_ocr(self, content: bytes) -> Blocks:
        """ Detects texts in the file

        :param content: bytes representing an image
        :return: blocks containing texts
        """

        image = vision.types.Image(content=content)

        response = self.client.text_detection(image=image)

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return Blocks.from_ocr_annotations(response.full_text_annotation)
