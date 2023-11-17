from common.database import *


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    username = Column(String(50))
    password = Column(String(100))
    email = Column(String(50))

    def add_one_user(self, username, password, email):
        user = User(username=username, password=password, email=email)
        db_session.add(user)
        db_session.commit()
        print("add user successfully")

    def query_all_users(self):
        user_list = db_session.query(User).all()
        for user in user_list:
            print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}")

    def find_user_by_username(self, username):
        return db_session.query(User).filter_by(username=username).first()
