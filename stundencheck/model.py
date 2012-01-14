from datetime import datetime 

from stundencheck.core import db


class School(db.Model):
    __tablename__ = 'school'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return self.name


class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    group = db.Column(db.Unicode)
    course = db.Column(db.Unicode)
    session = db.Column(db.Unicode)
    reason = db.Column(db.Unicode)
    
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    school = db.relationship(School,
                backref=db.backref('events', lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)


class Report(db.Model):
    __tablename__ = 'report'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Unicode)

    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    event = db.relationship(Event,
                backref=db.backref('reports', lazy='dynamic'))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow)

    def __repr__(self):
        return self.email



