#!/usr/bin/env python

#ALLDIRS = ['/var/www/jessamin/booklist']
import sys, os
abspath = os.path.dirname(__file__)
sys.path.append(abspath)
os.chdir(abspath)

""" Jessamin's booklist """
# Import our modules and declare our template path
import web
import model
import site 

# Remember original sys.path.
#prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
#for directory in ALLDIRS:
#    site.addsitedir(directory)

# Reorder sys.path so new directories at the front.
#new_sys_path = [] 
#for item in list(sys.path): 
#    if item not in prev_sys_path: 
#        new_sys_path.append(item) 
#        sys.path.remove(item) 
#sys.path[:0] = new_sys_pat


#render = web.template.render('templates/')

# URLs

urls = (
  '/', 'index',
  '/view/(\d+)', 'view',
  '/new', 'new',
#  '/edit/(.*)', 'edit'
  '/edit/(\d+)', 'edit',
  '/delete/(\d+)', 'delete',
)

# Templates

t_globals = {
        'datestr': web.datestr
}
render = web.template.render('templates/', base='base', globals=t_globals)
#render = web.template.render('templates/')

# Edit form

#editform = form.Form(
#    form.Textbox("title",
#    class_="form-control",
#    ),
#    form.Textbox("firstname",
#    class_="form-control",
#    ),
#    form.Textbox("lastname",
#    class_="form-control",
#    ),
#    form.Checkbox('owned',
#    class_="form-control",
#    ),
#    form.Checkbox('read',
#    class_="form-control"))

#class index:
#    def GET(self,name):
#	i = web.input(name=None)
#        return render.index(i.name)

class index:
    def GET(self):
        """ List Books with search function """
        titles = model.get_titles()
        return render.index(titles)

class view:
    def GET(self,id):
        """ view single title """
        title = model.get_title(int(id))
        return render.view(title)

class new:

    form = web.form.Form(
        web.form.Textbox("title", 
            class_="form-control"),  
        web.form.Textbox("firstname",
            class_="form-control"),  
        web.form.Textbox("lastname",
            class_="form-control"),  
        web.form.Checkbox('owned',
            class_="form-control"),  
        web.form.Checkbox('read',
            class_="form-control"),
        web.form.Button('Submit')
    )

    def GET(self):
        form = self.form()
        return render.new(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.new(form)
        model.new_title(form.d.title, form.d.owned, form.d.read)
        raise web.seeother('/')
        
class edit:

    def GET(self,id):
        title = model.get_title(int(id))
        form = new.form()
        form.fill(title)
        return render.edit(title, form)

    def POST(self,id):
        form = new.form()
        post = model.get_title(int(id))
        if not form.validates():
            return render.edit(post,form)
        model.update_title(int(id), form.d.title, form.d.owned, form.d.read)
        raise web.seeother('/')
        
app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
