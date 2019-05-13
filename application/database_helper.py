from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import logging
log_info = logging.getLogger('infoLog')
log_debug = logging.getLogger('debuggerLog')
log_error = logging.getLogger('errorLog')
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String)
    city = Column(String)
    phone = Column(String)


class Database:
    def __init__(self, driver, username, password, host, port, db_name):
        self.driver = driver
        self.username = username
        self. password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.session = None
        self.engine = None
        self.conn = None
        self._create_engine()
        self.connect()

    def _create_engine(self):
        self.engine = create_engine(self.driver+"://"+self.username+":"+self.password+"@" +
                                    self.host+":"+str(self.port)+"/"+self.db_name)

    def connect(self):
        if self.engine is None:
            self._create_engine()
        self.conn = self.engine.connect()
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def _add_entry(self, entry):
        self.session.add(entry)
        self.session.commit()

    def add_user(self, name, email, city, phone):
        query = "INSERT INTO users (name, email, city, phone) VALUES (%s, %s, %s, %s) RETURNING *"
        exc = self.conn.execute(query, (name, email, city, phone))
        print("INSERTED ENTRY", exc.fetchall)

    def read_users(self):
        query = "SELECT * FROM users"
        exc = self.conn.execute(query)
        print("---" * 10)
        for entry in exc.fetchall():
            print("ID:", entry[0])
            print("Name:", entry[1])
            print("Email:", entry[2])
            print("City:", entry[3])
            print("Phone:", entry[4])
            print("---"*10)

    def read_user(self, _id):
        query = "SELECT * FROM users WHERE id={}".format(_id)
        exc = self.conn.execute(query)
        print("---" * 10)
        for entry in exc.fetchall():
            print("ID:", entry[0])
            print("Name:", entry[1])
            print("Email:", entry[2])
            print("City:", entry[3])
            print("Phone:", entry[4])
            print("---" * 10)
