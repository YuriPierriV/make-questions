from flask import Flask, render_template, redirect, request, flash, url_for, session
import mysql.connector



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
    return render_template('index.html')


@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')

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
            meu_cursor.execute(f"INSERT INTO usuarios (nome,sobrenome,email,celular,senha_hash,senha_salt) VALUES ('{nome}','{sobrenome}','{email}','{celular}','{senha}','{senha}')")
            mydb.commit()
            flash("Enviado para o banco de dados")
        except Exception as e:
            flash(e);
        
        return redirect('/')
    
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]
        mydb = db()
        # Verificar as credenciais no banco de dados
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = %s AND senha_hash = %s", (email, senha))
        user = cursor.fetchone()
        print(user);
        mydb.close()

        if user:
            # Login bem-sucedido, armazena o ID do usuário na sessão
            session["user_id"] = user[0]
            return redirect(url_for("dashboard"))
        else:
            # Credenciais inválidas, exibir mensagem de erro
            flash("Login incorreto")
            return render_template("index.html", error="Credenciais inválidas")
        
@app.route("/dashboard")
def dashboard():

    if "user_id" in session:
        return render_template("dashboard.html")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
