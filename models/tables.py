# -*- coding: utf-8 -*-
from datetime import datetime

def get_first_name():
    name = 'Unidentified user'
    if auth.user:
        name = auth.user.first_name
    return name

def get_first_email():
    email = 'None'
    if auth.user:
        email = auth.user.email
    return email


def get_user_attending_info():
    value = 'None'
    if auth.user:
        value = auth.user.id
    return value

def get_user_info():
    value = 'None'
    if auth.user:
        value = auth.user.id
    return value

CATEGORY = ['Long-term', 'Short-term']

db.define_table('register',
                Field('name'),
                Field('event_name'),
                Field('user_id', db.auth_user),
                Field('phone'),
                Field('email'),
                Field('category'),
                Field('date_posted', 'datetime'),
                Field('prof_pic', 'upload'),
                Field('attend', 'boolean', default=False),
                #format = '%(title)s',
                )
db.define_table('attending',
                Field('user_attending', db.auth_user),
                Field('event_name','reference register'),
                )


db.define_table('messaging',
                Field('user_sender', db.auth_user),
                Field('user_recipient', db.auth_user),
                Field('message_body','text'),
                Field('read_status','boolean',default=False),
                Field('time_of_sending','datetime',default = datetime.utcnow())
                )



db.attending.event_name.requires = IS_EMPTY_OR(IS_IN_DB(db(db.register), 'register.id', '%(event_name)s'))
db.attending.user_attending.writable = False
db.attending.user_attending.readable = False
db.attending.user_attending.default = get_user_attending_info()

db.messaging.user_recipient.requires = IS_EMPTY_OR(IS_IN_DB(db(db.auth_user), 'auth_user.id', '%(first_name)s'))
db.messaging.user_sender.writable = False
db.messaging.user_sender.default = get_user_info()


db.register.id.readable = False
#db.register.name.default = get_first_name()
db.register.date_posted.default = datetime.utcnow()
#db.register.name.writable = False
db.register.date_posted.writable = False
db.register.name.default = get_first_name()
db.register.email.default = get_first_email()
db.register.user_id.default = auth.user_id
db.register.user_id.writable = db.register.user_id.readable = False
db.register.email.requires = IS_EMAIL()
db.register.category.requires = IS_IN_SET(CATEGORY,zero=None)
db.register.category.default = 'Misc.'
db.register.category.required = True
db.register.phone.requires = IS_MATCH('^1?((-)\d{3}-?|\(\d{3}\))\d{3}-?\d{4}$',
         error_message='not a phone number')
#db.register.price.requires = IS_FLOAT_IN_RANGE(0, 100000.0, error_message='The price should be in the range 0..100000')

