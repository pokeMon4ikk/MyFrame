class GetRequest:

    @staticmethod
    def parse_data(data: str):
        result = {}
        if data:
            data_items = data.split("&")
            for item in data_items:
                key, value = item.split("=")
                result[key] = value
        return result

    @staticmethod
    def get_request(environ):
        query_string = environ['QUERY_STRING']
        get_request = GetRequest.parse_data(query_string)
        return get_request


class PostRequest:

    @staticmethod
    def parse_data(data: str):
        result = {}
        if data:
            data_items = data.split("&")
            for item in data_items:
                key, value = item.split("=")
                result[key] = value
        return result

    @staticmethod
    def get_wsgi_data(environ) -> bytes:
        data_length = environ.get('CONTENT_LENGTH')
        content_length = int(data_length) if data_length else 0
        print(content_length)

        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_data(self, data: bytes) -> dict:
        result = {}
        if data:
            data_string_format = data.decode(encoding="utf-8")
            result = self.parse_data(data_string_format)

        return result

    def get_request(self, environ):
        data = self.get_wsgi_data(environ)
        data = self.parse_wsgi_data(data)
        return data
