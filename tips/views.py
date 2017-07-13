from flask import render_template, request, redirect, url_for

from . import app
from .database import session, Tip

# @app.route("/")
# def entries():
#     entries = session.query(Entry)
#     entries = entries.order_by(Entry.datetime.desc())
#     entries = entries.all()
#     return render_template("entries.html",
#         entries=entries
#     )

PAGINATE_BY = 10

@app.route("/")
@app.route("/page/<int:page>")
def tips(page=1):

    if page < 1:
        raise ValueError('Invalid number')
    try:
        paginate_by = int(request.args.get('limit', PAGINATE_BY))
    except ValueError:
        paginate_by = PAGINATE_BY

    # Zero-indexed page
    page_index = page - 1

    count = session.query(Tip).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) // paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    tips = session.query(Tip)
    tips = tips.order_by(Tip.datetime.desc())
    tips = tips[start:end]

    return render_template("tips.html",
        tips=tips,
        has_next=has_next,
        has_prev=has_prev,
        page=page,
        total_pages=total_pages
    )

@app.route("/tip/add", methods=["GET"])
def add_tip_get():
    return render_template("add_tip.html")

@app.route("/tip/add", methods=["POST"])
def add_tip_post():
    tip = Tip(
        title=request.form["title"],
        body=request.form["body"],
    )
    session.add(tip)
    session.commit()
    return redirect(url_for("tips"))

@app.route("/tip/<int:id>", methods=["GET"])
def view_tip_get(id):
    tip = session.query(Tip).get(id)
    return render_template("tip.html", id = id, tip = tip)

@app.route("/api/tips/<int:id>/edit", methods=["GET"])
def edit_tip_get(id):
    tip = session.query(Tip).get(id)
    return render_template("edit_tip.html", id = id, tip = tip)

# @app.route("/tip/<int:id>/delete", methods=["GET"])
# def delete_entry_get(id):
#     entry = session.query(Entry).get(id)
#     return render_template("delete_entry.html", id = id, entry = entry)
#
# @app.route("/entry/<id>/delete", methods=["POST"])
# def delete_entry_post(id):
#     entry = session.query(Entry).get(id)
#     session.delete(entry)
#     session.commit()
#     return redirect(url_for("entries"))
