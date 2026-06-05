import zlib
import base64

def decode():
    """Decode a Flask cookie."""
    try:
        compressed = False
        payload = ".eJxlizEKwzAMRa_iajYdMvoG7VS6lhCErTgCRQbL7hJy9xg6dvoP3vsHLKugbWQQPge4NgZ2MsNM4OGhXxROLlZKpI1RDObT_4dvymytYuOiznqMw6xdbu4lhEZOSma9j-_soRvVhROE6ceKO0GAZ9l0gvMCZHwx_g.afNA3Q.OckvhW0WjIaV5SOI0vQZZI1MzzQ"
        # The original cookie could have been extracted and used to login here.

        if payload.startswith('.'):
            compressed = True
            payload = payload[1:]

        data = payload.split(".")[0]

        data = base64.urlsafe_b64decode(data)
        if compressed:
            data = zlib.decompress(data)

        return data.decode("utf-8")
    except Exception as e:
        return "[Decoding error: are you sure this was a Flask session cookie? {}]".format(e)

if __name__ == "__main__":
        print(decode())
