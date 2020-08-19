from MangaTranslator.manga_translator import MangaTranslator
import flask
import io
import json


def translate_image(request):
    """Responds to any HTTP request.
    Args:
       request (flask.Request): HTTP request object.
    Returns:
       The response text or any set of values that can be turned into a
       Response object using
       `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """

    #image = request.data
    return json.dumps(request)
    # if image:
    #     translator = MangaTranslator()
    #     translated_manga = translator.translate(image)
    #
    #     response = flask.make_response((translated_manga, '200', {'Content-Type' : 'image/png'}))
    #
    #     return response
    # else:
    #     return flask.make_response(('Invalid Argument', '406'))


if __name__ == '__main__':
    MANGA_DIR = "/Users/bryan/Downloads/oops3.jpg"

    with io.open(MANGA_DIR, 'rb') as image_file:
        content = image_file.read()

    mange_translator = MangaTranslator()
    translated_blocks = mange_translator.translate(content)
