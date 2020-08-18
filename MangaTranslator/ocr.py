import pytesseract
from PIL import Image


class Recognizer:
    def __init__(self, config=r'--oem 3 --psm 6', language='kor'):
        self.config = config
        self.language = language

    def perform_ocr(self, image):
        data = pytesseract.image_to_data(image,
                                         config=self.config,
                                         lang=self.language,
                                         output_type=pytesseract.Output.DICT)
        return Blocks(data)

    def process(self, blocks):
        # filter out low confidence blocks
        blocks.filter_invalidate_blocks()
        # combine words of the same block and the same line together
        blocks.sort_and_combine_words()
        return blocks

class Block:
    params = ['level', 'block_num', 'line_num', 'word_num', 'top', 'left', 'width', 'height', 'conf', 'text']
    def __init__(self, level, block_num, line_num, word_num, top, left, width, height, conf, text):
        self.level = level
        self.block_num = block_num
        self.line_num = line_num
        self.word_num = word_num
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        self.conf = conf
        self.text = text

    def __repr__(self):
        return f"text: {self.text}, block: {self.block_num}, line: {self.line_num}, word: {self.word_num}, conf: {self.conf}"


class Blocks:
    INVALID_CONF = '-1'

    def __init__(self, output_dict):
        size = len(output_dict['text'])
        blocks = []

        for i in range(size):
            params = []
            for param in Block.params:
                params.append(output_dict[param][i])
            blocks.append(Block(*params))

        self.blocks = blocks

    def filter_invalidate_blocks(self, conf_threshold=71):
        self.blocks = list(filter(lambda block: block.conf != Blocks.INVALID_CONF and block.conf >= conf_threshold, self.blocks))

    def sort(self):
        self.blocks.sort(key=lambda block: (block.block_num, block.line_num, block.word_num))

    def sort_and_combine_words(self):
        def combine(block_source, block_target):
            block_source.text += block_target.text
        self.sort()
        write_index = 0
        for read_index in range(1, len(self.blocks)):
            write_block = self.blocks[write_index]
            read_block = self.blocks[read_index]
            if write_block.block_num == read_block.block_num and write_block.line_num == read_block.line_num:
                combine(write_block, read_block)
            else:
                write_index += 1
                self.blocks[write_index] = read_block
        self.blocks = self.blocks[:write_index+1]

    def __repr__(self):
        description = '[\n'
        for block in self.blocks:
            description += f'\t{block}\n'
        description += ']'
        return description

