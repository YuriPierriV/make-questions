from flask import Flask, render_template, redirect, request, flash




app = Flask(__name__)
app.secret_key = 'toor'



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/cadastro")
def cadastro():
    return render_template('cadastro.html')


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')