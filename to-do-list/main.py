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
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.task from content p order by p.{oby}")
    else:
        cursor.execute(f"select p.id, p.task, p.created_on, p.due, p.task from content p order by p.{oby} desc")
    dat = cursor.fetchall()
    return render_template('index.html', pets = dat, order="desc" if order=="asc" else "asc")





