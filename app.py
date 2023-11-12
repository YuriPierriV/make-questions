from flask import Flask, render_template, redirect, request, flash




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

        
        print(f"Nome: {nome}, Sobrenome: {sobrenome}, Celular: {celular}, Email: {email}, Senha: {senha}")

        
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')