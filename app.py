from flask import Flask, render_template, redirect, request, flash, url_for, session, abort
import mysql.connector
from uteis.mydb import db
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
        senha = request.form["senha"]

        usuario = Usuario()
        if usuario.login(email,senha):
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
            flash("Erro no MySQL: ")
            return redirect(url_for("index"))


@app.route("/form/<int:id_forms>/edit")
def exibir_formulario(id_forms):
    usuario = Usuario()
    usuario.getUsuario(session["user_id"])
    form = Forms()
    form.getForms(id_forms)
    questions_json = form.get_questions_json()
    questions = form.get_questions()
    for question in questions:
        question.get_options()

    if form is None or usuario is None:
        return "Formulário ou usuário não encontrados."

    return render_template("formCreation.html", usuario=usuario, form=form, form_id=id_forms, questions_json=questions_json, questions=questions)


@app.route("/form/<int:id_forms>/edit/att_form", methods=["PUT"])
def atualizar_form(id_forms):
    nome_param = next(iter(request.form))
    novo_valor = request.form.get(nome_param)
    try:
        mydb = db()
        cursor = mydb.cursor()

        # Atualize o campo no banco de dados
        cursor.execute(f"UPDATE forms SET {nome_param} = %s WHERE id = %s", (novo_valor, id_forms))

        mydb.commit()
        mydb.close()

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
        mydb = db()
        cursor = mydb.cursor()
        cursor.execute(f"UPDATE questions SET {nome_param} = %s WHERE id = %s", (novo_valor, id_question))
        
            

        mydb.commit()
        mydb.close()

        if novo_valor == 'multimult_escolha':
            
            question = Questions(id_question)
            question.cria_options_padrao()

        if novo_valor == 'text':

            question = Questions(id_question)
            question.remove_options()

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
        mydb = db()
        cursor = mydb.cursor()


        cursor.execute(f"UPDATE forms SET {nome_param} = %s WHERE id = %s", (novo_valor, id_forms))

        mydb.commit()
        mydb.close()

        return f"Campo {nome_param} do formulário atualizado com sucesso."

    except mysql.connector.Error as err:
        print(f"Erro no MySQL: {err}")
        return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."
    

@app.route("/excluir_formulario/<int:id_forms>", methods=['POST'])
def excluir_formulario(id_forms):
    try:
        mydb = db()
        cursor = mydb.cursor()

        # Recupera todos os IDs das perguntas associadas ao formulário
        cursor.execute("SELECT id FROM questions WHERE form_id = %s", (id_forms,))
        question_ids = cursor.fetchall()

        # Exclui todas as opções associadas a cada pergunta
        for question_id in question_ids:
            cursor.execute("DELETE FROM `options` WHERE `question_id` = %s", (question_id[0],))

        # Exclui todas as perguntas associadas ao formulário
        cursor.execute("DELETE FROM `questions` WHERE `form_id` = %s", (id_forms,))

        # Exclui o próprio formulário
        cursor.execute("DELETE FROM `forms` WHERE `id` = %s", (id_forms,))

        mydb.commit()
        mydb.close()

        return redirect(url_for("index"))

    except Exception as e:
        print(f"Erro ao remover formulário: {e}")
        abort(500)  # Internal Server Error



@app.route('/add_question',methods=['POST'])
def adicionar_questao():
    if request.method == 'POST':
        id_forms = request.form.get('id_form')
        forms = Forms()
        forms.getForms(id_forms)
        question = Questions()
        if question.cria_question(forms):
            # Redirecionar para a página de edição do formulário, passando o ID do formulário
            return redirect(url_for('exibir_formulario', id_forms=id_forms))
        else:
            return "Erro na criação da questão"


@app.route('/del_question', methods=['POST'])
def excluir_questao():
    if request.method == 'POST':
        id_question = request.form.get('id_question')
        try:
            mydb = db()
            cursor = mydb.cursor()

            # Excluir todas as opções associadas à questão
            cursor.execute("DELETE FROM `options` WHERE `question_id` = %s", (id_question,))

            # Excluir a própria questão
            cursor.execute("DELETE FROM `questions` WHERE `id` = %s", (id_question,))

            mydb.commit()
            mydb.close()

            # Redirecionar para a página de edição do formulário ou para qualquer outra página apropriada
            return 'ok'

        except Exception as e:
            print(f"Erro ao remover questão: {e}")
            abort(500)  # Internal Server Error



@app.route('/add_options', methods=['POST'])
def adicionar_options():
    if request.method == 'POST':
        questionId = request.form.get('questionId')  
        novoValor = request.form.get('novoValor')
        question = Questions(questionId)
        if question.cria_options_text(novoValor):
            return 'Funcionou'
        else:
            return 'erro'
        

@app.route('/edit_options', methods=['POST'])
def editar_options():
    if request.method == 'POST':
        optionId = request.form.get('optionId')  # Corrigido o nome do parâmetro
        novoValor = request.form.get('novoValor')

        try:
            mydb = db()
            cursor = mydb.cursor()

            # Correção na construção da string SQL e passagem dos parâmetros
            sql = "UPDATE options SET option_text = %s WHERE id = %s"
            cursor.execute(sql, (novoValor, optionId))

            mydb.commit()
            mydb.close()
            return 'Funcionou'
        except Exception as e:
            return str(e)  # Convertido o erro para string para retorná-lo como resposta HTTP


        
@app.route('/obrigatorio', methods=['POST'])
def obrigatorio():
    if request.method == 'POST':
        question_id = request.form.get('question_id')
        is_required = request.form.get('is_required')
        is_required = True if is_required == '1' else False
        
        try:
            mydb = db()
            cursor = mydb.cursor()
            if(is_required):
                cursor.execute("UPDATE questions SET required = true WHERE id = %s", (question_id,))
            else:
                cursor.execute("UPDATE questions SET required = false WHERE id = %s", (question_id,))

            mydb.commit()
            mydb.close()
            return 'Funcionou'
        except Exception as e:
            return str(e)  




        



@app.route("/logout", methods=["POST"])
def logout():
    
    session.pop("user_id", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
