import os
from base64 import b64encode  # encoding the image, line 79
from datetime import timedelta  # used on line 17



from flask import Flask, render_template, session
# start a flask app
app = Flask(__name__)
# set key to encrypt sessions
app.secret_key = '#modcom$541l0r5'
# import flask redirect, request
from flask import redirect
from flask import request

# Set session expiry lifetime if not in use, here its 2 mins
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=2)

# activate HTTP Only/Secure to True
# activate samesite to 'Lax'
# This reduces chances af a Sessions Fixation/Hijacking
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

# Home Page/Route
@app.route('/')
def home():
    return render_template('index.html')


# import pymysql to connect the database
import pymysql
import html   # html for escape

# function to ======================= hash password
import hashlib, binascii, os
# This function receives a password as a parameter
# its hashes and salts using sha512 encoding
def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')


# function to ======================= verify hashed password
def verify_password(hashed_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = hashed_password[:64]
    hashed_password = hashed_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == hashed_password



# Sell Page/Route
@app.route('/sell', methods=['post', 'get'])
def sell():
    if request.method == 'POST':
        # escape protects XSS/SQL Injection
        name = html.escape(str(request.form['name']))
        qtty = html.escape(str(request.form['qtty']))
        cost = html.escape(str(request.form['cost']))
        tel = html.escape(str(request.form['tel']))
        location = html.escape(str(request.form['location']))
        photo = request.files["photo"]  # get image from form
        # read image
        readImage = photo.read() # read the image file data, the real image
        # encode image to base64 and decode to utf-8
        encodedImage = b64encode(readImage).decode("utf-8")
        #pass 'encodedImage' to  your SQL on line 51

        conn = pymysql.connect('localhost', 'root', '', 'cyberdb')
        # Use prepared statements below: stops SQL Injection
        sql = "Insert into products_table(name,qtty,cost,tel,location, photo) values(%s,%s,%s,%s,%s, %s)"

        # Execute above sql, no values in sql
        cursor = conn.cursor()  # cursor executes sql
        try:
            cursor.execute(sql, (name, qtty, cost, tel, location, encodedImage))
            conn.commit()
            return render_template('sell.html',
                                       msg='Thank you for your request.')
        except:
            return render_template('sell.html',
                                    msg1='System problem. Try again later')
    else:
        return render_template('sell.html')



# # Register Page/Route
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # escape protects XSS/SQL Injection
        uname = html.escape(str(request.form['uname']))
        email = html.escape(str(request.form['email']))
        passw = str(request.form['passw'])  # NB: we do not escape the password, we hash it
        passw_again = str(request.form['passw_again'])
        gender = html.escape(str(request.form['gender']))
        nationality = html.escape(str(request.form['nationality']))
        #  more validation on inputs can be done here, empties, length, range

        import re

        # check if passw match with  - password again(confirm)
        #  more validation on inputs can be done here, empties, length, range
        if passw!=passw_again:
            return render_template('register.html',
                                   msg3="Password do not match!")
        # Check password strength  , this stops password brute force.
        elif (len(passw)<8):
                    return render_template('register.html',
                                  msg3="Must be more than 8 -ters")

        elif not re.search("[a-z]", passw):
                    return render_template('register.html',
                                  msg3="Must have small letters")

        elif not re.search("[A-Z]", passw):
                    return render_template('register.html',
                                  msg3="Must have capital letters")

        elif not re.search("[0-9]", passw):
                     return render_template('register.html',
                                  msg3="Must have a numbe")

        elif not re.search("[_@$]", passw):
                     return render_template('register.html',
                                  msg3="Must have a symbol")
        else:
            conn = pymysql.connect('localhost', 'root', '', 'cyberdb')
            # Use prepared statements below: stops SQL Injection
            sql = 'Insert into register(uname,email,passw,gender,nationality) values(%s,%s,%s,%s,%s)'
            cursor = conn.cursor()
            try:
                # password must be hashed, check how its provide below.
                # Its hashed, check hash function on line 42
                cursor.execute(sql, (uname, email, hash_password(passw), gender, nationality))
                conn.commit()
                return render_template('register.html',
                                      msg="Thank you for registering.")

            except:
                return render_template('register.html',
                                      msg2="Registration failed. Check your username")

    else:
        return render_template('register.html')


# Login Page/Route
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # escape protects XSS/SQL Injection
        uname = html.escape(str(request.form['uname']))
        passw = str(request.form['passw'])  # NB: we do not escape the password, we hash it
        #  more validation on inputs can be done here, empties, length, range etc
        # Confirm if above values are the same as those in the table. Use SQL
        conn = pymysql.connect('localhost', 'root', '', 'cyberdb')
        # Use prepared statements below: stops SQL Injection
        sql = "Select * from register where  uname=%s"
        cursor = conn.cursor()  # execute sql
        cursor.execute(sql , (uname))
        # get password for that username privided in the query

        # Cursor can provide the matched row, if any
        if cursor.rowcount == 0:
            return render_template('login.html', msg='Login failed. User not Found')
        elif cursor.rowcount == 1:
            # get password for user found by the query
            rows_found = cursor.fetchone()
            password_from_db = rows_found[2] # we retrieve the password at colm 3 of row found- count from zero
            # Now verify if this above password is same as what the user provided
            status = verify_password(password_from_db, passw) # check verify function on line 52
            if status ==True:
                 session['uname'] = uname   # create a session token
                 session.permanent = True   # to activate session expiry started on line 17
                 return redirect('/buy')

            else:
                # password do not match
                return render_template('login.html', msg='Password do not match')

        else:
            # Login error
            return render_template('login.html', msg='Error. Contact support')

    else:
        # load login form at the begining
        return render_template('login.html')


# Buy Page/Route, please the image
@app.route('/buy')
def view():
    # Control URL Access , below we check if user has a session
    # User must login to access this page
    if 'uname' in session:
        conn = pymysql.connect('localhost', 'root', '', 'cyberdb')
        sql = 'Select * from products_table'
        cursor = conn.cursor()
        cursor.execute(sql)

        # Check the number of rows found
        if cursor.rowcount < 1:
            return render_template('buy.html', msg='No products booked')
        else:
            rows = cursor.fetchall()
            # return all rows the templates, in templates check inage is decoded to utf and base 64
            return render_template('buy.html', rows=rows)

    else:
        return redirect('/buy')

# Checkout Page/Route, please the image
@app.route('/checkout')
def checkout():
    return render_template('checkout.html')


# Logout Route
@app.route('/logout')
def logout():
    session.pop('uname', None) # was set during login on line 95
    return redirect('/login') # session is now cleared


# Run the app
if __name__ == '__main__':
    app.run(debug=True)  # ranges from 1000 to 10000

# Create two folders templates and static
# Templates - HTML files
# static - css,js,images,videos,audios,everything else

