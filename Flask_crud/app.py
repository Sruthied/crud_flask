from flask import Flask, render_template, request, flash, url_for, redirect
import pymongo
from mongoengine import Document, connect, StringField, IntField, DateTimeField, FloatField, EmailField, BooleanField, Q

#db connection
client = connect("Flask_mongodb")

app = Flask(__name__)
app.secret_key="zzz"

#db model
class Employee(Document):
    name=StringField()
    empId=IntField()
    doj=DateTimeField()
    designation=StringField()
    salary=FloatField()
    address=StringField()
    phoneNO=IntField()
    email=EmailField(unique=True)
    password=StringField()




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/emp_form')
def emp_form():
    return render_template("add_employee.html")

@app.route('/add_employee',methods=["POST","GET"])
def add_employee():
    if request.method == "POST":
        ename=request.form.get("name")
        eid=request.form.get("id")
        doj=request.form.get("doj")
        des=request.form.get("designation")
        sal=request.form.get("salary")
        add=request.form.get("add")
        pno=request.form.get("pno")
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        print(eid)

        try:
            email_exist = Employee.objects.filter(email = email)
            print(eid)

            if email_exist:
                flash("Email already existed!")
                return render_template("add_employee.html")

            emp=Employee(
                name=ename,
                empId = eid,
                doj = doj,
                designation = des,
                salary = sal,
                address = add,
                phoneNO = pno,
                email = email,
                password = pwd
            )
            emp.save()
            flash("Employee added succesfully")
            return render_template("add_employee.html")


        except Exception as e :
            print(e)
            flash("Something Went Wrong")
            return render_template("add_employee.html")



    return render_template("add_employee.html")

@app.route('/get_all_employees',methods=["POST","GET"])
def get_all_employees():
    emp = Employee.objects.all()
    return render_template("view_emplyees.html",emp=emp)

@app.route('/view_emp/<int:empId>',methods=["POST","GET"])
def view_emp(empId):
    emp=Employee.objects.get(empId=empId)
    return render_template("update.html",emp=emp)

@app.route('/update_emp',methods=["POST","GET"])
def update_emp():

    if request.method == "POST":
        ename=request.form.get("name")
        eid=request.form.get("id")
        doj=request.form.get("doj")
        des=request.form.get("designation")
        sal=request.form.get("salary")
        add=request.form.get("add")
        pno=request.form.get("pno")
        email=request.form.get("email")
        pwd=request.form.get("pwd")
        # print(eid)
        try:

            print(eid)
            email_exist = Employee.objects.filter(email=email)

            #exclude(empId=eid)

            if email_exist:
                flash("Email already existed!")
                return redirect(url_for("view_emp",empId=eid))
            else:
                emp=Employee.objects.filter(empId=eid)
                emp.update(
                    name=ename,
                    empId=eid,
                    doj=doj,
                    designation=des,
                    salary=sal,
                    address=add,
                    phoneNO=pno,
                    email=email,
                    password=pwd
                )
                flash("Employee updated")
                return redirect(url_for("view_emp",empId=eid))
        except Exception as e:
            print(e)
            flash("somthing went wrong!")
            return redirect(url_for("view_emp",empId=eid))



@app.route('/delete_emp/<int:empId>',methods=["POST","GET"])
def delete(empId):
    # print(empId)
    eid=empId
    # idno = flask.request.args.get("empId")
    # print(idno)
    Employee.objects.get(empId=eid).delete()

    flash("Employee Deleted Successfully")
    return redirect(url_for("get_all_employees"))


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
