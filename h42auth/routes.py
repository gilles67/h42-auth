from flask import flash, redirect, render_template, url_for, request, session, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_cors import cross_origin
from h42auth import app, forward
from h42auth.forms import LoginForm, PasswordChange
from h42auth.user import User
from h42auth.forward import ForwardAuth


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_404.html.j2', title='Page not found', url=request.base_url), 404

@app.route('/')
@app.route('/home')
def home():
    fasessions = None
    title = "Home"
    if current_user.is_authenticated:
        title = "Dashboard"
        fasessions = ForwardAuth.get_user_sessions(current_user)
    return render_template('home.html.j2', title=title, user=current_user, fasessions=fasessions)

@app.route('/user/register')
@login_required
def register_start():
    return redirect(url_for('home'))

@app.route('/user/enroll')
def user_enroll_device():





    fasessions = None
    title = "Home"
    if current_user.is_authenticated:
        title = "Dashboard"
        fasessions = ForwardAuth.get_user_sessions(current_user)
    return render_template('client_enroll.html.j2', title=title, user=current_user, fasessions=fasessions)



@app.route('/user/password', methods=['GET', 'POST'])
@login_required
def user_password():
    passform = PasswordChange()
    if passform.validate_on_submit():
        if not current_user.check_password(passform.password_old.data):
            flash('Wrong old password', 'error')
            return redirect(url_for('user_password'))
        if not passform.password_new.data == passform.password_check.data :
             flash('The new password and the check not th same', 'error')
             return redirect(url_for('user_password'))
        if passform.password_old.data == passform.password_new.data:
             flash('The new password and the old one is the same, seriously ? ', 'error')
             return redirect(url_for('user_password'))
        current_user.set_password(passform.password_new.data)
        current_user.save()
        flash('Password change successfully, please sign in with the new password')
        return redirect(url_for('auth_logout'))

    return render_template('change_password.html.j2', title='Change password', user=current_user, form=passform)

@cross_origin(supports_credentials=True)
@app.route('/auth/login', methods=['GET', 'POST'])
def auth_login():
    fa = None
    if 'forward' in request.args:
        fa = ForwardAuth.find_auth(request.args['forward'])
        session['forward'] = fa.token
    if (fa == None) & ('forward' in session):
        fa = ForwardAuth.find_auth(session['forward'])
    if current_user.is_authenticated:
        if fa:
            fa.set_user(current_user)
            fa.save()
            return redirect(fa.url)
        return redirect(url_for('home'))

    loform = LoginForm()
    if loform.validate_on_submit():
        user = User.findUserByName(loform.username.data)
        if user is None or not user.check_password(loform.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth_login'))
        login_user(user, remember=True)
        if fa:
            fa.set_user(user)
            fa.save()
            session.pop('forward')
            return redirect(fa.url)
        return redirect(url_for('home'))
    return render_template('login.html.j2', title='Sign In', form=loform, forward=fa, domain=app.config['SO_DOMAIN'])

@app.route('/auth/logout')
def auth_logout():
    ForwardAuth.user_logout(current_user)
    logout_user()
    return redirect(url_for('home'))

@cross_origin(supports_credentials=True)
@app.route('/forward/auth')
def forward_auth():
    fa = None
    if request.headers.has_key('X-Forwarded-Server'):
        if '_fa_token' in request.cookies:
            fa = ForwardAuth.find_auth(request.cookies['_fa_token'])
            if fa:
                #fa.check_headers(request.headers)
                if fa.is_authenticated:
                    response = make_response("OK")
                    response.set_cookie('_fa_token', fa.token, expires=fa.expires)
                    response.headers['X-Forward-Auth-User'] = fa.user
                    #response.delete_cookie('_fa_token')
                    #fa.destroy()
                    return response
        # Prepare new session
        fa = ForwardAuth()
        fa.check_headers(request.headers)
        fa.save()

        #Clean sessions
        ForwardAuth.clean_session()

        #Redirect to login
<<<<<<< HEAD
        response = redirect(url_for('auth_login', forward=fa.token, _external=True))
=======
        if app.config['SITE_URL']:
            response = redirect("%s%s" % ( app.config['SITE_URL'], url_for('auth_login', forward=fa.token)))
        else:
            response = redirect(url_for('auth_login', forward=fa.token))
>>>>>>> e9136bbd6e95a0c9a172a88557f5bb0086263641
        response.set_cookie('_fa_token', fa.token, expires=fa.expires)
        return response
    else:
        return redirect(url_for('home'))

@app.route('/forward/terminate')
@login_required
def forward_terminate():
    if 'token' in request.args:
        flash('The session {} was terminate.'.format(request.args['token']))
        fa = ForwardAuth.terminate_session(request.args['token'])
    return redirect(url_for('home'))
