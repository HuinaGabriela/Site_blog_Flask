# Pasta de todas as páginas (links) do site comunidade

from flask import render_template, redirect, url_for, flash, request, abort
from siteblogcomunidade import database, app, bcrypt
from siteblogcomunidade.forms import FormLogin, FormCriarConta, FormEditarPerfil, FormCriarPost
from siteblogcomunidade.models import Usuario, Post
from flask_login import login_user, logout_user, login_required, current_user # current_user verifica se usuario esta logado
import secrets
import os
from PIL import Image
                                                                              # login_required atribui novas caracteristicas as funções como bloquear para exigir que usuario faça login  
# vai ser deletado, apenas para teste sem o banco de dados
#lista_usuarios = ['Huina', 'Maria', 'João', 'Gabriela', 'José']


# primeiro link a colocar o site no ar. Dentro dessa funcao mostramos o que sera exibido na página
@app.route('/')
def home():
    posts = Post.query.order_by(Post.id.desc()) # Atualiza os posts pela publicação mais atual
    return render_template('home.html', posts=posts)

@app.route("/contato")
def contato():
    return render_template('contato.html')

@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template('usuarios.html', lista_usuarios=lista_usuarios)

@app.route("/login", methods=['GET', 'POST']) # libera as informações do formulario
def login():
    Form_Login = FormLogin()
    Form_CriarConta = FormCriarConta()
    if Form_Login.validate_on_submit() and 'botao_submit_login' in request.form: # Se o login for validade quando submite
        # verica se usuario já existe e se a senha esta correta
        usuario = Usuario.query.filter_by(email=Form_Login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, Form_Login.senha.data):
            login_user(usuario, remember=Form_Login.lembrar_dados.data)
            # exibe mensagem de login bem sucedido e redireciona para home page
            flash(f'Login feito com sucesso no e-mail: {Form_Login.email.data}', 'alert-success')
            # pega o parametro que esta no argumento next e faz uma verificação, se não existe o next redireciona para página home se existir pede login e redireciona a pagina solicitada
            parametro_next = request.args.get('next')
            if parametro_next:
                return redirect(parametro_next)
            else:
                return redirect(url_for('home'))
        else:
            flash(f'Falha no login; E-mail ou senha incorretos:', 'alert-danger')
    if Form_CriarConta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        senha_crypt = bcrypt.generate_password_hash(Form_CriarConta.senha.data) # criptografa senha do usuario
        # criar o usuario
        usuario = Usuario(username=Form_CriarConta.username.data, email=Form_CriarConta.email.data, senha=senha_crypt)
        # adicionar a sessão
        database.session.add(usuario)
        # commit na sessão
        database.session.commit()
        # criou conta com sucesso
        flash(f'Conta criada para o e-mail: {Form_CriarConta.email.data}', 'alert-success')
        return redirect(url_for('home'))
    return render_template('login.html', Form_Login=Form_Login, Form_CriarConta=Form_CriarConta) # Adcionando o form_login e form_criarconta para serem acessados no login.html

# personalizando pagina após usuario estar logado
# cria o post só do usuario logado
# colocar o botão de sair e meu perfil

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash(f'Logout feito com sucesso!', 'alert-success')
    return redirect(url_for('home'))


@app.route('/perfil')
@login_required
def perfil():
    # precisa do parametro foto_perfil descrito na classe usuarios, é passado como uma variavel do perfil que esta logado
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('perfil.html', foto_perfil=foto_perfil)


@app.route('/post/criar', methods=['GET', 'POST']) # methods=['GET', 'POST'] autoriza a criação do post
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(titulo=form.titulo.data, corpo=form.corpo.data, autor=current_user)
        database.session.add(post)
        database.session.commit()
        flash('Post Criado com Sucesso', 'alert-success')
        return redirect(url_for('home'))
    return render_template('criarpost.html', form=form)

def salvar_imagem(imagem):
    # adicionar um código aleatório no nome da imagem
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao
    # reduzir o tamanho da imagem
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    tamanho = (250, 250)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # mudar o campo foto_perfil do usuário para o novo nome da imagem
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo

def atualizar_cursos(form):
    # percorrer todos os campos do formulario e verificar se tem algum curso com a caixa marcada
    lista_cursos = []
    for campo in form:
        if 'curso_' in campo.name:
            if campo.data: # verifica se o campo esta marcado
            # adicionar o texto do campo.label (Curso python) na lista de cursos
                lista_cursos.append(campo.label.text)
    return ';'.join(lista_cursos)

# criar uma nova página para edição do botão "editar pefil"
@app.route('/perfil/editar', methods=['GET', 'POST'])
# para editar o perfil o usuario deve estar obrigatóriamente logado
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.username = form.username.data
        # verificar se tem que mudar a foto(se foi feito upload de uma imagem)
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data)
            current_user.foto_perfil = nome_imagem
        current_user.cursos = atualizar_cursos(form)
        database.session.commit()
        flash(f'Perfil atualizado com Sucesso!', 'alert-success')
        return redirect(url_for('perfil'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
    foto_perfil = url_for('static', filename='fotos_perfil/{}'.format(current_user.foto_perfil))
    return render_template('editarperfil.html', foto_perfil=foto_perfil, form=form)


@app.route('/post/<post_id>', methods=['GET', 'POST'])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        if request.method == 'GET':
            form.titulo.data = post.titulo
            form.corpo.data = post.corpo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.corpo = form.corpo.data
            database.session.commit()
            flash('Post Atualizado com Sucesso', 'alert-success')
            return redirect(url_for('home'))
    else:
        form = None
    return render_template('post.html', post=post, form=form)

@app.route('/post/<post_id>/excluir', methods=['GET', 'POST'])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash('Post Excluído com Sucesso', 'alert-danger')
        return redirect(url_for('home'))
    else:
        abort(403)