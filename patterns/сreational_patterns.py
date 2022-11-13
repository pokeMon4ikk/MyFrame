from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject, FileWriter


class User:
    def __init__(self, name):
        self.name = name


class Client(User):
    pass


class Author(User):
    def __init__(self, name):
        self.books = []
        super().__init__(name)


class UserCreator:
    types = {
        'client': Client,
        'author': Author
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class BookPrototype:
    def clone(self):
        return deepcopy(self)


class Book(BookPrototype, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.books.append(self)
        self.authors = []
        super().__init__()

    def __getitem__(self, item):
        return self.authors[item]

    def add_author(self, author: Author):
        self.authors.append(author)
        author.books.append(self)
        self.notify()


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
        self.authors = []
        self.books = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserCreator.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_book(type_, name, category):
        return BookCreator.create(type_, name, category)

    def get_book(self, name):
        for item in self.books:
            if item.name == name:
                return item
        return None

    def get_author(self, name) -> Author:
        for item in self.authors:
            if item.name == name:
                return item

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

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
