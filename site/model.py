import web, datetime

db = web.database(dbn='postgres', db='booklist', user='booklist')

def get_titles():
    return db.select('titles', order='id DESC')

def get_title(id):
    try:
        return db.select('titles', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_title(title, owned, read):
    db.insert('titles', title=title, owned=owned, read=read) #created=datetime.datetime.utcnow())

def del_title(id):
    db.delete('titles', where="id=$id", vars=locals())

def update_title(id, title, owned, read):
    db.update('titles', where="id=$id", vars=locals(),
        title=title, owned=owned, read=read)
