from datetime import date
from views import Index, Orders, AboutUs, Login, Registration


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/orders/': Orders(),
    '/about_us/': AboutUs(),
    '/login/': Login(),
    '/registration/': Registration()
}
