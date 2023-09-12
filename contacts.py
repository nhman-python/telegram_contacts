from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired
from flask import Flask, render_template, request, redirect, flash, url_for
import asyncio
import httpx
import pytz
import datetime
from dotenv import load_dotenv
import os
load_dotenv()
bot_token = os.getenv('bot_token')
chat_owner = os.getenv('chat_owner')
app = Flask(__name__)
app.secret_key = os.urandom(32)


class ContactForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('submit')


def time_now():
    tz = pytz.timezone('Asia/Jerusalem')
    return datetime.datetime.now(tz=tz).strftime('%Y-%m-%d %H:%M:%S')


async def send_telegram(data):
    url_telegram = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    async with httpx.AsyncClient(timeout=3) as client:
        try:
            response = await client.post(url_telegram, data={'chat_id': chat_owner, 'text': data})
            response.raise_for_status()
            print(response.status_code)
            return response.status_code == 200
        except httpx.TimeoutException:
            return False
        except httpx.HTTPStatusError:
            return False


@app.route('/', methods=['POST', 'GET'])
def index():
    year = datetime.datetime.now().year
    form = ContactForm()
    if request.method == 'POST':
        print('post')
        if form.validate_on_submit():
            user_agent = request.headers.get('User-agent')
            ip_address = request.remote_addr

            from_user = f'📧 Email: {form.email.data}\n'
            from_user += f'👤 Name: {form.name.data}\n'
            from_user += f'💬 Message: {form.message.data}\n'
            from_user += f'⏰ Time sent: {time_now()}\n'
            from_user += f'🖥️ User agent: {user_agent}\n'
            from_user += f'🌐 IP Address: {ip_address}'
            if asyncio.run(send_telegram(from_user)):
                flash('✅ The message was sent successfully! 🚀', 'success')
                return redirect(url_for('index'))
            flash('❌ Failed to send the message. Please try again later. 😔', 'danger')
            return redirect(url_for('index'))
        flash('⚠️ Something is not right. Please try again. 🤔', 'danger')
    return render_template('index.html', form=form, year=year)


if __name__ == '__main__':
    app.run(debug=False)
