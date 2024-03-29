from flask import Flask, render_template, redirect, request, flash, url_for, session, abort
import mysql.connector
from uteis.connection import db
from uteis.functions import obter_formularios_do_usuario, obter_dados_do_formulario, obter_dados_do_usuario, obter_questoes_do_formulario
from werkzeug.security import generate_password_hash, check_password_hash
from uteis.usuario import Usuario
from uteis.forms import Forms
from uteis.questions import Questions

app = Flask(__name__)
app.secret_key = 'toor'



@app.route("/")
def index():
    if "user_id" in session:
        usuario = Usuario()
        usuario.getUsuario(session["user_id"])
        if usuario:
            forms = usuario.formularios()
            return render_template("painel.html", usuario=usuario, forms=forms)
        else:
                flash("Usuário não encontrado.")
                return render_template("index.html")
    else:
        return render_template("index.html")
        

    


@app.route("/cadastro")
def cadastro():
    if "user_id" in session:
        usuario = Usuario()
        usuario.getUsuario(session["user_id"])
        if usuario:
            return redirect(url_for('index'))
        else:
            flash("Usuário não encontrado.")
            return redirect(url_for('cadastro'))
    else:
        return render_template("cadastro.html")



@app.route("/process_form", methods=['POST'])
def process_form():
    if request.method == 'POST':
        nome = request.form.get('nome')
        sobrenome = request.form.get('sobrenome')
        celular = request.form.get('celular')
        email = request.form.get('email')
        senha = generate_password_hash(request.form.get('senha'))

        usuario = Usuario(nome, sobrenome, email, celular, senha)
        if usuario.cadastra():
            return redirect(url_for("index"))
        else:
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
        
        forms = Forms()
        if forms.cria_form():
            
            question = Questions()
            if question.cria_question(forms):
                
                return redirect(f'/form/{forms.id}/edit')
            
        else:
            print(f"Erro no MySQL: ")
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
    

@app.route("/form/<int:id_forms>/edit/att_question=<int:id_question>", methods=["PUT"])
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
    user = obter_dados_do_usuario(session["user_id"])
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
