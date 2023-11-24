from flask import Flask, render_template, redirect, request, flash, url_for, session
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

                return render_template("painel.html", usuario=usuario)
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
                flash("Este email já está cadastrado. Por favor, escolha outro","cadastro")
                return redirect('/cadastro')  

            # Gere o hash da senha usando o método padrão do Werkzeug
            senha_hash = generate_password_hash(senha)

            meu_cursor.execute("INSERT INTO usuarios (nome, sobrenome, email, celular, senha_hash, senha_salt) VALUES (%s, %s, %s, %s, %s, %s)",
                               (nome, sobrenome, email, celular, senha_hash, None))  # None para o campo senha_salt por enquanto

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
    ##Fazer aqui a criação de nova página
    return render_template("index.html")






@app.route("/logout", methods=["POST"])
def logout():
    
    session.pop("user_id", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
