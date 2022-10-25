from DousFrame.myRequests import PostRequest, GetRequest
from quopri import decodestring


class PageNotFound404:
    def __call__(self, request):
        return '404', '404 - ERROR\n  There are not such page!'


class DousFrame:
    def __init__(self, routes, front_items):
        self.routes = routes
        self.front_items = front_items

    def __call__(self, environ, start_response):

        path = environ["PATH_INFO"]

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequest().get_request(environ)
            request['data'] = DousFrame.decode_value(data)
            print(f'Нам пришёл post-запрос: {DousFrame.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequest().get_request(environ)
            request['request_params'] = DousFrame.decode_value(request_params)
            print(f'Нам пришли GET-параметры:'
                  f' {DousFrame.decode_value(request_params)}')

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        for front in self.front_items:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            value_string = decodestring(val).decode('UTF-8')
            new_data[key] = value_string
        return new_data
