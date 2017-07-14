from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
from . import app
from .database import session, Tip, User
# from .forms import EntryForm, EntryDeleteForm, LoginForm

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

    # if current_user.is_anonymous() == True:
    #     return redirect(url_for("login"))
    # Zero-indexed page
    page_index = page - 1

    # count = session.query(Tip).filter(Tip.author==current_user).count()
    count = session.query(Tip).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) // paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    tips = session.query(Tip)
    tips = tips.filter(Tip.author==current_user)
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
@login_required
def add_tip_get():
    return render_template("add_tip.html")

@app.route("/tip/add", methods=["POST"])
@login_required
def add_tip_post():
    tip = Tip(
        title=request.form["title"],
        body=request.form["body"],
        author=current_user
        # location=request.form["location"]
    )
    session.add(tip)
    session.commit()
    return redirect(url_for("tips"))

@app.route("/tip/<int:id>", methods=["GET"])
def view_tip_get(id):
    tip = session.query(Tip).get(id)
    return render_template("tip.html", id = id, tip = tip)

@app.route("/api/tips/<int:id>/edit", methods=["GET"])
@login_required
def edit_tip_get(id):
    tip = session.query(Tip).get(id)
    if current_user == tip.author:
        return render_template("edit_tip.html", id = id, tip = tip)
    else:
        return redirect(url_for("tips"))

@app.route("/api/tips/<int:id>/edit", methods=["POST"])
@login_required
def edit_tip_post(id):
    tip = session.query(Tip).get(id)
    tip.title = request.form["title"]
    tip.body = request.form["body"]
    session.commit()
    return redirect(url_for("tips"))
    # return render_template("edit_tip.html", id = id, tip = tip)
    # tip = Tip.query.filter_by(id = id).first_or_404()
    #
    # if not all([tip.author, current_user]) or tip.author.id != current_user.id:
    #     raise Forbidden('Only tip author can edit it.')
    #
    # form = EntryForm(obj=entry)
    #
    # if form.validate_on_submit():
    #     form.populate_obj(tip)
    #     db.session.add(tip)
    #     db.session.commit()
    #     return redirect(url_for('tips'))
    #
    # else:
    #     return render_template('add_tip.html', form=form)

# @app.route("/login", methods=["GET"])
# def login_get():
#     return render_template("login.html")

@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    # Test whether user already exists
    user = session.query(User).filter_by(email=email).first()
    # If user does not exist or password does not match hashed password, then redirect with error message
    if not user or not check_password_hash(user.password, password):
        # Flask 'flash' function stores message to display in page
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    # If username and password are correct,
    # Use Flask-Login login_user function to use cookie to identify user in browser
    login_user(user)
    # Either access resource selected at login or go to main /posts page
    return redirect(url_for("tips"))

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('tips'))

app.secret_key = "l\xcd\xaf\x93\xd5sy\xb4WHu\xdd\x8fW\xe4J LY\x14\x98\x13ft"

    # email = request.form["email"]
    # password = request.form["password"]
    # user = session.query(User).filter_by(email=email).first()
    # if not user or not check_password_hash(user.password, password):
    #     flash("Incorrect username or password", "danger")
    #     return redirect(url_for("login_get"))
    #
    # login_user(user)
    # return redirect(request.args.get('next') or url_for("tips"))

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
