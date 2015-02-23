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
                #format = '%(title)s',
                )




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

