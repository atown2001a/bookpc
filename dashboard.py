from flask import render_template, redirect, url_for, session, request
from datetime import datetime
from booking import PCS_BY_BRANCH, TIME_SLOTS

def register(app):

    @app.route("/dashboard")
    def dashboard():
        if "username" in session and "branch" in session:
            branch = session["branch"]

            pcs = PCS_BY_BRANCH.get(branch, [])
            times = TIME_SLOTS
            msg = session.pop("msg", None)
   
            return render_template(
                "dashboard.html",
                username=session["username"],
                fullname=session.get("fullname"),
                branch=branch,
                pcs=pcs,
                times=times,
                msg=msg
            )

        return redirect(url_for("login"))


#    @app.route("/about")
#   def about():
#        return render_template("about.html")


    @app.route("/logout")
    def logout():
        session.pop("username", None)
        session.pop("branch", None)
        session.pop("fullname", None)
        return redirect(url_for("login"))
