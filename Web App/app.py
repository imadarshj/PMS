from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '295f713dafe6d6674418995c7bbba2ae'

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    forms = RegistrationForm()
    if forms.validate_on_submit():
        flash(f'Account created for {forms.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=forms)

@app.route("/login", methods=['GET', 'POST'])
def login():
    forms = LoginForm()
    if forms.validate_on_submit():
        if forms.email.data == 'admin@blog.com' and forms.password.data == 'password':
            flash('You have been logged in', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template('login.html', title='Login', form=forms)

if __name__ == '__main__':
    app.run(debug=True)



