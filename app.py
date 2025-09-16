from flask import Flask, render_template, request, redirect, url_for, flash
from game import Personagem, RAÇAS, CLASSES, DistribuidorAtributos

app = Flask(__name__)
app.secret_key = "segredo"  # Necessário para usar flash messages


# ----------------- HOME -----------------
@app.route("/")
def index():
    return render_template("index.html")  # agora a home só mostra o menu


# ----------------- CRIAR PERSONAGEM -----------------
@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        nome = request.form["nome"]
        raca_nome = request.form["raca"]
        classe_nome = request.form["classe"]
        estilo = request.form.get("estilo", "classico")

        # selecionar atributos (por enquanto tudo clássico)
        if estilo == "classico":
            atributos = DistribuidorAtributos.estilo_classico()
        elif estilo == "aventureiro":
            atributos = DistribuidorAtributos.estilo_aventureiro()  # pode adaptar depois
        elif estilo == "heroico":
            atributos = DistribuidorAtributos.estilo_heroico()  # pode adaptar depois
        else:
            atributos = DistribuidorAtributos.estilo_classico()

        raca = RAÇAS.get(raca_nome)
        classe = CLASSES.get(classe_nome)

        p = Personagem(nome, atributos, raca, classe)
        p.salvar()

        flash(f"Personagem {nome} criado com sucesso!")
        return redirect(url_for("list_personagens"))

    return render_template("create.html", racas=RAÇAS.keys(), classes=CLASSES.keys())


# ----------------- VER PERSONAGEM -----------------
@app.route("/personagem/<nome>")
def personagem(nome):
    p = Personagem.carregar(nome)
    if not p:
        flash("Personagem não encontrado!")
        return redirect(url_for("list_personagens"))
    return render_template("personagem.html", personagem=p)


# ----------------- LISTAR PERSONAGENS -----------------
@app.route("/list")
def list_personagens():
    personagens = Personagem.listar_personagens()
    return render_template("list.html", personagens=personagens)


if __name__ == "__main__":
    app.run(debug=True)
