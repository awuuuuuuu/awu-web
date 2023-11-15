from flask import Blueprint, render_template, session, request, jsonify
from sqlalchemy.orm import exc

from model.Student import Student, Profession
from common.database import *

StudentController = Blueprint("StudentController", __name__)

student = Student()


@StudentController.route("/student")
def studentIndex():
    if 'is_login' in session and session['is_login'] == 'true':
        return render_template("student.html")
    else:
        return render_template("login.html")


@StudentController.route('/modify_student', methods=['POST', 'GET'])
def modify_student():
    data = request.get_json(force=True)
    student = db_session.query(Student).get(data['id'])
    profession = db_session.query(Profession).get(data['profession_id'])

    if not student:
        return jsonify(message='Student not found'), 404

    if not profession:
        return jsonify(message='Profession not found'), 404

    try:
        student.name = data['name']
        student.sex = data['sex']
        student.age = data['age']
        student.origin = data['origin']
        student.profession_id = data['profession_id']

        db_session.commit()
        return jsonify(message='Student updated successfully'), 200
    except Exception as e:
        db_session.rollback()
        return jsonify(message=f'Error updating student: {str(e)}'), 500


@StudentController.route('/modify_some_students', methods=['POST', 'GET'])
def modify_some_students():
    data = request.get_json(force=True)

    for id, new_student in data.items():
        print(id)
        print(new_student)
        profession = db_session.query(Profession).get(new_student['profession_id'])
        if not profession:
            return jsonify(message=f'Error updating students: {new_student, id},Profession not found'), 404

    print(data)
    try:
        for id, new_student in data.items():
            print(new_student)
            student_id = new_student.get('id')
            name = new_student.get('name')
            sex = new_student.get('sex')
            age = new_student.get('age')
            origin = new_student.get('origin')
            profession_id = new_student.get('profession_id')

            if student_id and name and sex and age and origin and profession_id:
                student = db_session.query(Student).get(student_id)

                if student:
                    student.name = name
                    student.sex = sex
                    student.age = age
                    student.origin = origin
                    student.profession_id = profession_id

        db_session.commit()
        return jsonify(message='Students updated successfully'), 200
    except Exception as e:
        db_session.rollback()
        return jsonify(message=f'Error updating students: {str(e)}'), 500


@StudentController.route("/delete_student", methods=["POST", "GET"])
def delete_student():
    data = request.get_json(force=True)

    student_id = data['student_id']

    need_delete_student = db_session.query(Student).get(student_id)
    try:
        db_session.delete(need_delete_student)
        db_session.commit()
        return jsonify(message='Student deleted successfully'), 200
    except:
        return jsonify(message='Student not found'), 404


@StudentController.route("/delete_some_students", methods=["POST", "GET"])
def delete_some_students():
    data = request.get_json(force=True)

    studet_ids = data['student_list']

    try:
        deleted_count = db_session.query(Student).filter(Student.id.in_(studet_ids)).delete(synchronize_session=False)
        db_session.commit()
        return jsonify(message=f'{deleted_count} students deleted successfully'), 200
    except Exception as e:
        db_session.rollback()
        return jsonify(message=f'Error deleting students: {str(e)}'), 500


@StudentController.route("/get_students_by_page", methods=["POST", "GET"])
def get_students_by_page():
    data = request.get_json(force=True)

    page = int(data['page'])
    start_id = 10 * (page - 1)
    end_id = 10 * page

    try:
        students_and_professions = db_session.query(Student, Profession).join(Profession).order_by(Student.id).all()
        students = []
        for i in range(start_id, min(end_id, len(students_and_professions))):
            student, profession = students_and_professions[i]
            students.append({'学生编号': student.id, '姓名': student.name, '性别': student.sex, '年龄': student.age,
                             '出生地': student.origin, '职业编号': profession.id, '职业': profession.profession})
        length = len(db_session.query(Student).all())
        db_session.commit()
        db_session.close()
        return jsonify({'students': students, "length": length, "error_message": "success"})
    except Exception as e:
        db_session.rollback()
        return jsonify({"error_message": "error"})


@StudentController.route("/get_all_students", methods=["POST", "GET"])
def get_all_students():
    students_and_professions = db_session.query(Student, Profession).join(Profession).order_by(Student.id).all()
    student_list = [
        {'学生编号': student.id, '姓名': student.name, '性别': student.sex, '年龄': student.age,
         '出生地': student.origin,
         '职业编号': profession.id, '职业': profession.profession} for student, profession in
        students_and_professions]
    return jsonify({'student_list': student_list})
