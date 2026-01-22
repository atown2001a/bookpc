from flask import render_template, redirect, url_for, session, request
import json, os
from datetime import datetime

PCS_BY_BRANCH = {
    "Derry": ["TCm-Derry-01", "TCm-Derry-02"],
    "Bally": ["TCm-Bally-01", "Tcm-Bally-02"],
}

TIME_SLOTS = ["09:00", "10:00", "11:00", "12:00", "13:00", "14:00"]


def register(app):

    @app.route("/bookpc", methods=["POST"])
    def bookpc():
        if "username" not in session or "branch" not in session:
            return redirect(url_for("login"))

        pc = request.form.get("pc")
        time = request.form.get("time")
        date = request.form.get("date")

        book_date = datetime.strptime(date, "%Y-%m-%d").date()
        if book_date < datetime.today().date():
           session["msg"] = "❌ Can't book past dates"
           return redirect(url_for("dashboard"))

        # record booking to JSON
        os.makedirs("data", exist_ok=True)
        path = "data/bookings.json"

        booking = {
            "username": session["username"],
            "branch": session["branch"],
            "pc": pc,
            "time": time,
            "date": date,
            "created": datetime.now().isoformat()
        }

        if os.path.exists(path):
            with open(path) as f:
                bookings = json.load(f)
        else:
            bookings = []

        duplicate = any( 

            b["branch"] == session["branch"] and 
            b["pc"] == pc and
            b["date"] == date and 
            b["time"] == time 
            for b in bookings 
        ) 
       # if not duplicate: 
       #    session["msg"] = "\u2705 Booking Confirmed" 
       #    return redirect(url_for("dashboard"))

        if duplicate: 
           session["msg"] = "\u274c Already booked for that PC/time" 
           return redirect(url_for("dashboard"))

        bookings.append(booking)

        with open(path, "w") as f:
            json.dump(bookings, f, indent=2)
        session["msg"] = "\u2705 Booking Confirmed" 
        print("BOOKING:", booking)
        return redirect(url_for("dashboard"))
