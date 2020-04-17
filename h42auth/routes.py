from flask import flash, redirect, render_template, url_for, request, session
from flask_login import current_user, login_user, logout_user
from flask_cors import cross_origin
from h42auth import app, forward, tydb
from h42auth.forms import LoginForm
from h42auth.user import User

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html.j2', title='Page not found', url=request.base_url), 404

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html.j2', title='Home')

@app.route('/register')
def register_start():
    return redirect(url_for('home'))

@cross_origin(supports_credentials=True)
@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    fa = None
    if 'forward' in request.args:
        fa = forward.ForwardAuth.create_from_url(request.args['forward'])
        session['forward'] = fa.toJson()
    if 'forward' in session:
        fa = forward.ForwardAuth.create_from_json(session['forward'])
    if current_user.is_authenticated:
        if fa:
            return redirect(fa.url)
        return redirect(url_for('home'))
    loform = LoginForm()
    if loform.validate_on_submit():
        user = User.findUserByName(loform.username.data)
        if user is None or not user.check_password(loform.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth_login'))
        login_user(user, remember=True)
        return redirect(url_for('home'))
    return render_template('login.html.j2', title='Sign In', form=loform, forward=fa)

@app.route('/auth/logout')
def auth_logout():
    logout_user()
    return redirect(url_for('home'))

@cross_origin(supports_credentials=True)
@app.route('/forward/auth')
def forward_auth():
    if request.headers.has_key('X-Forwarded-Server'):
        fa = forward.ForwardAuth.create_from_headers(request.headers)
        if current_user.is_authenticated:
            response = make_response("OK")
            response.headers['X-Forward-Auth-User'] = current_user.username
            session.clear()
            return response
        return redirect(url_for('auth_login', forward=fa.toUrl()))
    else:
        return redirect(url_for('home'))
