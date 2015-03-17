# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
#########################################################################

@auth.requires_login()
def index():

    response.flash = T("CMPS183 Project!")

    something = db().select(db.register.ALL)
    
    
    return dict(something=something)

@auth.requires_login()
def register():
    """Register an event."""
    form = SQLFORM(db.register)
    if form.process().accepted:
        #Successful processing.
        session.flash = T('Registered Event')
        redirect(URL('default', 'index'))
    return dict(form=form)

@auth.requires_login()
def mycal():
    rows=db(db.register.name==auth.user.id).select()
    return dict(rows=rows)

@auth.requires_login()
def mymap():
    #rows=db(db.register.name==auth.user.id)(db.register.f_start_time>=request.now).select()
    #return dict(rows=rows)
    from gluon.tools import geocode
    latitude = longtitude = ''
    form=SQLFORM.factory(Field('search'), _class='form-search')
    form.custom.widget.search['_class'] = 'input-long search-query'
    form.custom.submit['_value'] = 'Search'
    form.custom.submit['_class'] = 'btn'
    if form.accepts(request):
        address=form.vars.search
        (latitude, longitude) = geocode(address)
    else:
        (latitude, longitude) = ('','')
    return dict(form=form, latitude=latitude, longitude=longitude)

def enrollInEvent():
    
    form = SQLFORM(db.attending)
    if form.process().accepted:
        #Successful processing.
        session.flash = T('Registered Event')
        redirect(URL('default', 'index'))
    return dict(form=form)

def sendMessage():
    
    form = SQLFORM(db.messaging)
    if form.process().accepted:
        #Successful processing.
        session.flash = T('Message Sent')
        redirect(URL('default', 'index'))
    return dict(form=form)

def userInbox():
    
    q = db.messaging.user_recipient == auth.user.id
    
    form = SQLFORM.grid(q)
    
    return locals()
    

@auth.requires_login()
def events():
    show_all = request.args(0) == 'all'
    q = (db.register) if show_all else(db.register.attend == True)

    def generate_toggle_attend(row):
        b = ''
        if auth.user_id == row.user_id:
            b = A('Toggle', _class='btn', _href=URL('default', 'toggle_attend', args=[row.id], user_signature=True))
            return b

    if show_all:
        button = A('See attended events', _class='btn', _href=URL('default', 'events', user_signature=True))
    else:
        button = A('See all events', _class='btn', _href=URL('default', 'events', args=['all'], user_signature=True))

    links = [
        dict(header='', body = generate_toggle_attend),
    ]
    
    """View all events."""
    response.flash = T("Aaaaaall da events!")
    
    something = db().select(db.register.ALL)

    start_idx = 1 if show_all else 0
    create=(auth.user_id is not None)
    form = SQLFORM.grid(q, args=request.args[:start_idx],
        fields=[db.register.user_id, db.register.event_name,
                db.register.date_posted, db.register.name,
                db.register.event_name, db.register.email, 
                db.register.category,
                db.register.prof_pic,
                db.register.attend],
        editable=False, deletable=False,
        paginate=10,
        links = links,
        )
    
    return dict(something=something, form=form, button=button)

@auth.requires_signature()
@auth.requires_login()
def toggle_attend():
    item = db.register(request.args(0)) or redirect(URL('default', 'events'))
    item.update_record(attend = not item.attend)
    redirect(URL('default', 'events'))


def generate_history_button(row):
    # If our profile, we can view history of attended events.
    
    b = A('History', _class='btn', _href=URL('default', 'history', args=[row.id], user_signature=True))
    return b
    
links = [
    dict(header='', body = generate_history_button),
]

@auth.requires_signature()
@auth.requires_login()
def history():
    q = db.register.attend


    f = SQLFORM.grid(q,
        fields=[db.register.user_id, db.register.event_name,
                db.register.date_posted, db.register.name,
                db.register.event_name, db.register.email, 
                db.register.category,
                db.register.prof_pic,
                db.register.attend],
        editable=False, deletable=False,
        paginate=10,
        )
    return dict(f=f)
        
        
        
def profile():
    #return dict(form=auth.profile(edit= False))
    return dict(form=auth.profile())



def view():
    """View profile."""
    response.flash = T("User Profile")
    form = ''
    
    something = db(db.auth_user.id == auth.user_id).select().first()
    

    
    url = URL('download')
    
    form = SQLFORM(db.auth_user, record = something, readonly=True, upload=url)
   
    
    return dict(something=something, form=form)



@auth.requires_login()
@auth.requires_signature()
def edit():
    """Edit profile."""
    p = db.bio(request.args(0)) or redirect(URL('default', 'index'))
    if p.user_id != auth.user_id:
        session.flash = T('Not authorized.')
        redirect(URL('default', 'index'))
    profile = SQLFORM(db.bio, record=p)
    if profile.process().accepted:
        session.flash = T('Updated')
        redirect(URL('default', 'index'))
    return dict(profile=profile)



def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_login() 
def api():
    """
    this is example of API with access control
    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
    """
    from gluon.contrib.hypermedia import Collection
    rules = {
        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
        }
    return Collection(db).process(request,response,rules)
