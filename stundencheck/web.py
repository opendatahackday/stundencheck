#coding: utf-8
from collections import defaultdict
from datetime import datetime

from colander import Invalid
from flask import Flask, g, request, render_template, abort, flash, json
from flask import url_for, redirect, jsonify
from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore

from stundencheck.core import app, db
from stundencheck.model import Event, Report, School

admin_datastore = SQLAlchemyDatastore((School, Event, Report), db.session)
admin_blueprint = admin.create_admin_blueprint(admin_datastore)
app.register_blueprint(admin_blueprint, url_prefix='/admin')

@app.template_filter()
def datetime_format(dt):
    return dt.strftime("%d.%m.%Y")

@app.route("/list")
def list():
    events = db.session.query(Event)
    return render_template('list.tmpl', events=events)

@app.route("/school/<id>")
def school(id):
    school = db.session.query(School).filter_by(id=id).first()
    if school is None:
        abort(404)
    return render_template('school.tmpl', school=school)



@app.route("/")
def index():
    schools = db.session.query(School)
    return render_template('index.tmpl', schools=schools)

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(port=5007)

