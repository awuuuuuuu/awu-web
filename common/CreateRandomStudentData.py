from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
import random

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/awu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(10))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    sex = db.Column(db.String(2))
    age = db.Column(db.Integer)
    origin = db.Column(db.String(10))
    profession_id = db.Column(db.Integer, db.ForeignKey('profession.id'))


db.session.query(Student).delete()
db.session.commit()

result = db.session.query(Profession).all()
profession_id_list = []
for profession in result:
    profession_id_list.append(profession.id)

fake = Faker('zh_CN')
cnt = 0
while True:
    name = fake.name()[:3]
    sex = random.choice(["男", "女"])
    age = random.randint(18, 25)
    origin = fake.city()
    profession_id = random.choice(profession_id_list)
    if origin[-1] == '市':
        student = Student(name=name, sex=sex, age=age, origin=origin, profession_id=profession_id)
        db.session.add(student)
        cnt = cnt + 1
    if cnt >= 1000:
        break

db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
