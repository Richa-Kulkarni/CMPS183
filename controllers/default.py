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
def events():
    """View all events."""
    response.flash = T("Aaaaaall da events!")

    something = db().select(db.register.ALL)
    
    start_idx = 1 
    
    q= (db.register) 

    form = SQLFORM.grid(q, args=request.args[:start_idx],
        fields=[db.register.user_id, db.register.event_name,
                db.register.date_posted, db.register.name,
                db.register.event_name, db.register.email, 
                db.register.category,
                db.register.prof_pic],
        editable=False, deletable=False,
        paginate=10,
        )
    
    return dict(something=something, form=form)
        
def profile():
    #return dict(form=auth.profile(edit= False))
    return dict(form=auth.profile())


def resetpass():
    return dict(form=auth.request_reset_password())

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
