from flask import Flask, render_template, redirect, request, flash, url_for, session, abort, jsonify, send_file
import io
import traceback
import mysql.connector
from uteis.mydb import db
from uteis.functions import obter_formularios_do_usuario, obter_dados_do_formulario, obter_dados_do_usuario, obter_questoes_do_formulario, save_image_to_db, associate_image_question, allowed_file, associate_image_user
from werkzeug.security import generate_password_hash, check_password_hash
from uteis.usuario import Usuario
from uteis.forms import Forms
from uteis.questions import Questions
from uteis.answer import Answer
import secrets
import base64

app = Flask(__name__)
app.secret_key = 'toor'


@app.route("/")
def index():
    if "user_id" not in session:
        return render_template("index.html")

    usuario = Usuario()
    if not usuario.getUsuario(session["user_id"]):
        flash("Usuário não encontrado.")
        return render_template("index.html")

    usuario.get_image()

    if "token" in session:
        token = session["token"]
        try:
            form = Forms()
            form.byLink(token)
            if usuario.setPermission(form.id):
                del session["token"]
                return redirect(f'/form/link/{token}')
            else:
                flash("Erro ao definir permissões.")
                return render_template("index.html")
        except Exception as e:
            flash(f"Ocorreu um erro: {e}")
            return render_template("index.html")

    forms = usuario.formularios()
    participando = []
    respondido = []

    for p in usuario.participando:
        form = Forms()
        form.getForms(p)
        form.setDono(form.usuarios_id)
        form.getLink()
        participando.append(form)

    for r in usuario.respondido:
        form = Forms()
        form.getForms(r)
        form.setDono(form.usuarios_id)
        form.getLink()
        respondido.append(form)
    

    return render_template("painel.html", 
                           usuario=usuario, 
                           forms=forms, 
                           participando=participando, 
                           respondido=respondido)
    
        



@app.route("/cadastro")
def cadastro():
    if "user_id" in session:
        usuario = Usuario()
        usuario.getUsuario(session["user_id"])
        usuario.get_image()
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
    try:
        usuario.getUsuario(session["user_id"])
        usuario.get_image()
        form = Forms()
        form.getForms(id_forms)
        form.getLink()
        if form.usuarios_id != session["user_id"]:
            return redirect(url_for("index"))
        questions_json = form.get_questions_json()
        questions = form.get_questions()
        for question in questions:
            question.get_options()
            question.get_image()

        if form is None or usuario is None:
            return "Formulário ou usuário não encontrados."

        return render_template("formCreation.html", usuario=usuario, form=form, form_id=id_forms, questions_json=questions_json, questions=questions)
    except Exception as e:
        return redirect(url_for("index"))
    


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

    except Exception as err:
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

    except Exception as err:
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

    except Exception as err:
        print(f"Erro no MySQL: {err}")
        return f"Erro ao atualizar campo {nome_param} do formulário. Por favor, tente novamente."
    

@app.route("/excluir_formulario/<int:id_forms>", methods=['POST'])
def excluir_formulario(id_forms):
    try:
        mydb = db()
        cursor = mydb.cursor()

        # Seleciona todos os ids das questões relacionadas ao formulário
        cursor.execute("SELECT id FROM questions WHERE form_id = %s", (id_forms,))
        question_ids = cursor.fetchall()

        # Exclui todos os registros da tabela `link` relacionados ao formulário
        cursor.execute("DELETE FROM `link` WHERE `forms_id` = %s", (id_forms,))

        # Para cada questão, exclui os registros relacionados nas tabelas `options`, `answers` e `question_images`
        for question_id in question_ids:
            cursor.execute("DELETE FROM `answers` WHERE `question_id` = %s", (question_id[0],))
            cursor.execute("DELETE FROM `options` WHERE `question_id` = %s", (question_id[0],))
            cursor.execute("DELETE FROM `question_images` WHERE `question_id` = %s", (question_id[0],))

        # Exclui as questões relacionadas ao formulário
        cursor.execute("DELETE FROM `questions` WHERE `form_id` = %s", (id_forms,))

        # Exclui todos os registros da tabela `permission` relacionados ao formulário
        cursor.execute("DELETE FROM `permission` WHERE `forms_id` = %s", (id_forms,))

        # Exclui o formulário
        cursor.execute("DELETE FROM `forms` WHERE `id` = %s", (id_forms,))

        # Confirma as alterações e fecha a conexão com o banco de dados
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
            return 'changed'
        except Exception as e:
            return str(e)  


@app.route('/new_link', methods=['POST'])
def new_link():
    if request.method == 'POST':
        form_id = request.form.get('form_id')
        try:
            mydb = db()
            cursor = mydb.cursor()
            
            token = secrets.token_urlsafe(16) 
            cursor.execute("DELETE FROM `link` WHERE `forms_id` = %s", (form_id,))

            cursor.execute("INSERT INTO link (token, forms_id,permission) VALUES (%s,%s,%s)",
                            (token,form_id,'default'))

            mydb.commit()
            mydb.close()
            return redirect(f'/form/{form_id}/edit')
        except Exception as e:
            print(e)
            return str(e)  

        

@app.route("/form/link/<token>")
def link(token):

    form = Forms()
    verification,permission = form.byLink(token)
    
    if verification:
        
        if "user_id" in session:
            usuario = Usuario()
            
            if usuario.getUsuario(session["user_id"]):
                usuario.get_image()
                if usuario.check_permission(form.id):
                    questions_json = form.get_questions_json()
                    questions = form.get_questions()
                    for question in questions:
                        question.correct_id = "Não tente fazer isso, s2"
                        question.get_options()
                        question.get_image()
                    return render_template("form.html",usuario=usuario, form=form, questions_json=questions_json, questions=questions)
                else:
                    session["token"] = token
                    return redirect(url_for('index'))
            else:
                flash("Usuário não encontrado. Ou permissão insuficiente")
                session["token"] = token
                return redirect(url_for('cadastro'))
        else:
            session["token"] = token
            return redirect(url_for('cadastro'))
    else:
        return redirect(url_for('index'))



@app.route('/question-image/<int:id_question>', methods=['POST'])
def upload_image(id_question):
    file = request.files['image']
    if file and allowed_file(file.filename):
        try:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode('utf-8')
            image_id = save_image_to_db(base64_encoded)
            if image_id and associate_image_question(id_question, image_id):
                return jsonify(success=True), 200
            else:
                return jsonify(success=False), 500
        except Exception as e:
            print(traceback.format_exc())  # Isso ajudará no diagnóstico de problemas
            return jsonify(success=False, error=str(e)), 500
    return jsonify(success=False, error="No file or invalid file type"), 400


@app.route('/user-image/<int:id_user>', methods=['POST'])
def upload_image_user(id_user):
    file = request.files['image']
    if file and allowed_file(file.filename):
        try:
            file_content = file.read()
            base64_encoded = base64.b64encode(file_content).decode('utf-8')
            image_id = save_image_to_db(base64_encoded)
            if image_id and associate_image_user(id_user, image_id):
                return jsonify(success=True), 200
            else:
                return jsonify(success=False), 500
        except Exception as e:
            print(traceback.format_exc())  # Isso ajudará no diagnóstico de problemas
            return jsonify(success=False, error=str(e)), 500
    return jsonify(success=False, error="No file or invalid file type"), 400

@app.route('/get-image/<int:image_id>')
def get_image(image_id):
    conn = db() 
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT image_data FROM images WHERE id = %s", (image_id,)) 
        row = cursor.fetchone()
        if row:
            image_data = base64.b64decode(row[0])  # Supondo que a imagem está armazenada como BLOB
            return send_file(
                io.BytesIO(image_data),
                mimetype='image/jpeg'  
            )
    except Exception as e:
        return print(f"Erro ao recuperar a imagem: {e}", status=500)
    finally:
        cursor.close()
        conn.close()
    return print("Imagem não encontrada", status=404)



@app.route('/send_answer', methods=['POST'])
def send_answer():
    if request.method == 'POST':
        question_id = request.form.get('question_id')
        user_id = session["user_id"]
        selected_id = request.form.get('selected_id')
        response_text = request.form.get('response_text')
        try:
            conn = db() 
            cursor = conn.cursor()

            cursor.execute("INSERT INTO answers (question_id,user_id,response_text,enviado,selected_id) VALUES (%s,%s,%s,%s,%s);",
                            (question_id,user_id,response_text,1,selected_id))
            return redirect(url_for("index"))
        except Exception as e:
            return print(f"Erro ao enviar resposta: {e}")
        finally:
            conn.commit()
            conn.close()
    return redirect(url_for("index"))


@app.route("/logout", methods=["POST"])
def logout():
    
    session.pop("user_id", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
