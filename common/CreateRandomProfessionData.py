from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/awu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Profession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profession = db.Column(db.String(10))


db.session.query(Profession).delete()
db.session.commit()

fake = Faker('zh_CN')
cnt = 0
while True:
    profession_name = fake.job()
    if len(profession_name) < 10:
        if profession_name != "其他":
            profession = Profession(profession=profession_name)
            db.session.add(profession)
            cnt = cnt + 1
        if cnt >= 50:
            break

db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
