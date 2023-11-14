from flask import Flask, render_template, redirect, request, flash
import mysql.connector






app = Flask(__name__)
app.secret_key = 'toor'

try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="admin",
        password="admin",
        database="makequestions",
    )
    print("Conectado ao bd");
except mysql.connector.Error as e:
    print(e);


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
            meu_cursor = mydb.cursor()
            meu_cursor.execute(f"INSERT INTO usuarios (nome,sobrenome,email,celular,senha_hash,senha_salt) VALUES ('{nome}','{sobrenome}','{email}','{celular}','{senha}','{senha}')")
            mydb.commit()
            flash("Enviado para o banco de dados")
        except meu_cursor.execute or mydb.commit as e:
            flash(e);
        

        
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')