import secrets

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


@app.route("/")
def main():
    return render_template("index.html")


from controller.UserController import UserController
from controller.StudentController import StudentController

app.register_blueprint(UserController)
app.register_blueprint(StudentController)

if __name__ == "__main__":
    app.run(debug=True)
