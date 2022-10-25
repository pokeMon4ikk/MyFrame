from wsgiref.simple_server import make_server

from DousFrame.main import DousFrame
from urls import routes, fronts


application = DousFrame(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...")
    httpd.serve_forever()
