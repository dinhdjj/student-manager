from flask import render_template, request
from student_management import app



@app.route("/")
def doimatkhau():
    return render_template('doimatkhau.html')

@app.route("/login", methods=['post'])
def login():

    username = request.form['username']
    password = request.form['password']
    newpassword = request.form['new_password']

    if username == 'admin' and password == '123':
        if newpassword != password:
            return 'successful'
    return 'failed'

if __name__ == "__main__":
    app.run(debug=True)