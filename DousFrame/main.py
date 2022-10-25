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

        for front in self.front_items:
            front(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
