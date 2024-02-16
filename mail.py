from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'  # enter your email here
app.config['MAIL_PASSWORD'] = 'your-password'  # enter your password here

mail = Mail(app)




import random
from flask import session

def send_otp():
    otp = random.randint(100000, 999999)
    session['otp'] = otp

    msg = Message('OTP', sender='your-email@gmail.com', recipients=['recipient-email@gmail.com'])
    msg.body = f'Your OTP is {otp}'
    mail.send(msg)



from flask import request, session

@app.route('/verify', methods=['POST'])
def verify():
    user_otp = request.form.get('otp')

    if 'otp' in session and user_otp == session['otp']:
        session.pop('otp')  # Clear OTP from session
        return 'OTP verified!'
    else:
        return 'Invalid OTP!', 400


# <form method="POST" action="/verify">
#     <input type="text" name="otp" placeholder="Enter OTP">
#     <button type="submit">Verify</button>
# </form>
