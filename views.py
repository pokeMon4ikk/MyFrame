from DousFrame.templator import render
from patterns.сreational_patterns import Engine, Logger

site = Engine()
logger = Logger('main')


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


class Orders:
    def __call__(self, request):
        return '200 OK', render('orders.html', objects_list=site.categories)


class AboutUs:
    def __call__(self, request):
        return '200 OK', render('about_us.html')


class Login:
    def __call__(self, request):
        return '200 OK', render('login.html')


class Registration:
    def __call__(self, request):
        return '200 OK', render('registration.html')


class BooksList:
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


class AddBook:
    category_id = -1

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


class AddCategory:
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


class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)

