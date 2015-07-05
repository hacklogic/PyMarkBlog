# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2015 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash


import markdown
from flask import Flask
from flask import render_template
from flask import Markup
import markdown2



# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='admin'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def key_exist(key):
    if request.form.has_key(key):
        return True
    else:
        return False


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


###################################################################Test Mode##
@app.route('/test1/')
def show_blogs():
    
    return render_template('test1.html')
    #return render_template('show_blog.html', **locals())
    

@app.route('/test/')
def teste():
    return render_template('indextest2.html')


@app.route('/markdown', methods=['POST'])
def post_markdown():
    #request.form['title']
    #request.form['content']
    #print request.form['content']
    #content = Markup(markdown.markdown(request.form['content']))
    content = markdown2.markdown( "#"+ request.form['title']+ "\n" +request.form['content'], extras=["code-friendly","code-color", "cuddled-lists","tables","footnotes","pyshell","toc"])

    return content



###################################################################User Mode##

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('select id, title, content from blog order by id desc LIMIT 5')
    rows = cur.fetchall()
    #content = Markup(markdown.markdown(entries))
    #print entries
    result = []
    for row in rows:
        content = markdown2.markdown(row["content"], extras=["code-friendly","code-color", "cuddled-lists","tables","footnotes","pyshell","toc"])
        #content = Markup(markdown.markdown(row["content"]))
        result.append((row["id"], row["title"], content))
    #entries = newentries
    print result
    
    return render_template('index.html', result=result)
    
 


@app.route('/blog/')
@app.route('/blog/<id>')
def show_post(id=None):
    #===========================================================================
    # print "======================="
    # print id
    # f = request.form
    # for key in f.keys():
    #     for value in f.getlist(key):
    #         print key,":",value
    #===========================================================================

    if id:
        db = get_db()
        cur = db.execute('select id, title, content from blog where id = ?', [id])
        row = cur.fetchone()
        if row:
            #content = Markup(markdown.markdown(entries))
            #print entries
            result = []
            content = markdown2.markdown(row["content"], extras=["code-friendly","code-color", "cuddled-lists","tables","footnotes","pyshell","toc"])
            #content = Markup(markdown.markdown(row["content"]))
            result.append((row["id"], row["title"],content))
            #entries = newentries
            print result
            
            return render_template('blog.html', result=result)
            #return render_template('show_blog.html', **locals())
        else:
            abort(404)
    else:
        db = get_db()
        cur = db.execute('select id, title, content from blog order by id desc')
        rows = cur.fetchall()
        #content = Markup(markdown.markdown(entries))
        #print entries
        result = []
        for row in rows:
            content = markdown2.markdown(row["content"], extras=["code-friendly","code-color", "cuddled-lists","tables","footnotes","pyshell","toc"])
            #content = Markup(markdown.markdown(row["content"]))
            result.append((row["id"], row["title"], content))
        #entries = newentries
        print result
        
        return render_template('blog.html', result=result)
        #return render_template('show_blog.html', **locals())



#===============================================================================
# Admin Mode
#===============================================================================




@app.route('/admin/')
def admin_post():
    if not session.get('logged_in'):
        #abort(401)
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select title, id, content from blog order by id desc')
    rows = cur.fetchall()
    #content = Markup(markdown.markdown(entries))
    #print entries
    result = []
    for row in rows:
        result.append((row["title"],row["id"]))
    print result
        
    #entries = newentries
    #print newentries
    
    return render_template('admin.html', result=result)
    #return render_template('show_blog.html', **locals())


@app.route('/admin/edit/')
def new_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('editor_new.html')
    #return render_template('show_blog.html', **locals())

@app.route('/admin/edit/<id>', methods=['GET'])
def edit_post(id=None):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    if id:
        db = get_db()
        cur = db.execute('select id, title, content from blog where id = ?', [id])
        row = cur.fetchone()
        if row:
            #content = Markup(markdown.markdown(entries))
            #print entries
            result = []
            result.append(row["id"])
            result.append(row["title"])
            result.append(row["content"])
            print result
            #entries = newentries
            #print newentries
            
            return render_template('editor_update.html', result=result)
        else:
            abort(404)
    abort(404)



       
@app.route('/admin/update', methods=['POST'])
def update_post():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    print request.form['type']
    print request.form['title']
    print request.form['content']
    if request.form['type'] == 'new':
        db.execute("INSERT into blog (title, content, post_time) values (?, ?, datetime('now'))", [request.form['title'], request.form['content']])
        db.commit()
    elif request.form['type'] == 'update':
        db.execute('UPDATE blog set title=?, content=? where id= ?', [request.form['title'], request.form['content'], request.form['id']])
        db.commit()
    flash('New blog was successfully updated')
    return redirect(url_for('admin_post'))


@app.route('/admin/del/<id>', methods=['GET'])
def delete_post(id=None):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE from blog where id = ?',[id])
    db.commit()
    flash('blog was successfully deleted')
    return redirect(url_for('admin_post'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('admin_post'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))