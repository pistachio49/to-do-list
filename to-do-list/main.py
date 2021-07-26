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
    i=1
    conn = db.get_db()
    cursor = conn.cursor()
    oby = request.args.get("order_by", "id") # TODO. This is currently not used. 
    order = request.args.get("order", "asc")
    if order == "asc":
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.status from content p order by p.{oby}")
    else:
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.status from content p order by p.{oby} desc")

    dat = cursor.fetchall()
    ldat=list(dat)
    topass=[]
    #print(ldat)
    for item in ldat:
        litem=list(item)
        litem.append(i)
        topass.append(litem)
        i+=1
        #print(item)
    
    p=[]
    for item in topass:
        it=tuple(item)
        p.append(it)

    dat=tuple(p)
    #print(dat)
    return render_template('index.html', pets = dat, order="desc" if order=="asc" else "asc")


@bp.route("/<pid>/changetask")
def changetask(pid):
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute("select p.status from content p where p.id=?", (pid))
    d=cursor.fetchone()

    status=d
    if status[0]=="To-do":
        cursor.execute("update content set status=? where id=?",("In progress",pid))
        print("yes")
    elif status[0]=='In progress':
        cursor.execute("update content set status=? where id=?",("Completed",pid))
        print("yes22")
    else:
        cursor.execute("update content set status=? where id=?",("To-do",pid))
        print(status)
    
    conn.commit()

    return redirect(url_for("main.mainpage", pid=pid), 302)


@bp.route("/<pid>", methods=["GET", "POST"])
def task_info(pid): 
    conn = db.get_db()
    cursor = conn.cursor()

    if request.method== "GET":
        cursor.execute("select p.task, p.created_on, p.due,p.description,p.status from content p where p.id=?", [pid])
        pet = cursor.fetchone()
        #cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        
        task, created_on, due, description, status= pet
        data = dict(id = pid,
                    task=task,
                    created_on=created_on,
                    due=due,
                    description=description,
                    status=status
                    )
        return render_template("taskdetail.html", **data)
    elif request.method== "POST":
        cursor.execute("delete from content where id=?", (pid))
        #conn.commit()

        #if sold=="sold":
       # cursor.execute("update pet set sold = ? where id = ?", (datetime.datetime.today().strftime("%Y-%m-%d"), pid))
        conn.commit()
        # TODO Handle sold
        return redirect(url_for("main.mainpage", pid=pid), 302)

@bp.route("/<pid>/delete")
def delete(pid):
    conn = db.get_db()
    cursor = conn.cursor()

    cursor.execute("delete from content where id=?", (pid))
    conn.commit()

    return redirect(url_for("main.mainpage", pid=pid), 302)

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
        #print(type(due))
        due=due.replace("T"," ")
        status=request.form.get("status")

        if not task or not due or not status:
            return redirect(url_for("main.mainpage"), 302)

        cursor.execute("insert into content(task,created_on,due,status,description) values(?,?,?,?,?) ", (task,datetime.datetime.today().strftime("%Y-%m-%d %H:%M"), due,status,description))
        #conn.commit()

        #if sold=="sold":
        #cursor.execute("insert into content(created_on) values(?) ", (datetime.datetime.today().strftime("%Y-%m-%d")))
        conn.commit()
        # TODO Handle sold
        return redirect(url_for("main.mainpage"), 302)
        
@bp.route("/<pid>/edit", methods=["GET", "POST"])
def edit(pid):
    conn = db.get_db()
    cursor = conn.cursor()
    if request.method == "GET":
        cursor.execute("select p.task, p.created_on, p.due,p.description from content p where p.id = ?", [pid])
        pet = cursor.fetchone()
        #cursor.execute("select t.name from tags_pets tp, tag t where tp.pet = ? and tp.tag = t.id", [pid])
        #tags = (x[0] for x in cursor.fetchall())
        task, created_on, due, description= pet
        data = dict(id = pid,
                    task=task,
                    created_on=created_on,
                    due=due,
                    description=description
                    )
        return render_template("edittask.html", **data)
    elif request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        due = request.form.get("due")
        due=due.replace("T"," ")
        status=request.form.get("status")


        if not task or not due or not status:
            return redirect(url_for("main.mainpage"), 302)

        cursor.execute("update content set task=?,description = ?,due=?,status=? where id = ?", (task,description,due,status,pid))
        #conn.commit()

        #if sold=="sold":
       # cursor.execute("update pet set sold = ? where id = ?", (datetime.datetime.today().strftime("%Y-%m-%d"), pid))
        conn.commit()
        # TODO Handle sold
        return redirect(url_for("main.mainpage", pid=pid), 302)


