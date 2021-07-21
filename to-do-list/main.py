import datetime

from flask import Blueprint
from flask import render_template, request, redirect, url_for, jsonify
from flask import g

from . import db

bp = Blueprint("main", "main", url_prefix="")

def format_date(d):
    if d:
        v = d.strftime('%Y-%m-%d %H:%M:%S')
        return v
    else:
        return None

@bp.route("/")
def mainpage():
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.status from content p order by p.{oby}")
    else:
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.status from content p order by p.{oby} desc")
    dat = cursor.fetchall()
    return render_template('index.html', pets = dat, order="desc" if order=="asc" else "asc")


@bp.route("/<pid>")
def task_info(pid): 
    conn = db.get_db()
    cursor = conn.cursor()
    cursor.execute("select p.task, p.created_on, p.due,p.description from content p where p.id=?", [pid])
    pet = cursor.fetchone()
    #cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
    
    task, created_on, due, description= pet
    data = dict(id = pid,
                task=task,
                created_on=created_on,
                due=due,
                description=description
                )
    return render_template("taskdetail.html", **data)

@bp.route("/addtask", methods=["GET", "POST"])
def addtask():
    conn = db.get_db()
    cursor = conn.cursor()

    if request.method== "GET":
        data=dict(
            id=" ",
            task=" ",
            created_on=" ",
            due=" ",
            status=" "
        )
        return render_template("addtask.html",**data)
    elif request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        due = request.form.get("due")
        status=request.form.get("status")
        cursor.execute("insert into content(task,created_on,due,status,description) values(?,?,?,?,?) ", (task,datetime.datetime.today().strftime("%Y-%m-%d %H:%M"), due,status,description))
        #conn.commit()

        #if sold=="sold":
        #cursor.execute("insert into content(created_on) values(?) ", (datetime.datetime.today().strftime("%Y-%m-%d")))
        conn.commit()
        # TODO Handle sold
        return redirect(url_for("main.mainpage"), 302)
        



