from flask import Flask, render_template, redirect, request, url_for
from flask_mail import Mail, Message
import os


app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "sena_codes"

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ.get('EMAIL_USER'),
    "MAIL_PASSWORD": os.environ.get('EMAIL_PASS')
}


app.config.update(mail_settings)
mail = Mail(app)

class Contato:
    def __init__(self, nome, email, mensagem):
        self.nome = nome
        self.email = email
        self.mensagem = mensagem


# Rotas
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/send', methods=['GET', 'POST'])
def send():
    if request.method == 'POST':
        formContato = Contato(
            request.form["nome"],
            request.form["email"],
            request.form["mensagem"]
        )

        msg = Message(
            subject = f'{formContato.nome} te enviou uma mensagem no portfólio',
            sender = app.config.get("MAIL_USERNAME"),
            recipients= ['docencia.thiago@gmail.com', app.config.get("MAIL_USERNAME")],
            body = f'''
            
            {formContato.nome} com o e-mail {formContato.email}, te enviou a seguinte mensagem:

            {formContato.mensagem}

            '''
        )

        mail.send(msg)
        flash('Mensagem enviada com sucesso!')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
