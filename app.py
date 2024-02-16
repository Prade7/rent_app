
from start import app,socketio
from forms.login_signup import login_signup
from forms.after_login import after_login



app.register_blueprint(login_signup)
app.register_blueprint(after_login)


if(__name__=="__main__"):
    socketio.run(app, debug=True)
 