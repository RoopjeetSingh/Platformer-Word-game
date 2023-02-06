import base64
from io import BytesIO, StringIO


def decode_file(encoded_var):
    byte_data = base64.b64decode(encoded_var)
    image_data = BytesIO(byte_data)
    return image_data
