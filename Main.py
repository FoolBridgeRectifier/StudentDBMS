import mysql.connector
from flask import Flask, render_template, request, redirect, url_for
import requests


app = Flask(__name__)


cnx = mysql.connector.connect(user='root', password='1990',                      # change for required database
                              host='127.0.0.1', database = 'project1',
                              auth_plugin='mysql_native_password')

cursor = cnx.cursor()
# Main admin page
@app.route("/")
def main():
    return render_template("Admin.html")


@app.route("/", methods = ['POST'])
def main_form():
    if request.form['get_button'] == "Department":
        return redirect(url_for('department'))
    if request.form['get_button'] == "Staff":
        return redirect(url_for('teacher'))
    if request.form['get_button'] == "Rooms":
        return redirect(url_for('rooms'))
    if request.form['get_button'] == "Student":
        return redirect(url_for('student'))
    return render_template("Admin.html")

# Student course registeration
@app.route("/studentCourse")
def studentCourse():
    return render_template("studentCourse.html")

@app.route("/studentCourse", methods = ['POST'])
def studentCourse_form():
    courses = []
    errors = []
    available = []
    if request.form['get_button'] == "Show registered Courses":
        # print("KK")
        studID = request.form['studID']
        # print(1)
        if studID:
            sql = "select course_name, sec_no from registeration as r, course as c where c.course_no = r.course_no and s_id = " + studID
            cursor.execute(sql)
            courses = cursor.fetchall()
        else:
            errors.append("Fill required information!")

    if request.form['get_button'] == "Show Available Courses":
        # print("KK")
        sql = "select course_name, staff_name, c.course_no, sec_no from section as s, staff as st, course as c where c.course_no = s.course_no and st.staff_ssn = s.staff_ssn"
        cursor.execute(sql)
        available = cursor.fetchall()
        courses = []

    if request.form['get_button'] == "Register":
        # print(2)
        studID = request.form['studID']
        courseID = request.form['courseID']
        sectionID = request.form['secID']

        if studID and courseID and sectionID:

            sql = "select * from registeration where course_no = %s and s_id = %s"
            val = (courseID, studID)
            cursor.execute(sql, val)
            temp = cursor.fetchall()

            sql = "select max_enroll, current_enrolled from section where course_no = %s and sec_no = %s"
            val = (courseID, sectionID)
            cursor.execute(sql, val)
            temp2 = cursor.fetchall()

            sql = "select course_name, sec_no from registeration as r, course as c where c.course_no = r.course_no and s_id = " + studID
            cursor.execute(sql)
            temp3 = cursor.fetchall()

            if not temp:
                if int(temp2[0][0]) > int(temp2[0][1]) and len(temp3) < 5:
                    sql = "INSERT INTO registeration VALUES (%s, %s, %s)"
                    val = (studID, sectionID, courseID)
                    # print(val)
                    cursor.execute(sql, val)

                    sql = "update section set current_enrolled = %s where course_no = %s and sec_no = %s"
                    val = (str(int(temp2[0][1]) + 1), courseID, sectionID )
                    # print(val)
                    cursor.execute(sql, val)

                    cnx.commit()
                else:
                    errors.append("Not Enough Space in section")
            else:
                errors.append("Already registered for course")
        else:
            errors.append("Fill required information!")
    # else:
        # print("LL")
    return render_template("studentCourse.html", courses=courses, errors=errors, available=available)


# Teacher registeration
@app.route("/teacher")
def teacher():
    return render_template("teacher.html")

@app.route("/teacher", methods = ['POST'])
def teacher_form():
    table = []
    if request.form['get_button'] == "Show Staff Details":
        sql = "select * from staff"
        cursor.execute(sql)
        table = cursor.fetchall()
    else:
        salary = request.form['salary']
        name = request.form['name']
        type = request.form['type']
        load = request.form['load']
        rank = request.form['rank']
        hour = request.form['hour']
        ssn = request.form['ssn']
        if(type == "staff"):
            rank = "0"
            load = "0"
        if salary and name and type and ssn and hour and rank and load:
            sql = "INSERT INTO Staff VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (ssn, name, type, salary, rank, load, hour)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        elif salary and name and type == "staff" and ssn and hour:
            sql = "INSERT INTO Staff VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (ssn, name, type, salary, rank, load, hour)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        # else:
            # print("LL")
    return render_template("teacher.html", courses=table)

# Teacher Course registration
@app.route("/teachercourse")
def teachercourse():
    return render_template("teacherCourse.html")

@app.route("/teachercourse", methods = ['POST'])
def teachercourse_form():
    courses = []
    errors = []
    if request.form['get_button'] == "Show Created Courses":
        ssn = request.form['ssn']
        if ssn:
            sql = "select course_name, sec_no from course, section where section.course_no = course.course_no and staff_ssn = " + ssn
            cursor.execute(sql)
            courses = cursor.fetchall()

    if request.form['get_button'] == "Show Students Enrolled":
        ssn = request.form['ssn']
        courseID = request.form['courseID']
        sec = request.form['sec']
        if courseID and sec and ssn:
            sql = "select s.s_id, s_name from registeration as r, student as s where r.s_id = s.s_id and r.course_no = " + courseID + " and r.sec_no = " + sec
            cursor.execute(sql)
            courses = cursor.fetchall()
    if request.form['get_button'] == "Register":
        ssn = request.form['ssn']
        courseID = request.form['courseID']
        name = request.form['name']
        credit = request.form['credit']
        dept = request.form['dept']
        tareq = request.form['tareq']
        year = request.form['year']
        maxenroll = request.form['maxenroll']
        sec = request.form['sec']
        room = request.form['room']
        building = request.form['building']
        time = request.form['time']
        weekday = request.form['weekday']


        if ssn and courseID and name and credit and dept and tareq and year and maxenroll and sec and room and building and time and weekday:
            sql = "select course_no from course where course_no = " + courseID
            cursor.execute(sql)
            temp = cursor.fetchall()

            if not temp:
                sql = "INSERT INTO course VALUES (%s, %s, %s, %s, %s, %s)"
                val = (courseID, name, year, credit, tareq, dept)
                # print(val)
                cursor.execute(sql, val)

            sql = "INSERT INTO section VALUES (%s, %s, %s, %s, %s, %s)"
            val = (sec, courseID, year, ssn, "0", maxenroll)
            # print(val)
            cursor.execute(sql, val)

            sql = "INSERT INTO sectioninroom VALUES (%s, %s, %s, %s, %s, %s)"
            val = (building, room, courseID, sec, weekday, time)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        # else:
            # print("LL")
    return render_template("teachercourse.html", courses=courses)

# For inputting student
@app.route("/student")
def student():
    return render_template("student.html")

@app.route("/student", methods = ['POST'])
def student_form():
    table = []
    if request.form['get_button'] == "Show Students":
        sql = "select * from student"
        cursor.execute(sql)
        table = cursor.fetchall()
    else:
        studID = request.form['studID']
        name = request.form['name']
        address = request.form['address']
        ssn = request.form['ssn']
        dept = request.form['dept']
        year = request.form['year']
        school = request.form['school']

        if studID and name and address and ssn and dept and year and school:
            sql = "INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (studID, ssn, name, address, school, year, dept)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        # else:
            # print("LL")
    return render_template("student.html", courses=table)

# Building registration
@app.route("/rooms")
def rooms():
    return render_template("rooms.html")

@app.route("/rooms", methods = ['POST'])
def rooms_form():
    table = []
    if request.form['get_button'] == "Show Rooms":
        sql = "select * from building"
        cursor.execute(sql)
        table = cursor.fetchall()
    else:
        id = request.form['id']
        name = request.form['name']
        location = request.form['location']

        if id and name and location:
            sql = "INSERT INTO building VALUES (%s, %s, %s)"
            val = (id, name, location)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        # else:
            # print("LL")
    return render_template("rooms.html", courses=table)


# Department registration
@app.route("/department")
def department():
    return render_template("department.html")

@app.route("/department", methods = ['POST'])
def department_form():
    table = []
    if request.form['get_button'] == "Show Departments":
        sql = "select * from department"
        cursor.execute(sql)
        table = cursor.fetchall()
    else:
        code = request.form['code']
        office = request.form['office']
        name = request.form['name']
        budget = request.form['budget']
        chair = request.form['chair']

        if code and name and office and budget and chair:
            sql = "INSERT INTO department VALUES (%s, %s, %s, %s, %s)"
            val = (code, name, budget, chair, office)
            # print(val)
            cursor.execute(sql, val)
            cnx.commit()
        # else:
            # print("LL")
    return render_template("department.html", courses=table)


if __name__ == "__main__":
    app.run(debug=True)