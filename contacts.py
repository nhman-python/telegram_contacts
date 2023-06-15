import time
import os
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, render_template_string, request, redirect, session
import asyncio
import httpx


bot_token = ''  # טוקן מפאדר בוט
chat_owner = 12344  # החלף בid שלך

app = Flask(__name__)
app.secret_key = os.urandom(90)
allow_host = ['/', '/create_session']
app.config['SECRET_KEY'] = os.urandom(90)
csrf = CSRFProtect(app)

default_styles = """
    /* General styles */
    body {
      background-color: #111;
      color: #FFF;
      font-size: 20px;
      font-family: 'Roboto', Arial, sans-serif;
      overflow: hidden;
      margin: 0;
      padding: 0;
    }

    /* Container styles */
    .container {
      max-width: 90%;
      margin: 0 auto;
      padding: 60px;
      background-color: #000;
      border-radius: 8px;
      box-shadow: 0 0 40px rgba(255, 255, 255, 0.1);
      position: relative;
      z-index: 1;
    }

    /* Header styles */
    h1 {
      text-align: center;
      font-size: 32px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 40px;
      color: #FFF;
    }

    /* Textfield styles */
    .input-contacts {
      width: 100%;
      background-color: transparent;
      color: #FFF;
      border: none;
      border-bottom: 2px solid #FFF;
      padding: 16px;
      font-size: 20px;
      margin-bottom: 30px;
      transition: border-bottom-color 0.3s ease;
    }

    .input-contacts:focus {
      outline: none;
      border-bottom-color: #F00;
    }

    /* Success message styles */
    .success {
      color: green;
      font-weight: bold;
      text-align: center;
      margin-top: 30px;
      font-size: 20px;
    }

    /* Submit button styles */
    input[type="submit"] {
      background-color: #F00;
      color: #FFF;
      padding: 16px 32px;
      border: none;
      border-radius: 50px;
      cursor: pointer;
      font-size: 20px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-top: 40px;
      margin-bottom: 30px;
      transition: background-color 0.3s ease;
      box-shadow: 0 4px 10px rgba(255, 0, 0, 0.3);
    }

    input[type="submit"]:hover {
      background-color: #C00;
      box-shadow: 0 8px 20px rgba(255, 0, 0, 0.5);
      font-size: 25px;

    }

    /* Footer styles */
    .footer {
      text-align: center;
      margin-top: 60px;
      font-size: 20px;
      color: #FFF;
    }

    .footer a {
      color: #FFF;
      text-decoration: none;
      transition: color 0.3s ease;
    }

    .footer a:hover {
      color: #F00;
    }
"""


class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Send')


contacts_page = """
<!DOCTYPE html>
<html dir="rtl">
<head>
  <title>Contact Form</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
        /* General styles */
    body {
      background-color: #111;
      color: #FFF;
      font-size: 20px;
      font-family: 'Roboto', Arial, sans-serif;
      overflow: hidden;
      margin: 0;
      padding: 0;
    }

    /* Container styles */
    .container {
      max-width: 90%;
      margin: 0 auto;
      padding: 60px;
      background-color: #000;
      border-radius: 8px;
      box-shadow: 0 0 40px rgba(255, 255, 255, 0.1);
      position: relative;
      z-index: 1;
    }

    /* Header styles */
    h1 {
      text-align: center;
      font-size: 32px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-bottom: 40px;
      color: #FFF;
    }

    /* Textfield styles */
    .input-contacts {
      width: 100%;
      background-color: transparent;
      color: #FFF;
      border: none;
      border-bottom: 2px solid #FFF;
      padding: 16px;
      font-size: 20px;
      margin-bottom: 30px;
      transition: border-bottom-color 0.3s ease;
    }

    .input-contacts:focus {
      outline: none;
      border-bottom-color: #F00;
    }

    /* Success message styles */
    .success {
      color: green;
      font-weight: bold;
      text-align: center;
      margin-top: 30px;
      font-size: 20px;
    }

    /* Submit button styles */
    input[type="submit"] {
      background-color: #F00;
      color: #FFF;
      padding: 16px 32px;
      border: none;
      border-radius: 50px;
      cursor: pointer;
      font-size: 20px;
      text-transform: uppercase;
      letter-spacing: 2px;
      margin-top: 40px;
      margin-bottom: 30px;
      transition: background-color 0.3s ease;
      box-shadow: 0 4px 10px rgba(255, 0, 0, 0.3);
    }

    input[type="submit"]:hover {
      background-color: #C00;
      box-shadow: 0 8px 20px rgba(255, 0, 0, 0.5);
      font-size: 25px;

    }

    /* Footer styles */
    .footer {
      text-align: center;
      margin-top: 60px;
      font-size: 20px;
      color: #FFF;
    }

    .footer a {
      color: #FFF;
      text-decoration: none;
      transition: color 0.3s ease;
    }

    .footer a:hover {
      color: #F00;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>יצירת קשר טלגרם</h1>

    <form method="POST">
      {{ form.csrf_token }}
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" class="input-contacts" required>
      </div>

      <div class="form-group">
        <label for="message">Message:</label>
        <textarea id="message" name="message" class="input-contacts" rows="4" required></textarea>
      </div>

      <div class="form-group">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" class="input-contacts" required>
      </div>

      <input type="submit" value="שלח">
    </form>

    {% if redirect_message %}
    <p class="success">{{ redirect_message }}</p>
    {% endif %}

    {% if success %}
    <p class="success">{{ request_status }}</p>
    {% endif %}

    <div class="footer">
      <p>נוצר ב <span style="color: red;">&#9829;</span> <a href="https://t.me/python_tip_israel">{{ name }}</a></p>
    </div>
  </div>
</body>
</html>
"""


async def send_telegram(data):
    url_telegram = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url_telegram, data={'chat_id': chat_owner, 'text': data})
            response.raise_for_status()
            return response.status_code == 200
        except httpx.TimeoutException:
            return False
        except httpx.HTTPStatusError:
            return False


@app.before_request
def before_request():
    if request.path not in allow_host:
        session['previous_page'] = request.path
        return redirect('/', code=302)


@app.route('/', methods=['POST', 'GET'])
def index():
    success = False
    name = 'python-tip-israel-telegram'
    redirect_message = None
    request_status = 'ההודעה לא נשלחה נא לנסות שוב מאוחר יותר'
    previous_page = session.pop('previous_page', None)
    if previous_page and previous_page != '/':
        redirect_message = "הדף לא קיים, לכן הופניתה לדף הבית."

    form = ContactForm()

    if form.validate_on_submit():
        last_contact_time = session.get('last_contact_time')
        len_contact = sum(len(field.data) for field in [form.email, form.message, form.name])

        from_user = f'אמייל:{form.email.data}' \
                    f' שם:{form.name.data}' \
                    f' הודעה:{form.message.data}'
        if not last_contact_time or time.time() - last_contact_time > 180:
            data = f'🗂️ הודעה: {from_user}'
            if data:
                new_session_time = session.get('new_session_time')
                if not new_session_time or time.time() - new_session_time > 180:
                    session['last_contact_time'] = time.time()
                    session['new_session_time'] = time.time()
                    if 0 < len_contact <= 100:
                        res = asyncio.run(send_telegram(data))
                    else:
                        res = False
                    if res:
                        request_status = 'ההודעה נשלחה בהצלחה'
                    success = True
                else:
                    redirect_message = "למטרות אבטחה, עליך להמתין 3 דקות לפני שליחת הודעה נוספת."
            else:
                redirect_message = "הודעה ריקה. נא למלא את השדה."
        else:
            redirect_message = "ניתן לשלוח רק הודעה אחת כל 3 דקות."

    return render_template_string(contacts_page,
                                  success=success,
                                  name=name,
                                  redirect_message=redirect_message,
                                  form=form,
                                  request_status=request_status)


@app.route('/error', methods=['POST', 'GET'])
def redict_error():
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False)
