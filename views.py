from DousFrame.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html')


class Orders:
    def __call__(self, request):
        return '200 OK', render('orders.html')


class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html')


class Login:
    def __call__(self, request):
        return '200 OK', render('login.html')


class Registration:
    def __call__(self, request):
        return '200 OK', render('registration.html')

