import sqlite3
import sys
import logging

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from flask.logging import default_handler
from werkzeug.exceptions import abort
i = 0
count = 0

# Function to get a database connection.
# This function connects to database with the name `database.db`
def get_db_connection():
    global i
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    i+=1
    num_conn= str(i)
    app.logger.info("connection number:" + num_conn + '\n')
    return (connection)

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Function to count posts
def count_post():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    count=(len(cursor.fetchall()))
    connection.commit()
    connection.close()
    num_count= str(count)
    app.logger.info("number of posts in db:" + num_count + '\n')
    return count


# Define the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    stdout_pablo = sys.stdout
    sys.stdout.write("main page" + '\n' )
    sys.stdout = stdout_pablo
    app.logger.info('main page')
    return render_template('index.html', posts=posts)


# Define the /metrics
@app.route('/metrics')
def metrics():
   count1 = count_post()
   response = app.response_class(
            response=json.dumps({"status":"success","code":0,"data":{"db_connection_count":i,"post_count":count1}}),
            status=200,
            mimetype='application/json'
    )
   stdout_pablo = sys.stdout
   sys.stdout.write("metrics page" + '\n' )
   sys.stdout = stdout_pablo
   app.logger.info('metrics web page')
   return response

# Define the /healthz
@app.route('/healthz')
def healthz():
   response = app.response_class(
            response=json.dumps({"result":"ok - healthy"}),
            status=200,
            mimetype='application/json'
    )

   return response


# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      stdout_pablo = sys.stdout
      stderr_pablo = sys.stderr
      sys.stdout.write('error 404' + '\n')
      sys.stdout = stdout_pablo
      sys.stderr.write("error 404" + '\n' )
      sys.stderr = stderr_pablo
      app.logger.error('wrong id')
      return render_template('404.html'), 404
    else:
      stdout_pablo = sys.stdout
      postid = str(post_id)
      sys.stdout.write('post_ok_id:' + postid + '\n')
      sys.stdout = stdout_pablo
      app.logger.info('post_ok_id:' + postid + '\n')
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    stdout_pablo = sys.stdout
    sys.stdout.write("about" + '\n' )
    sys.stdout = stdout_pablo
    app.logger.info("about page")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
            stderr_pablo = sys.stderr
            sys.stderr.write("error no title" + '\n' )
            sys.stderr = stderr_pablo
            stdout_pablo = sys.stdout
            sys.stdout.write('no title ' + title + '\n')
            sys.stdout = stdout_pablo
            app.logger.error("error no title given" + '\n' )
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            connection.close()
            stdout_pablo = sys.stdout
            sys.stdout.write('title: ' + title + '\n')
            sys.stdout = stdout_pablo
            app.logger.info('title: ' + title + '\n')
            return redirect(url_for('index'))

    return render_template('create.html')

# start the application on port 3111
if __name__ == "__main__":
   logging.basicConfig(level=logging.DEBUG)
   app.run(host='0.0.0.0', port='3111')

