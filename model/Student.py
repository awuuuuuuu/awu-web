from flask import jsonify
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from common.database import *


class Profession(Base):
    __tablename__ = 'profession'
    id = Column(Integer, primary_key=True)
    profession = Column(String(10))


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    name = Column(String(10))
    sex = Column(String(2))
    age = Column(Integer)
    origin = Column(String(10))
    profession_id = Column(Integer, ForeignKey('profession.id'))
    profession = relationship('Profession', backref='student')

    def add_one_student(self, name, sex, age, origin, profession_id):
        student = Student(name=name, sex=sex, age=age, origin=origin, profession_id=profession_id)
        db_session.add(student)
        db_session.commit()
        print("add student successfully")

    def filter_student_by_name(self, name):
        return db_session.query(Student).filter_by(name=name)

    def filter_student_by_sex(self, sex):
        return db_session.query(Student).filter_by(sex=sex)

    def filter_student_by_origin(self, origin):
        return db_session.query(Student).filter_by(origin=origin)

    def filter_student_by_profession_id(self, profession_id):
        return db_session.query(Student).filter_by(profession_id=profession_id)
