from flask import Blueprint, render_template, request, session, jsonify

from common.utils import send_email, gen_email_code

import hashlib
from model.User import User

UserController = Blueprint("UserController", __name__)


@UserController.route("/login")
def login():
    return render_template("login.html")


@UserController.route("/register")
def register():
    return render_template("register.html")


@UserController.route("/sendVerificationCode", methods=["POST", "GET"])
def sendVerificationCode():
    data = request.get_json(force=True)

    email = data["email"]
    code = gen_email_code()
    try:
        send_email(email, code)
        session["ecode"] = code
        print("已发送， 验证码：" + session.get("ecode"))
        return jsonify(error_message="success")
    except:
        return jsonify(error_message="error")


@UserController.route("/Register", methods=["POST", "GET"])
def Register():
    data = request.get_json(force=True)
    username = data["username"]
    password = data["password"]
    email = data["email"]
    verificationCode = data["verificationCode"]

    if verificationCode != session.get("ecode"):
        return jsonify(error_message="验证码错误")

    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    password = sha256.hexdigest()

    try:
        user = User()
        user.add_one_user(username, password, email)
        return jsonify(error_message="success")
    except:
        return jsonify(error_message="数据库拒绝插入")


@UserController.route("/Login", methods=["POST", "GET"])
def Login():
    data = request.get_json(force=True)
    username = data["username"]
    password = data["password"]

    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    password = sha256.hexdigest()

    user = User().find_user_by_username(username)
    if user and user.username == username and user.password == password:
        session['is_login'] = 'true'
        session['userid'] = user.id
        session['username'] = user.username
        return jsonify(error_message="success")
    else:
        return jsonify(error_message="用户名或者密码错误")


@UserController.route("/logout", methods=["POST", "GET"])
def logout():
    try:
        session.pop('is_login')
        session.pop('userid')
        session.pop('username')
        return jsonify(error_message="success")
    except:
        return jsonify(error_message="error")
