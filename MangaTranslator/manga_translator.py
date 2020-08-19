from MangaTranslator.translator import Translator
from MangaTranslator.image_processor import ImageProcessor
from MangaTranslator.ocr import Recognizer
from MangaTranslator.ocr import Blocks

import cv2
import numpy as np
import textwrap
from typing import List


class MangaTranslator:
    FILL = -1

    def __init__(self):
        self.translator = Translator()
        self.image_processor = ImageProcessor()
        self.recognizer = Recognizer()

        self.font_face = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 1
        self.estimate_character = 's'
        self.text_color = (0, 0, 0)

        self.text_background = (255, 255, 255)

    def translate(self,
                  manga_blob: bytes) -> bytes:
        """ Translates a manga encoded as bytes

        :param manga_blob: manga to translate
        :return: translated manga
        """

        ocr_blocks = self.recognizer.perform_ocr(manga_blob)
        translations = self.translator.translate(ocr_blocks.text_list())
        translated_blocks = ocr_blocks.translated(translations)

        manga = self.read_image_from_blob(manga_blob)

        manga = self.remove_text(manga, translated_blocks)
        manga = self.write_text(manga, translated_blocks)

        manga_encoded = cv2.imencode('.png', manga)
        if manga_encoded[0]:
            return manga_encoded[1].tobytes()
        else:
            raise ValueError("Error while translating manga")

    def read_image_from_blob(self,
                             blob: bytes) -> np.ndarray:
        """ Decodes an image

        :param blob: bytes representing an image
        :return: decoded image as a numpy array
        """

        # convert string data to numpy array
        npimg = np.fromstring(blob, np.uint8)
        # convert numpy array to image
        return cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    def remove_text(self,
                    image: np.ndarray,
                    blocks: Blocks) -> np.ndarray:
        """ Remove existing texts from a manga

        :param image: manga containing texts
        :param blocks: containing bounding boxes of texts
        :return: manga with texts removed
        """

        # TODO: Use background color
        for block in blocks:
            vertices = block.bounding_box.vertices
            start, end = (vertices[0].x, vertices[0].y), (vertices[2].x, vertices[2].y)
            image = cv2.rectangle(image,
                                  start,
                                  end,
                                  self.text_background,
                                  MangaTranslator.FILL)
        return image

    def write_text(self,
                   image: np.ndarray,
                   blocks: Blocks) -> np.ndarray:
        """

        :param image: manga without text
        :param blocks: blocks containing translations and bounding boxes
        :return: manga with translations
        """

        for block in blocks:
            lines = self.wrap_text(block.text, block.bounding_box)
            origin = (block.bounding_box.vertices[0].x, block.bounding_box.vertices[0].y)
            for line in lines:
                origin = self.new_line(origin)
                image = cv2.putText(image,
                                    line,
                                    origin,
                                    self.font_face,
                                    self.font_scale,
                                    self.text_color,
                                    self.font_thickness,
                                    cv2.LINE_AA)

        return image

    def wrap_text(self,
                  text: str,
                  bounding_box: Blocks) -> List[str]:
        (char_width, char_height), baseline = cv2.getTextSize(text=self.estimate_character,
                                                              fontFace=self.font_face,
                                                              fontScale=self.font_scale,
                                                              thickness=self.font_thickness)
        width = bounding_box.vertices[1].x - bounding_box.vertices[0].x
        max_num_chars = max(width // char_width, 1)
        return textwrap.wrap(text, max_num_chars)

    def get_line_height(self) -> int:
        (char_width, char_height), baseline = cv2.getTextSize(text=self.estimate_character,
                                                              fontFace=self.font_face,
                                                              fontScale=self.font_scale,
                                                              thickness=self.font_thickness)
        return char_height + baseline

    def new_line(self, origin: (int, int)) -> (int, int):
        return origin[0], origin[1] + self.get_line_height()
