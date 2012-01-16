#coding: utf-8
from collections import defaultdict
from datetime import datetime

import colander
from flask import Flask, g, request, render_template, abort, flash, json
from flask import url_for, redirect, jsonify
from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore

from stundencheck.core import app, db
from stundencheck.model import Event, Report, School

admin_datastore = SQLAlchemyDatastore((School, Event, Report), db.session)
admin_blueprint = admin.create_admin_blueprint(admin_datastore)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


class SchoolType(colander.SchemaType):

    def serialize(self, node, struct):
        return struct.id

    def deserialize(self, node, struct):
        return db.session.query(School).filter_by(id=struct).first()


class ReportSchema(colander.MappingSchema):
    school = colander.SchemaNode(SchoolType())
    group = colander.SchemaNode(colander.String())
    course = colander.SchemaNode(colander.String())
    session = colander.SchemaNode(colander.String())
    reason = colander.SchemaNode(colander.String())
    email = colander.SchemaNode(colander.String())



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

@app.route("/report")
def report():
    school_id = request.args.get('school')
    schools = db.session.query(School)
    return render_template('report.tmpl', schools=schools,
            school_id=school_id)

@app.route("/report", methods=['POST'])
def report_save():
    try:
        data = dict(request.form.items())
        data = ReportSchema().deserialize(data)
        # TODO: fuzzy match events.
        event = Event()
        event.school = data['school']
        event.group = data['group']
        event.course = data['course']
        event.session = data['session']
        event.reason = data['reason']
        db.session.add(event)
        report_ = Report()
        report_.event = event
        report_.email = data['email']
        db.session.add(report_)
        db.session.commit()
        return redirect(url_for('school', 
            id=event.school.id))
    except colander.Invalid, i:
        #print i
        return report()

@app.route("/")
def index():
    schools = db.session.query(School)
    count = db.session.query(Report).count()
    return render_template('index.tmpl', schools=schools, 
            count=count)

if __name__ == '__main__':
    db.create_all()
    app.debug = True
    app.run(port=5007)

