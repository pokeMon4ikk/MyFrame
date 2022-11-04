from DousFrame.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug

site = Engine()
logger = Logger('main')
routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/orders/')
class Orders:
    @Debug(name='Order')
    def __call__(self, request):
        return '200 OK', render('orders.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/about_us/')
class AboutUs:
    @Debug(name='AboutUs')
    def __call__(self, request):
        return '200 OK', render('about_us.html')


@AppRoute(routes=routes, url='/login/')
class Login:
    @Debug(name='Login')
    def __call__(self, request):
        return '200 OK', render('login.html')


@AppRoute(routes=routes, url='/registration/')
class Registration:
    @Debug(name='Registration')
    def __call__(self, request):
        return '200 OK', render('registration.html')


@AppRoute(routes=routes, url='/books_list/')
class BooksList:
    @Debug(name='BooksList')
    def __call__(self, request):
        logger.log('Список книг')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('books_list.html',
                                    objects_list=category.books,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'Empty'


@AppRoute(routes=routes, url='/add_book/')
class AddBook:
    category_id = -1

    @Debug(name='AddBook')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                book = site.create_book('record', name, category)
                site.books.append(book)
            return '200 OK', render('books_list.html',
                                    objects_list=category.books,
                                    name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('add_book.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Empty'


@AppRoute(routes=routes, url='/add_category/')
class AddCategory:
    @Debug(name='AddCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('add_category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category_list/')
class CategoryList:
    @Debug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)

