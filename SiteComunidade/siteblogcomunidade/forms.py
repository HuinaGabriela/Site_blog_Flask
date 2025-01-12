from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed # FileFiel é um campo de arquivo que a pessoa clica e pode escolher qual arquivo quer fazer dowload e FileAllowed é um validador através dele que podemos escolher as extensões de arquivo permitidas para dawload da imagem
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField 
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from siteblogcomunidade.models import Usuario
from flask_login import current_user


# Criando uma classe para cada formulario (login e criar conta)
# Class Recebe como herança os parametros do FlaskForm. Não precisa o __ini__.
# flask_wtf faz algumas validações(email, campos iguais...)
# criando proteção para o site(csrf token)

class FormCriarConta(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    botao_submit_criarconta = SubmitField('Criar Conta')

    # verifica se o email já existe no banco de dados
    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado! Cadastre-se com outro e-mail ou faça login para continuar.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    lembrar_dados = BooleanField('lembrar dados de Acesso') # será uma caixa de marcar
    botao_submit_login = SubmitField('Fazer Login')


class FormEditarPerfil(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    # adicionando o campo de imagem
    foto_perfil = FileField('Atualizar foto de Perfil', validators=[FileAllowed(['jpg', 'png'])])
    # adicionar os cursos no html do formulário
    curso_cplusplus = BooleanField('Curso C/C++')
    curso_python = BooleanField('Curso Python avançado')
    curso_powerbi = BooleanField('Curso PowerBi')
    curso_sql = BooleanField('Curso SQL')
    curso_AI = BooleanField('Curso Inteligência Artificial')
    botao_submit_editarperfil = SubmitField('Confirmar Edição')

    def validate_email(self, email):
            # verifica se o campo de edição de perfil não foi adicionado um email já cadastrado
            if current_user.email != email.data:
                usuario = Usuario.query.filter_by(email=email.data).first()
                if usuario:
                    raise ValidationError('Já existe um usuário com este e-mail utilize um outro email.')


class FormCriarPost(FlaskForm):
    titulo = StringField('Título do Post', validators=[DataRequired(), Length(2, 140)])
    corpo = TextAreaField('Escreva seu Post Aqui', validators=[DataRequired()])
    botao_submit = SubmitField('Criar Post')