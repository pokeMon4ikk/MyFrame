from DousFrame.templator import render
from patterns.architectural_system_pattern_unit_of_work import UnitOfWork
from patterns.сreational_patterns import Engine, Logger, MapperRegistry
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import EmailNotifier, SmsNotifier, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:

                category = site.find_category_by_id(int(self.category_id))

                book = site.create_book('record', name, category)

                book.observers.append(email_notifier)
                book.observers.append(sms_notifier)

                site.books.append(book)

            return '200 OK', render('books_list.html',
                                    objects_list=category.books,
                                    name=category.name,
                                    id=category.id)

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
            return '200 OK', render('add_category.html', objects_list=site.categories)
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


@AppRoute(routes=routes, url='/authors_list/')
class AuthorListView(ListView):
    template_name = 'authors_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('author')
        return mapper.all()


@AppRoute(routes=routes, url='/create_author/')
class AuthorCreateView(CreateView):
    template_name = 'create_author.html'

    def create_obj(self, data: dict):
        first_name = data['first_name']
        last_name = data['last_name']
        short_info = data['short_info']
        first_name = site.decode_value(first_name)
        last_name = site.decode_value(last_name)
        short_info = site.decode_value(short_info)
        new_obj = site.create_user("author", first_name, last_name, short_info)
        site.authors.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add_author/')
class AddAuthorByBookCreateView(CreateView):
    template_name = 'add_author.html'

    def get_template(self):
        context = super().get_context_data()
        context['books'] = site.books
        context['authors'] = site.authors
        return context

    def create_obj(self, data: dict):
        book_name = data['book_name']
        book_name = site.decode_value(book_name)
        book = site.get_book(book_name)
        author_name = data['author_name']
        author_name = site.decode_value(author_name)
        author = site.get_author(author_name)
        book.add_author(author)


@AppRoute(routes=routes, url='/api/')
class BookApi:
    @Debug(name='BookApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.books).save()
