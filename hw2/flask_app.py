from flask import Flask, render_template, request, url_for, redirect
from email.mime.text import MIMEText
import smtplib
from email.message import EmailMessage
import sqlite3 as sql

app = Flask(__name__)

# Database initialisation
conn = sql.connect('database.db')
print("Opened database successfully")
conn.execute('CREATE TABLE IF NOT EXISTS comments (name TEXT, comment TEXT)')
print ("Table created successfully")
conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sendemail/", methods=['POST'])
def sendemail():
    if request.method == "POST":
        name = request.form['name']
        subject = request.form['Subject']
        email = request.form['_replyto']
        message = request.form['message']
        print(name, subject, email, message)

        your_name = "Ayush Kalla"
        your_email = "cisc3300fordham@gmail.com"
        your_password = "CB649B7D388A956AF99E63D7924FBD328F3B"

        # Logging in to our email account
        server = smtplib.SMTP('smtp.elasticemail.com', 2525)
        server.ehlo()
        server.starttls()
        server.login(your_email, your_password)

        # Sender's and Receiver's email address
        sender_email = "cisc3300fordham@gmail.com"
        receiver_email = "cisc3300fordham@gmail.com"

        msg = EmailMessage()
        msg.set_content("First Name : "+str(name)+"\nEmail : "+str(email)+"\nSubject : "+str(subject)+"\nMessage : "+str(message))
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        # Send the message via our own SMTP server.
        try:
            # sending an email
            server.send_message(msg)
        except:
            """pass"""
            print("error sending email")
    return "<h1>Returned from Mail Function</h1>"
    """return redirect('/')"""

@app.route("/newcomment/")
def new_comment():
    return render_template('comment.html')

@app.route('/addcomment/', methods=['POST', 'GET'])
def add_comment():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            comment = request.form['comment']

            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO comments (name,comment) VALUES (?,?)", (nm, comment))
                con.commit()
                print("Comment successfully added")
        except:
            con.rollback()
            print("Error in insert operation")
        finally:
            con.close()
            return redirect(url_for('index'))  # redirects back to the comment submission form


@app.route('/listcomments/')
def list_comments():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from comments")
    rows = cur.fetchall()
    return render_template("listcomments.html",rows = rows)

if __name__ == "__main__":
    app.run(debug=True)

