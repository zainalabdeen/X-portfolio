import os
from . import create_app
from .models import Users,Skills,Titles,Interests,Educations,Experiences,Contacts
from .helpers import Helper
from flask import Flask,flash,redirect,jsonify,request,abort,render_template,session
from . import db
from flask_session import Session
from werkzeug.security import check_password_hash


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

app.jinja_env.filters["get_age"] = Helper.get_age_by_birthdate

# Configure session to use filesystem (instead of signed cookies)
Session(app)

MODEL_LIST = ['skills','titles','interests','educations','experiences']

@app.route("/start", methods=["GET", "POST"])
def start():
    return render_template("index.html")


@app.route("/")
def index():
    """Show portfolio"""
    if session.get("user_id",False):
        user_row = Users.query.get(session["user_id"])
        if not user_row:
            flash("Session Expired","error")
            return redirect("/logout")
        titles = []
        for title in user_row.titles:
            titles.append(title.name) 
        return render_template("resume/index.html",user=user_row,titles=' , '.join(titles))
    return redirect("/start")

@app.route("/view",methods=["GET"])
def view_portfolio():
    """Show portfolio by email"""
    email =  request.args.get('email',False)
    if not email:
        flash("Can't View Portfolio","error")
        return redirect("/")
    user_row = Users.query.filter_by(email=email).first()
    if not user_row:
        flash("Portfolio Not Exist","error")
        return redirect("/")
    titles = []
    for title in user_row.titles:
        titles.append(title.name) 
    return render_template("resume/index.html",user=user_row,titles=' , '.join(titles))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    model = Users
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Forget any user_id
        session.clear()

        form_errors = dict()
        # Ensure username was submitted
        if not request.form.get("email"):
            form_errors["Email"] = "You must provide email"

        # Ensure password was submitted
        elif not request.form.get("password"):
            form_errors["Password"] = "You must provide password"

        # Query database for username
        user = model.query.filter_by(email=request.form.get("email")).first()
        

        # Ensure username exists and password is correct
        if not user or not user.check_user_password(request.form.get("password")):
            form_errors["Wrong Info"] = "invalid email and/or password"
        
        if form_errors:
            return render_template("login.html",form_errors=form_errors)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        if session.get("user_id",False):
            return redirect("/")
        return render_template("login.html")


@app.route("/logout")
@Helper.login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    model = Users
    if request.method == "POST":
        form_errors = dict()
        
        if not request.form.get("sex"):
            form_errors['Sex'] = "You must provide your sex"
        if not request.form.get("phone"):
            form_errors['Phone'] = "You must provide your phone"
        if not request.form.get("address"):
            form_errors['Address'] = "You must provide your address"
        if not request.form.get("birthday"):
            form_errors['Birthday'] = "You must provide your birthday"
        if not request.form.get("degree"):
            form_errors['Degree'] = "You must provide your degree"
        if not request.form.get("email"):
            form_errors['Email'] = "You must provide your email"
        if not request.form.get("fullname"):
            form_errors['Fullname'] = "You must provide your fullname"
        if not request.form.get("description"):
            form_errors['About You'] = "You must provide Summary About You"
        if not request.form.get("password") or not request.form.get("confirm_password"):
            form_errors['Password'] = "You must provide password"

        if not form_errors and request.form.get("password") != request.form.get("confirm_password"):
            form_errors['Password'] = "Password and confirmed password must be same"
        if request.form.get("birthday"):
            try:
                Helper.from_string(request.form.get("birthday"))
            except:
                form_errors['Birthday'] = "Wrong Birthday"
        if form_errors:
            return render_template("register.html",form_errors=form_errors)
        # Query database for username
        users = model.query.filter_by(email=request.form.get("email")).all()
        if users:
            form_errors['email'] = "this email already exist"
            return render_template("register.html",form_errors=form_errors)
        try:
            rec = model.json_create(model,request.form)
            db.session.add(rec)
            db.session.commit()
        except Exception as EX:
            form_errors['timeout'] = "Unable to process your request now please try later"
            return render_template("register.html",form_errors=form_errors)
        # Remember which user has logged in
        session["user_id"] = rec.id

        # Redirect user to home page
        return redirect("/")
    else:
        if session.get("user_id",False):
            return redirect("/")
        return render_template("register.html")


@app.route("/basic_info", methods=["GET", "POST"])
@Helper.login_required
def basic_info():
    """Register user"""
    model = Users
    if request.method == "POST":
        form_errors = dict()
        
        if not request.form.get("sex"):
            form_errors['Sex'] = "You must provide your sex"
        if not request.form.get("phone"):
            form_errors['Phone'] = "You must provide your phone"
        if not request.form.get("address"):
            form_errors['Address'] = "You must provide your address"
        if not request.form.get("birthday"):
            form_errors['Birthday'] = "You must provide your birthday"
        if not request.form.get("degree"):
            form_errors['Degree'] = "You must provide your degree"
        if not request.form.get("fullname"):
            form_errors['fullname'] = "You must provide your fullname"
        if request.form.get("birthday"):
            try:
                Helper.from_string(request.form.get("birthday"))
            except:
                form_errors['Birthday'] = "Wrong Birthday"
        if form_errors:
            return render_template("profile/basic_info.html",form_errors=form_errors)
        # Query database for username
        user = model.query.get(session.get("user_id"))
        if not user:
            flash("Session Expired","error")
            return redirect("/")
        try:
            rec = user.json_edit(request.form)
            db.session.commit()
        except Exception as EX:
            form_errors['timeout'] = "Unable to process your request now please try later"
            return render_template("profile/basic_info.html",form_errors=form_errors,info=user)
        flash("Successfully Edited.","success")
        return render_template("profile/basic_info.html",info=user)
    else:
        user = model.query.get(session.get("user_id"))
        return render_template("profile/basic_info.html",info=user)


@app.route("/change_password", methods=["GET", "POST"])
@Helper.login_required
def change_password():
    """Change user Password"""
    model = Users
    if request.method == "POST":
        form_errors = dict()
        if not request.form.get("current_password"):
            form_errors["Current Password"] = "You must provide Current Password"

        # Ensure password was submitted
        elif not request.form.get("password") or not request.form.get("confirmation"):
            form_errors["New Password"] = "You must provide New password"

        elif request.form.get("password") != request.form.get("confirmation"):
            form_errors["New Password"] = "New password and confirmed password must be same"
        
        if form_errors:
            return render_template("profile/change_password.html",form_errors=form_errors)

        user = model.query.get(session.get("user_id"))

        # Ensure username exists and password is correct
        if not user or not user.check_user_password(request.form.get("current_password")):
            form_errors["Wrong Info"] = "invalid password"
        
        if form_errors:
            return render_template("profile/change_password.html",form_errors=form_errors)
        try:
            user.change_user_password(request.form)
            db.session.commit()
        except Exception as EX:
            form_errors['timeout'] = "Unable to process your request now please try later"
            return render_template("profile/change_password.html",form_errors=form_errors)
        session.clear()
        flash("Password Successfully Changed.","success")
        return redirect("/login")
    else:
        return render_template("profile/change_password.html")
    
#Model Api
#TODO: Make decorated function to check the model in list and return class of the str model
@app.route("/get/profile/<model>", methods=["GET"])
@Helper.login_required
def profile(model):
    """Show portfolio profile"""
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    records = model.query.filter_by(user_id=session.get("user_id")).all()
    #records = [rec.to_json() for rec in recs]
    model_name = model.__tablename__
    return render_template("profile/{}.html".format(model_name),records=records)

@app.route("/social_profile",methods=["GET","POST"])
@Helper.login_required
def social_profile():
    """Show contacts"""
    user = Users.query.get(session["user_id"])
    if request.method == "POST": 
        #try:
        user.json_edit(request.form)
        db.session.commit()
        #except Exception as EX:
        #    flash("Unable to process your request now please try later","error")
        #    return render_template("profile/contacts.html",user=user)
        flash("Successfully Edited.","success")
    return render_template("profile/contacts.html",user=user)


#Retrieve
@app.route("/get/list/<model>", methods=["GET"])
@Helper.login_required
def get_list(model):
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    
    recs = model.query.filter_by(user_id=session.get("user_id")).all()
    return jsonify([rec.to_json() for rec in recs])

@app.route("/get/<model>/<int:id>", methods=["GET"])
@Helper.login_required
def get_by_id(model,id):
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    rec = model.query.get(id)
    if rec is None:
        abort(404)
    return jsonify(rec.to_json())

#Operation
#Create Need Login
@app.route('/create/<model>', methods=['POST'])
@Helper.login_required
def create(model):
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    if not request.form:
        abort(400)
    model_name = model.__tablename__
    try:
        rec = model.json_create(model,request.form)
        db.session.add(rec)
        db.session.commit()
    except Exception as Ex:
        flash(Ex,"error")
        return redirect("/get/profile/{}".format(model_name))
    flash("Successfully Created.","success")
    return redirect("/get/profile/{}".format(model_name))
#Create Without Login
@app.route('/add/<model>', methods=['POST'])
def add(model):
    if model not in ['contacts']:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    if not request.form:
        abort(400)
    model_name = model.__tablename__
    try:
        rec = model.json_create(model,request.form)
        db.session.add(rec)
        db.session.commit()
    except Exception as Ex:
        flash(Ex,"error")
        return redirect("/view?email={}".format(request.form.get("user_email")))
    flash("Message Successfully Send.","success")
    return redirect("/view?email={}".format(request.form.get("user_email")))

@app.route('/edit/<model>/<int:id>', methods=['POST'])
@Helper.login_required
def edit(model,id):
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    if not request.form:
        abort(400)
    model_name = model.__tablename__
    rec = model.query.get(id)
    if rec is None:
        flash("Record Not Exist","error")
        return redirect("/get/profile/{}".format(model_name))
    try:
        rec.json_edit(request.form)
        db.session.commit()
    except Exception as Ex:
        flash(Ex,"error")
        return redirect("/get/profile/{}".format(model_name))
    flash("Successfully Edited.","success")
    return redirect("/get/profile/{}".format(model_name))

@app.route("/delete/<model>/<int:id>", methods=["GET"])
@Helper.login_required
def delete(model,id):
    if model not in MODEL_LIST:
        abort(404)
    else:
        try:
            model = eval(model.capitalize())
        except:
            abort(404)
    model_name = model.__tablename__
    rec = model.query.get(id)
    if rec is None:
        flash("Record Not Exist","error")
        return redirect("/get/profile/{}".format(model_name))
    try:
        db.session.delete(rec)
        db.session.commit()
    except Exception as Ex:
        flash(Ex,"error")
        return redirect("/get/profile/{}".format(model_name))
    flash("Successfully Deleted.","success")
    return redirect("/get/profile/{}".format(model_name))

