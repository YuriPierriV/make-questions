from flask import Flask, render_template, redirect, request, flash, url_for, session, abort
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash



db_config = {
    "host":"localhost",
    "user":"admin",
    "password":"admin",
    "database":"makequestions",
}

def db():
    return mysql.connector.connect(**db_config)

app = Flask(__name__)
app.secret_key = 'toor'

def obter_id_do_usuario_logado():
    # Verifique se 'user_id' está na sessão
    return session.get('user_id')


def obter_formularios_do_usuario(id_user):
    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, usuarios_id, nome, titulo, descricao, created_at FROM forms WHERE usuarios_id = %s", (id_user,))
    forms_tuplas = meu_cursor.fetchall()

    formularios = []
    for form_tupla in forms_tuplas:
        formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))
        formularios.append(formulario)

    return formularios


def obter_dados_do_formulario(id_forms):
    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, usuarios_id,nome, titulo, descricao, created_at FROM forms WHERE id = %s", (id_forms,))
    form_tupla = meu_cursor.fetchone()

    formulario = None
    if form_tupla:
        formulario = dict(zip(['id', 'usuarios_id','nome', 'titulo', 'descricao', 'created_at'], form_tupla))

    return formulario

def obter_dados_do_usuario(id_usuario):
    if id_usuario is None:
        return None  # ou uma resposta padrão se o ID do usuário não estiver definido

    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, nome, sobrenome, email, celular FROM usuarios WHERE id = %s", (id_usuario,))
    usuario_tupla = meu_cursor.fetchone()

    usuario = None
    if usuario_tupla:
        usuario = dict(zip(['id', 'nome', 'sobrenome', 'email', 'celular'], usuario_tupla))

    return usuario

def obter_questoes_do_formulario(id_formulario):
    if id_formulario is None:
        return None  # ou uma resposta padrão se o ID do usuário não estiver definido

    mydb = db()
    meu_cursor = mydb.cursor()

    meu_cursor.execute("SELECT id, question_text, question_type, correct_id FROM questions WHERE form_id = %s", (id_formulario,))
    questions_tuplas = meu_cursor.fetchall()

    questions = []
    for question_tupla in questions_tuplas:
        question = dict(zip(['id', 'question_text', 'question_type', 'correct_id'], question_tupla))
        questions.append(question)

    return questions

@app.route("/")
def index():
    if "user_id" in session:
        try:
            mydb = db()
            meu_cursor = mydb.cursor()

            meu_cursor.execute("SELECT id, nome, sobrenome, email, celular FROM usuarios WHERE id = %s", (session["user_id"],))
            usuario_tupla = meu_cursor.fetchone()

            if usuario_tupla:
                usuario = dict(zip(['id', 'nome', 'sobrenome', 'email', 'celular'], usuario_tupla))
                forms = obter_formularios_do_usuario(obter_id_do_usuario_logado())
                return render_template("painel.html", usuario=usuario, forms=forms)
            else:
                flash("Usuário não encontrado.")
                return render_template("index.html")

        except Exception as e:
            print(str(e))

        finally:
            mydb.close()

    return render_template("index.html")


@app.route("/cadastro")
def cadastro():
    if "user_id" in session:
        try:
            mydb = db()
            meu_cursor = mydb.cursor()

            meu_cursor.execute("SELECT id, nome, sobrenome, email, celular FROM usuarios WHERE id = %s", (session["user_id"],))
            usuario_tupla = meu_cursor.fetchone()

            if usuario_tupla:
                usuario = dict(zip(['id', 'nome', 'sobrenome', 'email', 'celular'], usuario_tupla))

                return redirect(url_for('index'))
            else:
                flash("Usuário não encontrado.")
                return redirect(url_for('cadastro'))

        except Exception as e:
            print(str(e))

        finally:
            mydb.close()

    return render_template("cadastro.html")

@app.route("/process_form", methods=['POST'])
def process_form():

    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        celular = request.form.get('celular')
        email = request.form.get('email')
        senha = request.form.get('senha')

        try:
            mydb = db()
            meu_cursor = mydb.cursor()

            meu_cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            resultado = meu_cursor.fetchone()

            if resultado:
                flash("Este email já está cadastrado. Por favor, escolha outro ou faça login.","cadastro")
                return redirect('/cadastro')  

            # Gere o hash da senha usando o método padrão do Werkzeug
            senha_hash = generate_password_hash(senha)

            meu_cursor.execute("INSERT INTO usuarios (nome, sobrenome, email, celular, senha_hash) VALUES (%s, %s, %s, %s, %s)",
                               (nome, sobrenome, email, celular, senha_hash))  

            meu_cursor.execute("SELECT id FROM usuarios WHERE email = %s", (email,))
            user_id = meu_cursor.fetchone()[0]

            mydb.commit()

            session["user_id"] = user_id

            flash("Cadastro realizado com sucesso!","cadastro")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e))
        
        return redirect("/cadastro")
    
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        mydb = db()

        cursor = mydb.cursor()
        cursor.execute("SELECT id, senha_hash FROM usuarios WHERE email = %s", (email,))
        user = cursor.fetchone()

        mydb.close()

        if user and check_password_hash(user[1], request.form["senha"]):
            session["user_id"] = user[0]

            return redirect(url_for("index"))
        else:
            flash("Email ou senha incorreto","login")
            return render_template("index.html", error="Credenciais inválidas")
        


@app.route("/newpage", methods=["POST"])
def newpage():
    if request.method == "POST":
        # Obtenha os dados do formulário

        # Insira os dados na tabela forms
        try:
            connection = db()
            cursor = connection.cursor()

            # Obtenha o ID do usuário logado (supondo que você tenha um sistema de login)
            user_id = session.get('user_id')

            # Insira o novo formulário na tabela forms
            cursor.execute("INSERT INTO forms (usuarios_id, nome, titulo, descricao) VALUES (%s,%s, %s, %s)",
                           (user_id,'Formulário sem Nome', 'Formulário sem Titulo', 'Descrição'))
            
            form_id = cursor.lastrowid

            cursor.execute("INSERT INTO questions (form_id, question_text, question_type, correct_id) VALUES (%s,%s, %s, %s)",
                           (form_id,'Pergunta sem título', 'type_text', None))
            # Commit e feche a conexão
            connection.commit()

            

            connection.close()

            return redirect(f'/form/{form_id}/edit')

        except mysql.connector.Error as err:
            print(f"Erro no MySQL: {err}")
            return "Erro ao criar formulário. Por favor, tente novamente."

    return redirect(url_for("index"))




@app.route("/form/<int:id_forms>/edit/att_form", methods=["POST"])
def atualizar_form(id_forms):
    # Obtenha os dados do formulário
    nome_param = next(iter(request.form))
    novo_valor = request.form.get(nome_param)

    try:
        connection = db()
        cursor = connection.cursor()

        # Atualize o campo no banco de dados
        cursor.execute(f"UPDATE forms SET {nome_param} = %s WHERE id = %s", (novo_valor, id_forms))

        # Commit e feche a conexão
        connection.commit()
        connection.close()

        return f"Campo {nome_param} do formulário atualizado com sucesso."

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."
    

@app.route("/form/<int:id_forms>/edit/att_question=<int:id_question>", methods=["POST"])
def atualizar_question(id_forms,id_question):
    # Obtenha os dados do formulário
    nome_param = next(iter(request.form))
    novo_valor = request.form.get(nome_param)

    try:
        connection = db()
        cursor = connection.cursor()

        # Atualize o campo no banco de dados
        cursor.execute(f"UPDATE questions SET {nome_param} = %s WHERE id = %s", (novo_valor, id_question))

        # Commit e feche a conexão
        connection.commit()
        connection.close()

        return f"Campo {nome_param} do formulário atualizado com sucesso."

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."

@app.route("/form/<int:id_forms>/edit/add", methods=["POST"])
def adicionar_campo(id_forms):
    # Obtenha os dados do formulário
    nome_param = next(iter(request.form))
    novo_valor = request.form.get(nome_param)

    try:
        connection = db()
        cursor = connection.cursor()

        # Atualize o campo no banco de dados
        cursor.execute(f"UPDATE forms SET {nome_param} = %s WHERE id = %s", (novo_valor, id_forms))

        # Commit e feche a conexão
        connection.commit()
        connection.close()

        return f"Campo {nome_param} do formulário atualizado com sucesso."

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."
    

@app.route("/excluir_formulario/<int:id_forms>", methods=['POST'])
def excluir_formulario(id_forms):
    # Obtenha os dados do formulário

    try:
        connection = db()
        cursor = connection.cursor()

        # Atualize o campo no banco de dados
        #DELETE FROM `forms` WHERE `id` = 1;
        cursor.execute(f"DELETE FROM `questions` WHERE `form_id` = %s", (id_forms,))
        cursor.execute(f"DELETE FROM `forms` WHERE `id` = %s", (id_forms,))

        # Commit e feche a conexão
        connection.commit()
        connection.close()

        return redirect(url_for("index"))

    except Exception as e:
        print(f"Erro ao remover formulário: {e}")
        abort(500)  # Internal Server Error


@app.route("/form/<int:id_forms>/edit")
def exibir_formulario(id_forms):
    # Obtenha os dados do formulário para exibição
    form = obter_dados_do_formulario(id_forms)
    user = obter_dados_do_usuario(obter_id_do_usuario_logado())
    questions = obter_questoes_do_formulario(id_forms)
    
    if form is None or user is None:
        return "Formulário ou usuário não encontrados."

    return render_template("formCreation.html", usuario=user, form=form,form_id=id_forms,questions=questions)




@app.route("/logout", methods=["POST"])
def logout():
    
    session.pop("user_id", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
