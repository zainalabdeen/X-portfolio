from . import db
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from flask import request, session
from werkzeug.security import check_password_hash, generate_password_hash
from .helpers import Helper


class Users(db.Model):
    __tablename__ = 'users'
    __rec_name__ = 'fullname'

    id = db.Column(db.Integer, primary_key=True)
    sex = db.Column(db.String(50),nullable=False)
    phone = db.Column(db.String(50),nullable=False)
    address = db.Column(db.String(100),nullable=False)
    birthday = db.Column(db.Date,nullable=False)
    degree = db.Column(db.String(100),nullable=False)
    freelance = db.Column(db.String(100),nullable=False)
    email =db.Column(db.String(100),nullable=False)
    fullname = db.Column(db.String(100),nullable=False)
    hash = db.Column(db.String,nullable=False)
    years_of_experience = db.Column(db.Integer)
    happy_clients = db.Column(db.Integer)
    projects = db.Column(db.Integer)
    description = db.Column(db.String)
    twitter = db.Column(db.String(50),nullable=True)
    facebook = db.Column(db.String(50),nullable=True)
    instagram = db.Column(db.String(50),nullable=True)
    linkedin = db.Column(db.String(50),nullable=True)
    titles = db.relationship('Titles', backref='users')
    skills = db.relationship('Skills', backref='users')
    interests = db.relationship('Interests', backref='users')
    educations = db.relationship('Educations', backref='users')
    experiences = db.relationship('Experiences', backref='users')
    contacts = db.relationship('Contacts', backref='users')


    def to_json(self):
        return {
            'id': self.id,
            'sex': self.sex,
            'phone': self.phone,
            'address': self.address,
            'birthday': self.birthday,
            'degree': self.degree,
            'freelance': self.freelance,
            'email': self.email,
            'fullname': self.fullname,
            'description' : self.description,
            'years_of_experience': self.years_of_experience,
            'happy_clients': self.happy_clients,
            'projects': self.projects
        }

    def json_create(self,json):
        hashed_password = generate_password_hash(json.get("password"))
        rec = self(
            sex = json.get('sex'),
            phone = json.get('phone'),
            address = json.get('address'),
            birthday =  Helper.from_string(json.get('birthday')),
            degree = json.get('degree'),
            freelance =  "Available",
            email = json.get('email'),
            fullname = json.get('fullname'),
            description = json.get('description'),
            years_of_experience = json.get('years_of_experience',0),
            happy_clients = json.get('happy_clients',0),
            projects = json.get('projects',0),
            twitter = json.get('twitter',''),
            facebook = json.get('facebook',''),
            instagram = json.get('instagram',''),
            linkedin = json.get('linkedin',''),
            hash = hashed_password
            )
        return rec

    def json_edit(self,json):
        self.sex = json.get('sex',self.sex)
        self.phone = json.get('phone',self.phone)
        self.address = json.get('address',self.address)
        if json.get('birthday',False):
            self.birthday = Helper.from_string(json.get('birthday')),
        self.degree = json.get('degree',self.degree)
        self.freelance =  json.get('freelance',self.freelance)
        self.fullname = json.get('fullname',self.fullname)
        self.description = json.get('description',self.description)
        self.years_of_experience = json.get('years_of_experience',self.years_of_experience)
        self.happy_clients = json.get('happy_clients',self.happy_clients)
        self.projects = json.get('projects',self.projects)
        self.twitter = json.get('twitter',self.twitter)
        self.facebook = json.get('facebook',self.facebook)
        self.instagram = json.get('instagram',self.instagram)
        self.linkedin = json.get('linkedin',self.linkedin)
        return self

    def check_user_password(self,plain_password):
        if not plain_password:
            return False
        return check_password_hash(self.hash,plain_password)

    def change_user_password(self,json):
        hashed_password = generate_password_hash(json.get("password"))
        self.hash = hashed_password
        return self

class Skills(db.Model):
    __tablename__ = 'skills'
    __rec_name__ = 'name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    percent = db.Column(db.Integer)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'percent': self.percent,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('name'):
            raise Exception("You Should Provide Name")
        if  int(json.get('percent')) < 1 or int(json.get('percent')) > 100:
            raise Exception("Percent Should be between 1-100")
        rec = self(
            name = json.get('name'),
            percent = int(json.get('percent')),
            user_id = session["user_id"]
        )
        return rec

    def json_edit(self,json):
        self.name = json.get('name',self.name)
        self.percent = json.get('percent',self.percent)
        return self

class Titles(db.Model):
    __tablename__ = 'titles'
    __rec_name__ = 'name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('name'):
            raise Exception("You Should Provide Name")
        rec = self(
            name = json.get('name'),
            user_id = session["user_id"]
        )
        return rec

    def json_edit(self,json):
        self.name = json.get('name',self.name)
        return self

    def get_items(self):
        items = []
        for rec in self:
            items.append(rec.name)
        return ''.join(items)

class Interests(db.Model):
    __tablename__ = 'interests'
    __rec_name__ = 'name'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('name'):
            raise Exception("You Should Provide Name")
        rec = self(
            name = json.get('name'),
            user_id = session["user_id"]
        )
        return rec

    def json_edit(self,json):
        self.name = json.get('name',self.name)
        return self

class Educations(db.Model):
    __tablename__ = 'educations'
    __rec_name__ = 'title'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    institute_name = db.Column(db.String,nullable=False)
    date_from = db.Column(db.Date,nullable=False)
    date_to = db.Column(db.Date,nullable=True)
    description = db.Column(db.String)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('title'):
            raise Exception("You Should Provide Name")
        if not json.get('institute_name'):
            raise Exception("You Should Provide Institute Name")
        rec = self(
            title = json.get('title'),
            institute_name = json.get('institute_name'),
            description = json.get('description'),
            date_from = Helper.from_string(json.get('date_from')),
            date_to = Helper.from_string(json.get('date_to')),
            user_id = session["user_id"]
        )
        return rec

    def json_edit(self,json):
        self.title = json.get('title',self.title)
        self.institute_name = json.get('institute_name',self.institute_name)
        self.date_from = Helper.from_string(json.get('date_from',self.date_from))
        self.date_to = Helper.from_string(json.get('date_to',self.date_to))
        self.description = json.get('description',self.description)
        return self

class Experiences(db.Model):
    __tablename__ = 'experiences'
    __rec_name__ = 'title'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,nullable=False)
    company = db.Column(db.String,nullable=False)
    description = db.Column(db.String)
    date_from = db.Column(db.Date,nullable=False)
    date_to = db.Column(db.Date,nullable=True)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('title'):
            raise Exception("You Should Provide Title")
        if not json.get('company'):
            raise Exception("You Should Provide Company")
        rec = self(
            title = json.get('title'),
            company = json.get('company'),
            description = json.get('description'),
            date_from = Helper.from_string(json.get('date_from')),
            date_to = Helper.from_string(json.get('date_to')),
            user_id = session["user_id"]
        )
        return rec

    def json_edit(self,json):
        self.title = json.get('title',self.title)
        self.company = json.get('company',self.company)
        self.description = json.get('description',self.description)
        self.date_from = Helper.from_string(json.get('date_from',self.date_from))
        self.date_to = Helper.from_string(json.get('date_to',self.date_to))
        return self

class Contacts(db.Model):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False)
    subject = db.Column(db.String(500),nullable=False)
    message = db.Column(db.String,nullable=False)
    user_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message,
            'user_id': self.user_id
        }

    def json_create(self,json):
        if not json.get('name'):
            raise Exception("You Should Provide Name")
        rec = self(
            name = json.get('name'),
            user_id = json.get('user_id'),
            email = json.get('email'),
            subject = json.get('subject'),
            message = json.get('message')
        )
        return rec

    def json_edit(self,json):
        self.name = json.get('name',self.name)
        self.user_id = json.get('user_id',self.user_id)
        self.email = json.get('email',self.email)
        self.subject = json.get('subject',self.subject)
        self.message = json.get('message',self.message)
        return self
