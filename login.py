from flask import render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
import os


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    submit = SubmitField("Login")


def find_auth_module():
    search_dirs = [
        "/srv",
        "/mnt/Authy/bookpc",
    ]

    auth_module_name = "auth"

    for directory in search_dirs:
        print("Searching in:", directory)
        auth_module_path = os.path.join(directory, auth_module_name + ".py")
        if os.path.isfile(auth_module_path):
            print("Auth module file found at:", auth_module_path)
            return auth_module_path

    print("Auth module file not found.")
    return None


def register(app):
    @app.route("/", methods=["GET", "POST"])
    def login():
        auth_module_path = find_auth_module()

        if auth_module_path:
            try:
                from importlib.machinery import SourceFileLoader
                auth_module = SourceFileLoader("auth", auth_module_path).load_module()
                authenticate = auth_module.authenticate

                print("Authentication module found at:", auth_module_path)

                form = LoginForm(request.form)

                if request.method == "POST" and form.validate():
                    username = form.username.data
                    password = form.password.data

                    branch, fullname = authenticate(username, password)

                    if branch:
                        session["username"] = username
                        session["branch"] = branch
                        session["fullname"] = fullname
                        return redirect(url_for("dashboard"))

                    return render_template("login.html", form=form, error="Invalid username or password")

                return render_template("login.html", form=form)

            except Exception as e:
                print("Error importing or executing the authenticate function:", e)

        else:
            print("Auth module file not found.")

        form = LoginForm()
        return render_template("login.html", form=form)
