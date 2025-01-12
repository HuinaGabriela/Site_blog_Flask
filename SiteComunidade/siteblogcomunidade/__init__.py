# Precisa instalar 'pip install flask-bcrypt' para criptografia das senhas
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
# permite o flask interligar varios arquivos de formularios, tabelas do banco, edicao visual, paginas frontend ...

# importa chamando o python na linha de comando e import secrets para não precisar criar um token manulamente
# python
# >>> import secrets
# >>> secrets.token_hex(16)
# >>> exit()


# cria a configuração do app e do banco de dados
app.config['SECRET_KEY'] = '4948e4bd059d478399d2ddf5d69f9d8c'
if os.getenv("DATABASE_URL"):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db' # caminho local onde o banco estará armazenado. Só seguir esse passo-a-passo padrão

database = SQLAlchemy(app)

# só o site conseguirá criptografar e descriptografar a senha do app(site)
bcrypt = Bcrypt(app)

# necessario para manter o controle de acesso do login conectado
login_manager = LoginManager(app)

# é a pagina que o login manager vai redirecionar quando for exigido login para acessar o conteúdo da página
login_manager.login_view = 'login' # redireciona para função de fazer login da página para acessá-la
# destaca a mensagem de alerta para estar logado em uma caixa azul clara
login_manager.login_message_category = 'alert-info'

# coloca o site no ar. Tem que ser colocado antes de ser criado o app
from siteblogcomunidade import routes
