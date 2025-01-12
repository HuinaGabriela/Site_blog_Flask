# Pasta que contem todas as tabelas do banco de dados.

from siteblogcomunidade import database, login_manager
from datetime import datetime
from flask_login import UserMixin # parametro que passamos a classe para controlar e manter o login conectado

# essa função que carrega o usuario no campo login
@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True) # chave primária, cada usuário tem um ID único
    username = database.Column(database.String, nullable=False) # Pode ter mais de uma pessoa com mesmo nome, mas não pode ter username vazio
    email = database.Column(database.String, nullable=False, unique=True) # Não pode estar vazio campo de email e não poder pode ter duas pessoas com o mesmo email
    senha = database.Column(database.String, nullable=False) # não precisa ser único, não pode ser vazio. Mesmo como texto estará codificado
    foto_perfil = database.Column(database.String, default='default.jpg') # string porque no banco sera armazenado ao nome do usuario a foto. Não pode ficar sem foto sera um avatar vazio
    posts = database.relationship('Post', backref='autor', lazy=True) # cada usuário pode ter varios posts. bacref serve para verificar post.autor busca o autor do post
    cursos = database.Column(database.String, nullable=False, default='Não Informado')

    def contar_posts(self):
            return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    corpo = database.Column(database.Text, nullable=False) # Quando for texto grande não pode ser string mas test 
    data_criacao = database.Column(database.DateTime, nullable=False, default=datetime.utcnow) # tem que passar a função e NÂO utcnow() senão todos vão criar o post no mesmo horario
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)