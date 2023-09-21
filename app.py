from flask import Flask, flash, abort
from flask import request, render_template, jsonify, redirect, session, url_for
from pymongo import MongoClient
from flask_session import Session
from bson.objectid import ObjectId
from functools import wraps
from datetime import datetime, timedelta


# flask object
app = Flask(__name__)
app.secret_key = "your_secret_key"


# Config Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up MongoDB cloud connection.
# It was used in the begginning of lab and was replaced with docker:
# Cloud connection string (won't be needed):
# connection_string = "mongodb+srv://viktorijapopova5:simple_pass@cluster0.da1byij.mongodb.net/?retryWrites=true&w=majority"

connection_string = "mongodb://root:example@mongo/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
# DB with name UnipiLibrary
db = client.UnipiLibrary
if "user" not in db.list_collection_names():
    db.create_collection("user")
    db.create_collection("book")
    db.create_collection("reservation")

    # add default users to collection "user":
    db["user"].insert_many(
        [
            {
                "name": "admin",
                "surname": "admin",
                "birthday": "None",
                "pwd": "123456",
                "email": "admin@mail.com",
                "role": "admin",
            },
            {
                "name": "Maria",
                "surname": "Smith",
                "birthday": "1997-01-09",
                "pwd": "2121",
                "email": "maria@iv.com",
                "role": "user",
            },
            {
                "name": "John",
                "surname": "Black",
                "birthday": "1994-11-02",
                "pwd": "2121",
                "email": "john@mail.com",
                "role": "user",
            },
            {
                "name": "Anna",
                "surname": "White",
                "birthday": "1997-12-12",
                "pwd": "2121",
                "email": "anna@mail.com",
                "role": "user",
            },
            {
                "name": "Jesse",
                "surname": "Pickman",
                "birthday": "1992-01-01",
                "pwd": "2121",
                "email": "jesse@mail.com",
                "role": "user",
            },
            {
                "name": "Sam",
                "surname": "George",
                "birthday": "1999-12-04",
                "pwd": "2121",
                "email": "sam@mail.com",
                "role": "user",
            },
        ]
    )

    # add default books to collection "book":
    db["book"].insert_many(
        [
            {
                "title": '"Introduction to the Theory of Computation"',
                "author": "Michael Sipser",
                "year": "2012",
                "page_number": "800",
                "be_land": "62",
                "description": "This book is a foundational resource for understanding the theory of computation, including topics like automata theory, formal languages, and complexity theory. It's widely used in computer science curricula and provides insights into the mathematical aspects of computing.",
                "isAvailable": "Yes",
            },
            {
                "title": '"Structure and Interpretation of Computer Programs"',
                "author": "Harold Abelson, Gerald Jay Sussman, Julie Sussman",
                "year": "1985",
                "page_number": "800",
                "be_land": "62",
                "description": 'Commonly referred to as "SICP," this book is a classic text in computer science education. It emphasizes programming as a means of expressing computational processes and understanding the foundations of programming languages and software engineering.',
                "isAvailable": "Yes",
            },
            {
                "title": '"Artificial Intelligence: A Modern Approach"',
                "author": "Stuart Russell, Peter Norvig",
                "year": "1995",
                "page_number": "1200",
                "be_land": "93",
                "description": ": Widely used in artificial intelligence courses, this book provides a comprehensive overview of the field. It covers topics such as problem-solving, knowledge representation, machine learning, natural language processing, and robotics, offering both theoretical foundations and practical insights.",
                "isAvailable": "Yes",
            },
            {
                "title": '"Introduction to Naval Architecture"',
                "author": "E.C. Tupper",
                "year": "1995",
                "page_number": "600",
                "be_land": "32",
                "description": "This comprehensive book provides an introduction to the fundamental principles of naval architecture. It covers topics such as ship geometry, hydrostatics, stability, resistance, propulsion, and more. It's widely used as a textbook in maritime engineering programs.",
                "isAvailable": "Yes",
            },
            {
                "title": '"Principles of Management"',
                "author": "Gary Dessler, Richard L. Daft",
                "year": "2000",
                "page_number": "800",
                "be_land": "62",
                "description": "his comprehensive textbook covers fundamental concepts of management, including planning, organizing, leading, and controlling. It provides insights into contemporary management practices and theories, making it a popular choice for management students.",
                "isAvailable": "Yes",
            },
            {
                "title": '"Introduction to the Practice of Statistics"',
                "author": "David S. Moore, George P. McCabe, Bruce A. Craig",
                "year": "1997",
                "page_number": "800",
                "be_land": "62",
                "description": "This book is a widely-used textbook that provides an accessible introduction to statistics. It covers fundamental statistical concepts, data visualization, hypothesis testing, regression analysis, and more. It's designed for students and professionals in various fields.",
                "isAvailable": "Yes",
            },
        ]
    )


# Decorator is to protect unauthorized access to a page
# exept signup.html and login.html
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        # if user is not logged in, redirect to login page
        user = db["user"].find_one({"_id": ObjectId(session["mongodb_id"])})
        if not user:
            flash("Please authorize")
            return redirect("login", code=401)
        return f(*args, **kwargs)

    return wrap


# Pages that have following decorator can be accessible only by admin
def admin_login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        user = db["user"].find_one({"_id": ObjectId(session["mongodb_id"])})
        user_role = user.get("role")
        if user_role != "admin":
            # flash("Unauthorize access. Only admin can access this page.")
            abort(403)
        return f(*args, **kwargs)

    return wrap


# Display login.html
@app.route("/")
def login():
    return render_template("login.html")


# Display signup.html
@app.route("/signup")
def signup():
    return render_template("signup.html")


# Admin profile
@app.route("/admin_profile")
# Unauthorized access:
@login_required
# Admin decorator:
@admin_login_required
def admin_profile():
    book = db["book"].find({})
    return render_template("admin_profile.html", book=book)


# User profile
@app.route("/profile")
# Unauthorized access:
@login_required
def profile():
    find_user = session.get("mongodb_id")
    user = db["user"].find_one({"_id": ObjectId(find_user)})
    reservation = db["reservation"].find({"id_user": str(find_user)})
    return render_template("profile.html", user=user, reservation=reservation)


# Display page where admin can add new book:
@app.route("/admin_add_new_books")
@login_required
@admin_login_required
def admin_add_new_books():
    return render_template("admin_add_new_book.html")


@app.route("/admin_book_detail/")
@login_required
@admin_login_required
def admin_book_detail():
    id = request.args.get("id")
    book = db["book"].find_one({"_id": ObjectId(id)})
    users = db["reservation"].find_one({"id_book": str(id)})
    return render_template("admin_book_detail.html", book=book, user=users)


@app.route("/admin_show_book_search_result", methods=["post"])
@login_required
@admin_login_required
def admin_show_book_search_result():
    title = request.form.get("title")
    author = request.form.get("author")
    isbn = request.form.get("isbn")
    # session.get("mongodb_id")
    if title:
        book = db["book"].find({"title": title})
        return render_template("admin_show_book_search_result.html", book=book)
    if author:
        book = db["book"].find({"author": author})
        return render_template("admin_show_book_search_result.html", book=book)
    if isbn:
        book = db["book"].find({"_id": ObjectId(isbn)})
        return render_template("admin_show_book_search_result.html", book=book)
    else:
        book = db["book"].find({})
        return render_template("admin_show_book_search_result.html", book=book)


@app.route("/specific_book_information/")
def specific_book_information():
    find_user = session.get("mongodb_id")
    id = request.args.get("id")
    book = db["book"].find_one({"_id": ObjectId(id)})
    user = db["user"].find_one({"_id": ObjectId(find_user)})
    return render_template("specific_book_information.html", book=book, user=user)


@app.route("/show_book_search_result")
@login_required
def show_book_search_result():
    return render_template("show_book_search_result.html")


@app.route("/borrow_book/")
def borrow_book():
    find_user = session.get("mongodb_id")
    id = request.args.get("id")
    # using ObjectId from the bson.objectid module:
    book = db["book"].find_one({"_id": ObjectId(id)})
    find_user_id = db["user"].find_one({"_id": ObjectId(find_user)})
    return render_template("borrow_book.html", book=book, user=find_user_id)


@app.route("/signup", methods=["post"])
def signup_action():
    name = request.form["name"]
    surname = request.form["surname"]
    birthday = request.form["birthday"]
    pwd = request.form["pwd"]
    email = request.form["email"]
    # role will be setted up automatically,
    # in this project exists only one admin:
    role = "user"

    # login if username and email do not exist in db,
    # login if all fields are filled
    if request.method == "POST":
        emailCheck = db["user"].find_one({"email": email})
        if name == "" or surname == "" or birthday == "" or pwd == "" or email == "":
            return jsonify({"output": "Some of the inputs are null. Please try again."})
        if emailCheck:
            return jsonify({"output": "This email " + email + " is in use."})
        else:
            db["user"].insert_one(
                {
                    "name": name,
                    "surname": surname,
                    "birthday": birthday,
                    "pwd": pwd,
                    "email": email,
                    "role": role,
                }
            )
    return jsonify({"output": "You were signed up. Please log in."})


@app.route("/login", methods=["post"])
def login_action():
    pwd = request.form.get("pwd")
    email = request.form.get("email")
    emailCheck = db["user"].find_one({"email": email})
    if emailCheck:
        if emailCheck["pwd"] == pwd:
            session["mongodb_id"] = emailCheck["_id"]
            # role based authorization,
            # further session["role"] will be used in decorators @login_required and @admin_login_required:
            session["role"] = emailCheck["role"]
            if emailCheck["role"] == "user":
                return redirect(url_for("profile"))
            else:
                return redirect(url_for("admin_profile"))
        else:
            flash("Wrong password.")
            return redirect(url_for("login"))
    else:
        flash("There is no such an user.")
        return redirect(url_for("login"))


@app.route("/search_book_result", methods=["post"])
@login_required
def search_book_result():
    title = request.form.get("title")
    author = request.form.get("author")
    year = request.form.get("year")
    isbn = request.form.get("isbn")

    # does session work ?
    session.get("mongodb_id")
    if title:
        book_find = db["book"].find({"title": title})
        return render_template("show_book_search_result.html", books=book_find)
    if author:
        book_find = db["book"].find({"author": book_find})
        return render_template("show_book_search_result.html", books=book_find)
    if year:
        book_find = db["book"].find({"year": year})
        return render_template("show_book_search_result.html", books=book_find)
    if isbn:
        book_find = db["book"].find({"_id": ObjectId(isbn)})
        return render_template("show_book_search_result.html", books=book_find)
    else:
        book_find = db["book"].find({})
        return render_template("show_book_search_result.html", books=book_find)


@app.route("/submit_book_borrow", methods=["post"])
@login_required
def submit_book_borrow():
    # get form inputs:
    id_book = ObjectId(request.form["id_book"])
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    be_land = request.form["be_land"]

    land_start = datetime.now()
    land_end = land_start + timedelta(days=int(be_land))
    land_start = land_start.strftime("%Y-%m-%d")
    land_end = land_end.strftime("%Y-%m-%d")

    print("ATTENTION be_land" + str(be_land))
    print("land_start" + str(land_start))
    print("land_end" + str(land_end))

    id_user = ObjectId(request.form["id_user"])
    name = request.form["name"]
    surname = request.form["surname"]
    email = request.form["email"]
    contact_phone = request.form["contact_phone"]

    # check if object with this _id exists:
    isAvailable = db["book"].find_one({"_id": id_book})

    if isAvailable["isAvailable"] == "No":
        flash("The book is not available.")
        return redirect(url_for("borrow_book"))
    else:
        # change the availability of book:
        db["book"].update_one(
            {"_id": id_book},
            {"$set": {"isAvailable": "No"}},
        )
        # add to db collection:
        db["reservation"].insert_one(
            {
                "id_book": str(id_book),
                "id_user": str(id_user),
                "title": title,
                "author": author,
                "year": year,
                "be_land": be_land,
                "land_start": land_start,
                "land_end": land_end,
                "name": name,
                "surname": surname,
                "email": email,
                "contact_phone": contact_phone,
            }
        )
        flash("Done!")
        return redirect(url_for("borrow_book"))


@app.route("/delete_my_profile")
def delete_my_profile():
    find_user = session.get("mongodb_id")
    db["user"].delete_one({"_id": ObjectId(find_user)})
    flash("Your profile was deleted successfully")
    return redirect(url_for("login"))


@app.route("/return_borrowed_book/")
def return_borrowed_book():
    id = request.args.get("id")
    get_land_id = db["reservation"].find_one({"_id": ObjectId(id)})
    book = get_land_id.get("id_book")
    db["book"].update_one({"_id": ObjectId(book)}, {"$set": {"isAvailable": "Yes"}})
    db["reservation"].delete_one({"_id": ObjectId(id)})
    flash("Reservation was canceled.")
    return redirect(url_for("profile"))


# admin
@app.route("/admin_add_new_book", methods=["post"])
def admin_add_new_book():
    title = request.form["title"]
    author = request.form["author"]
    year = request.form["year"]
    page_number = request.form["page_number"]
    be_land = request.form["be_land"]
    description = request.form["description"]
    isAvailable = request.form["isAvailable"]

    if request.method == "POST":
        if title == None or author == None or year == None:
            flash("Some fields are empty.")
            return redirect(url_for("admin_add_new_books"))
        else:
            db["book"].insert_one(
                {
                    "title": title,
                    "author": author,
                    "year": year,
                    "page_number": page_number,
                    "be_land": be_land,
                    "description": description,
                    "isAvailable": isAvailable,
                }
            )
        flash("New book is added to library.")
        return redirect(url_for("admin_add_new_books"))


@app.route("/admin_update_borrow_day", methods=["post"])
def admin_update_borrow_day():
    id_up = request.form["id"]
    be_land = request.form["be_land"]

    if request.method == "POST":
        if be_land == None:
            return jsonify({"output": "Please fullfill the field."})
        else:
            db["book"].update_one(
                {"_id": ObjectId(id_up)},
                {"$set": {"be_land": be_land}},
            )
            return jsonify({"output": "Borrow days are successfully updated."})


@app.route("/admin_delete_book/")
def admin_delete_book():
    id = request.args.get("id")
    book = db["reservation"].find_one({"id_book": ObjectId(id)})
    # book can be deleted only if it is not borrowed already:
    if book != None:
        flash("This book was already borrowed and can't be deleted.")
        return redirect(url_for("admin_profile"))
    else:
        db["book"].delete_one({"_id": ObjectId(id)})
        flash("Book was deleted.")
        return redirect(url_for("admin_profile"))


@app.route("/logout")
def logout():
    session["mongodb_id"] = None
    session["role"] = None
    return redirect(url_for("login"))


# run application
if __name__ == "__main__":
    # app.run()
    app.run(host="0.0.0.0")
