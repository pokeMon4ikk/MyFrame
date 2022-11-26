from copy import deepcopy
from quopri import decodestring
from patterns.behavioral_patterns import Subject, FileWriter
from patterns.architectural_system_pattern_unit_of_work import DomainObject
from sqlite3 import connect


class User:
    def __init__(self, first_name, last_name, short_info):
        self.first_name = first_name
        self.last_name = last_name
        self.short_info = short_info


class Client(User):
    pass


class Author(User, DomainObject):
    def __init__(self, first_name, last_name, short_info):
        self.books = []
        super().__init__(first_name, last_name, short_info)


class UserCreator:
    types = {
        'client': Client,
        'author': Author
    }

    @classmethod
    def create(cls, type_, first_name, last_name, short_info):
        return cls.types[type_](first_name, last_name, short_info)


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
    def create_user(type_, first_name, last_name, short_info):
        return UserCreator.create(type_, first_name, last_name, short_info)

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


class AuthorMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.tablename = 'author'

    def all(self):
        statement = f'SELECT * from {self.tablename}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, first_name, last_name, short_info = item
            author = Author(first_name, last_name, short_info)
            author.id = id
            result.append(author)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, first_name FROM {self.tablename} WHERE id=?," \
                    f"SELECT id, last_name  FROM {self.tablename} WHERE id=?," \
                    f"SELECT id, short_info FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Author(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.tablename} (first_name) VALUES (?)" \
                    f"INSERT INTO {self.tablename} (last_name) VALUES (?)" \
                    f"INSERT INTO {self.tablename} (short_info) VALUES (?)"

        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.short_info,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.tablename} SET first_name=? WHERE id=?" \
                    f"UPDATE {self.tablename} SET last_name=? WHERE id=?" \
                    f"UPDATE {self.tablename} SET short_info=? WHERE id=?"

        self.cursor.execute(statement, (obj.first_name, obj.last_name, obj.short_info, obj.id, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.tablename} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = connect('DousFrameDb.sqlite')


# архитектурный системный паттерн - Data Mapper
class MapperRegistry:
    mappers = {
        'author': AuthorMapper,
    }

    @staticmethod
    def get_mapper(obj):

        if isinstance(obj, Author):

            return AuthorMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')
