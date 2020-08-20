from MangaTranslator.manga_translator import MangaTranslator
from google.cloud import error_reporting
import base64
import flask
import io


def translate_image(request: flask.Request) -> flask.Response:
    """ Translates a manga

    :param request: flask request object with an image file "manga"
    :return: flask response with base64 encoded png on success OR error message on failure
    """

    error_report_client = error_reporting.Client()

    try:
        image = request.files['manga'].read()

        if image:
            translator = MangaTranslator()
            translated_manga = translator.translate(image)
            encoded_translated_manga = base64.b64encode(translated_manga)
            response = flask.make_response((encoded_translated_manga, 200, {'Content-Type' : 'image/png'}))
            return response
        else:
            return flask.make_response(('Invalid Argument', 406))

    except Exception:
        error_report_client.report_exception()
        return flask.make_response(('Failed to process manga :(', 500))


if __name__ == '__main__':
    MANGA_DIR = "/Users/bryan/Downloads/oops2.jpg"

    with io.open(MANGA_DIR, 'rb') as image_file:
        content = image_file.read()

    mange_translator = MangaTranslator()
    manga = mange_translator.translate(content)

    with io.open("manga.png", 'wb') as image_out:
        image_out.write(manga)
