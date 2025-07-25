from flask import Flask, render_template, request, redirect, url_for, flash
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.secret_key = "chave secreta"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "apiflask.sqlite3")

db = SQLAlchemy(app)

frutas = []
registros = []

class cursos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    ch = db.Column(db.Integer)

    def __init__(self, nome, descricao, ch):
        self.nome = nome
        self.descricao = descricao
        self.ch = ch

@app.route('/', methods=["GET", "POST"])
def principal():
    if request.method == "POST":
        print("11")
        if request.form.get("fruta"):
            print("22")
            frutas.append(request.form.get("fruta"))

    return render_template("index.html", frutas=frutas)

@app.route('/sobre', methods=["GET", "POST"])
def sobre():
    if request.method == "POST":
        if request.form.get("aluno") and request.form.get("nota"):
            registros.append({"aluno": request.form.get("aluno"), "nota": request.form.get("nota")})
    return render_template('sobre.html', registros=registros)

@app.route('/filmes/<propriedade>')
def filmes(propriedade):
    if propriedade == 'populares':
        url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=969e9563e021a4f270024589412edc55"

    elif propriedade == 'kids':
        url = "https://api.themoviedb.org/3/discover/movie?certification_country=US&certification.lte=G&sort_by=popularity.desc&api_key=969e9563e021a4f270024589412edc55"

    elif propriedade == "2010":
        url = "https://api.themoviedb.org/3/discover/movie?primary_release_year=2010&sort_by=vota_average.desc&api_key=969e9563e021a4f270024589412edc55"

    elif propriedade == "drama":
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=18&sort_by=vote_average.desc&vote_count.gte=10&api_key=969e9563e021a4f270024589412edc55"    

    elif propriedade == 'tom_cruise':
        url = "https://api.themoviedb.org/3/discover/movie?with_genres=878&with_casat=500&sort_by=vote_average.desc&api_key=969e9563e021a4f270024589412edc55"

    resposta = urllib.request.urlopen(url)
    dados = resposta.read()
    jsondata = json.loads(dados)
    return render_template('filmes.html', filmes=jsondata['results'])

@app.route('/cursos')
def listar_cursos():
    page = request.args.get('page', 1, type=int)
    per_page = 4
    todos_cursos = cursos.query.paginate(page=page, per_page=per_page)
    return render_template("cursos.html", cursos=todos_cursos)

@app.route('/add_curso', methods=["GET", "POST"])
def add_curso():

    nome = request.form.get('nome') 
    descricao = request.form.get('descricao')
    ch = request.form.get('ch')

    if request.method == "POST":

        if not nome or not descricao or not ch:
            flash("Preencha todos os campos do formulário", "error")
        else:
            curso = cursos(nome, descricao, ch)
            db.session.add(curso)
            db.session.commit()
            return redirect(url_for('listar_cursos'))

    return render_template('add_curso.html')

@app.route('/<int:id>/edit_curso', methods = ["GET", "POST"])
def edit_curso(id):
    curso = cursos.query.filter_by(id=id).first()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        ch = request.form["ch"]
        cursos.query.filter_by(id=id).update({"nome":nome, "descricao":descricao, "ch":ch})
        db.session.commit()
        return redirect(url_for('listar_cursos'))
    return render_template('edit_curso.html', curso=curso)

@app.route('/<int:id>/remove_curso')
def remove_curso(id):
    curso = cursos.query.filter_by(id=id).first()

    db.session.delete(curso)
    db.session.commit()
    return redirect(url_for('listar_cursos'))

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)