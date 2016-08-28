#!/usr/bin/env python

import sqlite3
from flask import Flask, render_template
from flask import g
from flask import request, redirect

import time
import os

###############
# Global vars #
###############
app = Flask(__name__)

THRESHOLD = 0.12
WEEK = time.strftime("%W")
YEAR = time.strftime("%Y")

####################
# Helper functions #
####################
def until_week_not_empty(week_number):
    while week_number > -1:
        query_str = str(week_number) + "-%"
        c = g.db.execute("SELECT rowid FROM FPL WHERE date LIKE (?)", (query_str,)).fetchone()

        if c is not None:
            break
        else:
            week_number = week_number - 1

    if week_number == -1:
        return(week_number)
    else:
        return(week_number)


def file_exists(file_name):
    if os.path.exists(file_name):
        return True
    else:
        return False

#############
# Functions #
#############
def connect_db(db_name):
    """Connects to the specified database"""
    db = sqlite3.connect(db_name)
    return db

####################
# Webapp Functions #
####################
@app.teardown_appcontext
def close_connection(exception):
    """Closes the database at the end of the request"""
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/')
def index():
    return redirect('/week/' + YEAR + '/' + str(WEEK))

@app.route('/week/<string:year>/<int:week_number>')
def week(year, week_number):
    # Open the DB
    if file_exists("db/" + year + ".db"):
        g.db = connect_db("db/" + year + ".db")
    else:
        return render_template('error.html')
    # The query to the DB returns a tuple for each hour of the day. E.g.
    # ('29-0', 0, 0.01, 0.31, 78)
    # 29-0 -> The first day of the week 29
    # 0    -> Hour 0:00 for this day
    # 0.01 -> The money we were charged
    # 0.31 -> kWh
    # 78   -> The average temperature
    week_number = until_week_not_empty(week_number)
    if week_number == -1:
        return render_template('error.html')

    # List of list of tuples.
    # The outter list represents a week
    # The inner loop represents a day of the week
    # The tuple represents the hours of that day
    week = []
    # List of tuples
    day_summary = []
    for day in range(1, 8):
        week_day = str(week_number) + "-" + str(day)
        # Only append data to week when we find an entry for that day in the DB
        if g.db.execute("SELECT rowid FROM FPL WHERE date=?", (week_day,)).fetchone():
            week.append(g.db.execute("SELECT * FROM FPL WHERE date=?", (week_day,)).fetchall())
            day_summary.append(g.db.execute("SELECT * FROM SUMMARY WHERE date=?", (week_day,)).fetchall()[0])

    return render_template('week.html',
            summary         = day_summary,
            year            = year,
            week            = week,
            week_number     = int(week_number),
            hours_in_a_day  = list(range(0, 24)),
            threshold       = THRESHOLD)
