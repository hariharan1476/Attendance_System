from flask import Flask,render_template,request,redirect,session
import json
from datetime import date

app = Flask(__name__)
app.secret_key="secret"


# -------- helper functions --------

def load_users():
    with open("users.json") as f:
        return json.load(f)

def load_students():
    with open("students.json") as f:
        return json.load(f)

def load_attendance():
    with open("attendance.json") as f:
        return json.load(f)

def save_attendance(data):
    with open("attendance.json","w") as f:
        json.dump(data,f,indent=4)

# -------- routes --------

@app.route("/",methods=["GET","POST"])
def login():

    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        users=load_users()

        for u in users:
            if u["username"]==username and u["password"]==password:
                session["user"]=username
                return redirect("/dashboard")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/attendance",methods=["GET","POST"])
def attendance():

    students=load_students()

    if request.method=="POST":
        records=load_attendance()
        today=str(date.today())

        for s in students:
            sid=str(s["id"])
            status=request.form.get(sid)

            records.append({
                "student_id":sid,
                "status":status,
                "date":today
            })

        save_attendance(records)

    return render_template("attendance.html",students=students)


if __name__ == "__main__":
    app.run()

