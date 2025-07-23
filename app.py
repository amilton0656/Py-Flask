from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def principal():
    frutas = ["Morango", "Uva", "Maçã", "Laranja"]
    return render_template("index.html", frutas=frutas)

@app.route('/sobre')
def sobre():
    notas = { "Fulano":5.0, "Beltrano": 6.0, "Aluno": 7.0, "Sicrano": 8.5}
    return render_template('sobre.html', notas=notas)