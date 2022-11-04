from copy import deepcopy
from quopri import decodestring


class User:
    pass


class Client(User):
    pass


class Admin(User):
    pass


class UserCreator:
    types = {
        'client': Client,
        'Admin': Admin
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class BookPrototype:
    def clone(self):
        return deepcopy(self)


class Book(BookPrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.books.append(self)


class Fairytale(Book):
    pass


class Romance(Book):
    pass


class BookCreator:
    types = {
        'fairytale': Fairytale,
        'romance': Romance
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category:
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.books = []

    def books_count(self):
        result = len(self.books)
        if self.category:
            result += self.category.books_count()
        return result


class Engine:
    def __init__(self):
        self.clients = []
        self.admins = []
        self.books = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserCreator.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    @staticmethod
    def create_book(type_, name, category):
        return BookCreator.create(type_, name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    def get_book(self, name):
        for item in self.books:
            if item.name == name:
                return item
        return None

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
