from flask import Blueprint, render_template, request, redirect, url_for
from game import Personagem, RAÇAS, CLASSES, DistribuidorAtributos

routes = Blueprint("routes", __name__)

@routes.route("/")
def index():
    personagens = Personagem.listar_personagens()
    return render_template("index.html", personagens=personagens)

@routes.route("/criar", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        nome = request.form["nome"]
        raca = RAÇAS[request.form["raca"]]
        classe = CLASSES[request.form["classe"]]
        estilo = request.form["estilo"]

        if estilo == "classico":
            atributos = DistribuidorAtributos.estilo_classico()
        else:
            atributos = DistribuidorAtributos.estilo_classico()

        personagem = Personagem(nome, atributos, raca, classe)
        personagem.salvar()
        return redirect(url_for("routes.personagem", nome=nome))

    return render_template("create.html", racas=RAÇAS, classes=CLASSES)

@routes.route("/personagem/<nome>")
def personagem(nome):
    p = Personagem.carregar(nome)
    return render_template("personagem.html", personagem=p)
