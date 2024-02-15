from flask import Flask
import sqlite3
from flask import render_template, request
import random
from flask import g

app = Flask(__name__)

#get message database
def get_message_db():
    if 'message_db' not in g:
        g.message_db = sqlite3.connect('messages_db.sqlite')
    cursor = g.message_db.cursor()
  
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, handle TEXT, message TEXT)')
    return g.message_db
    
#create insert function
def insert_message(request): 
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO messages (handle, message) VALUES (?, ?)', (request.form['user'], request.form['message']))
    db.commit() 
    db.close()

#random message function 
def random_messages(n):
    #add message to the database
    db = get_message_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM messages')
    messages = cursor.fetchall()
  
    db.close()

    #return our result
    return random.sample(messages, min(n, len(messages)))



#route from function to homepage    
@app.route('/', methods=['GET'])
def home():
    return render_template('base.html')

#route to submit page
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    message = None
    user = None
    if request.method == 'POST':
        user = request.form['user']
        message = request.form['message']
        insert_message(request)
    return render_template('submit.html', user=user, message=message)

#route to view message page 
@app.route('/messages', methods=['GET'])
def messages(): 
    #generate random messages
    messages = random_messages(5)
    return render_template('view.html', messages=messages)



#route functions
with open('base.html', 'w') as f:
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{% block title %}Message Bank{% endblock %}</title>
        <link rel = "stylesheet" type = "text/css" href="{{ url_for('statis', filename='style.css') }}">
    </head>
    <body>
        <div class="center">
        {% block header %}
        <h1>Welcome to the message bank!</h1>
        <nav>
            <a href="/submit">Submit Message</a> |
            <a href="/messages">View Messages</a>
        </nav>
        {% endblock %}
        {% block content %}
        {% endblock %}
        </div>
    </body>
    </html>
    """
    f.write(html_content)

with open('submit.html', 'w') as f:
    html_content = """
    {% extends "base.html" %}
    {% block content %}
    <h2>Submit your message below:</h2>
    <form method="POST"> 
        <label for="message">Your message:</label><br>
        <input type="text" name="user_message">Your name or handle:</label><br>
        <input type="submit" value="Submit">
    </form>
    {% if message %}
    <p>Thank you for your submission, {{ user }}!</p>
    {% endif %}
    {% endblock %}
    """
    f.write(html_content)

with open('view.html', 'w') as f:
    html_content = """
    {% extends "base.html" %}
    {% block content %}
    <h1>Messages</hi>
    <u1>
    {% for message in messages %}
        <li>{{ message[1] }}: {{ message[2] }}</li>
    {% endfor %}
    </ul>
    {% endblock %}
    """
    f.write(html_content)

with open('style.css', 'w') as f:
    html_content = """
    html {
        font-family: cursive; 
        background-color: rgb(250, 209, 228); 
        padding: 1rem; 
    }

    body {
        background-color: purple; 
        font-family: san-serif; 
        color: darkpurple
    }

    .center {
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        height: 100vh; 
        text-align: center; 
    }
    """
    f.write(html_content)