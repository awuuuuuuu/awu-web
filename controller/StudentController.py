from flask import Blueprint, render_template, session, request, jsonify
from sqlalchemy import func

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


@StudentController.route('/add_student', methods=['POST', 'GET'])
def add_student():
    data = request.get_json(force=True)
    name = data.get('name')
    sex = data.get('sex')
    age = data.get('age')
    origin = data.get('origin')
    profession_name = data.get('profession')

    try:
        profession = db_session.query(Profession).filter_by(profession=profession_name).first()
        if not profession:
            profession = Profession(profession=profession_name)
            db_session.add(profession)
            db_session.commit()

        new_student = Student(name=name, sex=sex, age=age, origin=origin, profession_id=profession.id)
        db_session.add(new_student)
        db_session.commit()
        return jsonify(message='Student added successfully'), 201
    except Exception as e:
        db_session.rollback()
        return jsonify(message=f'Error updating student: {str(e)}'), 500


@StudentController.route('/modify_student', methods=['POST', 'GET'])
def modify_student():
    data = request.get_json(force=True)
    student = db_session.query(Student).get(data['id'])
    profession_name = data['profession']

    if not student:
        return jsonify(message='Student not found'), 404

    profession = db_session.query(Profession).filter_by(profession=profession_name).first()
    if not profession:
        profession = Profession(profession=profession_name)
        db_session.add(profession)
        db_session.commit()

    try:
        student.name = data['name']
        student.sex = data['sex']
        student.age = data['age']
        student.origin = data['origin']
        student.profession_id = profession.id

        db_session.commit()
        return jsonify(message='Student updated successfully'), 200
    except Exception as e:
        db_session.rollback()
        return jsonify(message=f'Error updating student: {str(e)}'), 500


@StudentController.route('/modify_some_students', methods=['POST', 'GET'])
def modify_some_students():
    data = request.get_json(force=True)

    for id, new_student in data.items():
        profession_name = new_student['profession']
        profession = db_session.query(Profession).filter_by(profession=profession_name).first()
        if not profession:
            profession = Profession(profession=profession_name)
            db_session.add(profession)
            db_session.commit()
        new_student['profession_id'] = profession.id

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
    is_search = data['is_search']
    file_name = data['type']
    file_value = data['key']

    start_id = 10 * (page - 1)
    end_id = 10 * page

    students_and_professions = None
    if is_search and file_name == "profession":
        students_and_professions = db_session.query(Student, Profession).join(Profession). \
            filter(getattr(Profession, file_name).ilike(f"%{file_value}%")) \
            .order_by(Student.id.desc()).all()
    elif is_search:
        students_and_professions = db_session.query(Student, Profession).join(Profession). \
            filter(getattr(Student, file_name).ilike(f"%{file_value}%")) \
            .order_by(Student.id.desc()).all()
    else:
        students_and_professions = db_session.query(Student, Profession).join(Profession).order_by(
            Student.id.desc()).all()

    try:
        students = []
        for i in range(start_id, min(end_id, len(students_and_professions))):
            student, profession = students_and_professions[i]
            students.append({'学生编号': student.id, '姓名': student.name, '性别': student.sex, '年龄': student.age,
                             '出生地': student.origin, '职业编号': profession.id, '职业': profession.profession})
        length = len(students_and_professions)
        db_session.commit()
        db_session.close()
        return jsonify({'students': students, "length": length, "error_message": "success"})
    except Exception:
        db_session.rollback()
        return jsonify({"error_message": "error"})


@StudentController.route("/get_all_students", methods=["POST", "GET"])
def get_all_students():
    students_and_professions = db_session.query(Student, Profession).join(Profession).order_by(Student.id.desc()).all()
    student_list = [
        {'学生编号': student.id, '姓名': student.name, '性别': student.sex, '年龄': student.age,
         '出生地': student.origin,
         '职业编号': profession.id, '职业': profession.profession} for student, profession in
        students_and_professions]
    return jsonify({'student_list': student_list})
